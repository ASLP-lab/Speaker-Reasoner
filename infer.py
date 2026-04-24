import argparse
import json
import logging
import os
import re
import warnings
from decimal import Decimal
from pathlib import Path

os.environ['VLLM_USE_V1'] = '1'
os.environ['VLLM_WORKER_MULTIPROC_METHOD'] = 'spawn'
os.environ['VLLM_LOGGING_LEVEL'] = 'INFO'

import torch
import torchaudio
from qwen_omni_utils import process_mm_info
from transformers import Qwen3OmniMoeProcessor

warnings.filterwarnings('ignore')

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def _load_model_processor(model_path: str, use_transformers: bool = False, use_flash_attn2: bool = True):
    if use_transformers:
        from transformers import Qwen3OmniMoeForConditionalGeneration
        kwargs = {'dtype': 'auto', 'device_map': 'auto'}
        if use_flash_attn2:
            kwargs['attn_implementation'] = 'flash_attention_2'
        model = Qwen3OmniMoeForConditionalGeneration.from_pretrained(model_path, **kwargs)
    else:
        from vllm import LLM
        model = LLM(
            model=model_path,
            trust_remote_code=True,
            gpu_memory_utilization=0.95,
            tensor_parallel_size=torch.cuda.device_count(),
            limit_mm_per_prompt={'image': 1, 'video': 1, 'audio': 100},
            max_num_seqs=1,
            max_model_len=32768,
            seed=1234,
            enable_prefix_caching=True,
        )
    processor = Qwen3OmniMoeProcessor.from_pretrained(model_path)
    return model, processor


def run_model(
    model,
    processor,
    messages: list,
    chat_template: str,
    use_transformers: bool = False,
    temperature: float = 1e-2,
    top_p: float = 0.1,
    top_k: int = 1,
) -> str:
    if use_transformers:
        text = processor.apply_chat_template(
            messages, chat_template, add_generation_prompt=True, tokenize=False
        )
        audios, images, videos = process_mm_info(messages, use_audio_in_video=True)
        inputs = processor(
            text=text, audio=audios, images=images, videos=videos,
            return_tensors='pt', padding=True, use_audio_in_video=True,
        )
        inputs = inputs.to(model.device).to(model.dtype)
        text_ids, _ = model.generate(
            **inputs,
            thinker_return_dict_in_generate=True,
            thinker_max_new_tokens=8192,
            thinker_do_sample=False,
            speaker='Ethan',
            use_audio_in_video=True,
            return_audio=False,
        )
        response = processor.batch_decode(
            text_ids.sequences[:, inputs['input_ids'].shape[1]:],
            skip_special_tokens=True,
            clean_up_tokenization_spaces=False,
        )[0]
        return response
    else:
        from vllm import SamplingParams
        sampling_params = SamplingParams(
            temperature=temperature, top_p=top_p, top_k=top_k, max_tokens=8192
        )
        text = processor.apply_chat_template(
            messages, chat_template, tokenize=False, add_generation_prompt=True
        )
        audios, images, videos = process_mm_info(messages, use_audio_in_video=True)
        inputs = {
            'prompt': text,
            'multi_modal_data': {},
            'mm_processor_kwargs': {'use_audio_in_video': True},
        }
        if images is not None:
            inputs['multi_modal_data']['image'] = images
        if videos is not None:
            inputs['multi_modal_data']['video'] = videos
        if audios is not None:
            inputs['multi_modal_data']['audio'] = audios
        outputs = model.generate(inputs, sampling_params=sampling_params)
        return outputs[0].outputs[0].text


def _save_segment(
    audio_pcm: torch.Tensor,
    sample_rate: int,
    audio_path: str,
    start_time,
    end_time,
    tmp_dir: str,
) -> str:
    segment_pcm = audio_pcm[:, int(start_time * sample_rate):int(end_time * sample_rate)]
    filename = f'{Path(audio_path).stem}_{start_time}_{end_time}{Path(audio_path).suffix}'
    segment_path = os.path.join(tmp_dir, filename)
    os.makedirs(tmp_dir, exist_ok=True)
    torchaudio.save(segment_path, segment_pcm, sample_rate)
    return segment_path


def _build_initial_messages(audio_path: str, initial_user_text: str) -> list:
    return [
        {
            'role': 'user',
            'content': [
                {'type': 'audio', 'audio': audio_path},
                {'type': 'text', 'text': initial_user_text},
            ],
        }
    ]


def run_inference(
    model,
    processor,
    audio_path: str,
    tmp_dir: str,
    chat_template: str,
    initial_user_text: str,
    turn_user_text: str,
    use_transformers: bool = False,
    max_turns: int = 100,
    max_retries: int = 50,
) -> tuple[list, str | None]:
    audio_pcm, sample_rate = torchaudio.load(audio_path, normalize=False)
    messages = _build_initial_messages(audio_path, initial_user_text)

    box_pattern = re.compile(r'<box>\[\s*(\d+(?:\.\d+)?)\s*,\s*(\d+(?:\.\d+)?)\s*\]</box>')
    transcript_pattern = re.compile(
        r'(?:^|\n)([^\[\n]+?)\s*\[\s*(\d+(?:\.\d+)?)\s*,\s*(\d+(?:\.\d+)?)\s*\]\s*:\s*(.*)'
    )
    think_pattern = re.compile(r'<think>(.*?)</think>', re.DOTALL)
    answer_pattern = re.compile(r'<answer>(.*?)</answer>', re.DOTALL)

    answer = None
    last_start_time = None
    current_turn = 0
    response = ''

    while current_turn < max_turns:
        turn_success = False
        for attempt in range(max_retries):
            try:
                if attempt < 3:
                    temperature, top_p, top_k = 1e-2, 0.1, 1
                else:
                    increase = ((attempt - 3) // 3) * 0.1
                    temperature = min(0.1 + increase, 1.0)
                    top_p, top_k = 0.9, -1

                response = run_model(
                    model=model,
                    processor=processor,
                    messages=messages,
                    chat_template=chat_template,
                    temperature=temperature,
                    top_p=top_p,
                    top_k=top_k,
                    use_transformers=use_transformers,
                )

                assert not re.search(r'(.+?)\1{10,}', response.strip()), \
                    'LLM repeated output detected'

                answer_match = answer_pattern.search(response)
                if answer_match:
                    answer = answer_match.group(1)
                    messages.append({
                        'role': 'assistant',
                        'content': [{'type': 'text', 'text': response.strip()}],
                    })
                    turn_success = True
                    current_turn = max_turns + 1
                    break

                box_match = box_pattern.search(response)
                start_time = Decimal(box_match.group(1))
                end_time = Decimal(box_match.group(2))

                assert int(end_time * sample_rate) - audio_pcm.shape[1] <= 1600, \
                    f'end prediction {int(end_time * sample_rate)} exceeds audio length {audio_pcm.shape[1]}'
                assert int(start_time * sample_rate) <= audio_pcm.shape[1], \
                    f'start prediction {int(start_time * sample_rate)} exceeds audio length {audio_pcm.shape[1]}'
                assert end_time - start_time >= 0.1, \
                    f'segment too short: [{start_time}, {end_time}]'

                think_match = think_pattern.search(response)
                think = think_match.group(1)
                for _, t_start, t_end, _ in re.findall(transcript_pattern, think):
                    assert Decimal(t_end) - Decimal(t_start) >= 0.1, \
                        f'transcript segment too short: [{t_start}, {t_end}]'

                if last_start_time is not None:
                    assert start_time >= last_start_time, \
                        f'non-monotonic start time: {last_start_time} -> {start_time}'
                last_start_time = start_time

                messages.append({
                    'role': 'assistant',
                    'content': [{'type': 'text', 'text': response.strip()}],
                })
                segment_path = _save_segment(
                    audio_pcm, sample_rate, audio_path, start_time, end_time, tmp_dir
                )
                content = [{'type': 'audio', 'audio': segment_path}]
                turn_text = turn_user_text.format(turn=current_turn + 1)
                if turn_text:
                    content.append({'type': 'text', 'text': turn_text})
                messages.append({'role': 'user', 'content': content})

                turn_success = True
                current_turn += 1
                break
            except Exception as e:
                logger.warning('Turn %d, attempt %d: %s', current_turn, attempt, e)

        if not turn_success:
            if response:
                messages.append({
                    'role': 'assistant',
                    'content': [{'type': 'text', 'text': response.strip()}],
                })
            current_turn = max_turns + 1
            break

    return messages, answer


def main():
    parser = argparse.ArgumentParser(description='Speaker-Reasoner inference')
    parser.add_argument('--model', required=True, help='Path to the model')
    parser.add_argument('--audio', required=True, help='Path to the input audio file')
    parser.add_argument('--prompts', default='plugin/prompt_4194h.json',
                        help='Path to prompt JSON file')
    parser.add_argument('--tmp_dir', default='tmp',
                        help='Directory for temporary audio segment files')
    parser.add_argument('--use_transformers', action='store_true',
                        help='Use HuggingFace Transformers backend instead of vLLM')
    parser.add_argument('--no_flash_attn2', action='store_true',
                        help='Disable Flash Attention 2 (Transformers only)')
    parser.add_argument('--max_turns', type=int, default=100,
                        help='Maximum number of reasoning turns')
    parser.add_argument('--max_retries', type=int, default=50,
                        help='Maximum retries per turn on failure')
    args = parser.parse_args()

    with open(args.prompts, encoding='utf-8') as f:
        prompts = json.load(f)

    model, processor = _load_model_processor(
        model_path=args.model,
        use_transformers=args.use_transformers,
        use_flash_attn2=not args.no_flash_attn2,
    )

    messages, answer = run_inference(
        model=model,
        processor=processor,
        audio_path=args.audio,
        tmp_dir=args.tmp_dir,
        chat_template=prompts['chat_template'],
        initial_user_text=prompts['initial_user_text'],
        turn_user_text=prompts['turn_user_text'],
        use_transformers=args.use_transformers,
        max_turns=args.max_turns,
        max_retries=args.max_retries,
    )

    print(json.dumps(messages, indent=2, ensure_ascii=False))
    if answer:
        print(answer)


if __name__ == '__main__':
    main()
