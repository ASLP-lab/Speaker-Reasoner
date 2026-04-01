<h1 align="center">Speaker-Reasoner: Scaling Interaction Turns and Reasoning Patterns for Timestamped Speaker-Attributed ASR</h1>

<div align="center">

<div style="text-align: center;">
  <img src="https://img.shields.io/badge/Python-3.10+-blue" alt="Python">
  <img src="https://img.shields.io/badge/License-Apache%202.0-green" alt="License">
  <a href="https://arxiv.org/abs/TODO">
    <img src="https://img.shields.io/badge/arXiv-paper-red" alt="arXiv Paper">
  </a>
  <a href="https://github.com/ASLP-lab/Speaker-Reasoner">
    <img src="https://img.shields.io/badge/GitHub-repo-black" alt="GitHub">
  </a>
  <a href="http://www.npu-aslp.org/">
    <img src="https://img.shields.io/badge/🏫-ASLP-grey?labelColor=lightgrey" alt="lab">
  </a>
</div>

</div>

<div align="center">
  <h3>
    Zhennan Lin<sup>1</sup>, Shuai Wang<sup>2</sup>, Zhaokai Sun<sup>1</sup>, Pengyuan Xie<sup>3</sup>, Chuan Xie<sup>3</sup>, Jie Liu<sup>3</sup>, Qiang Zhang<sup>3</sup>, Lei Xie<sup>1†</sup>
  </h3>

  <p>
    <sup>†</sup>Corresponding author
  </p>

  <p>
    <sup>1</sup>Audio, Speech and Language Processing Group (ASLP@NPU), Northwestern Polytechnical University<br>
    <sup>2</sup>School of Intelligence Science and Technology, Nanjing University<br>
    <sup>3</sup>Shanghai Lingguang Zhaxian Technology
  </p>
</div>

----

Speaker-Reasoner is an end-to-end Speech LLM for **timestamped speaker-attributed ASR** featuring agentic multi-turn temporal reasoning. Instead of single-pass inference, the model iteratively analyzes global audio structure, autonomously predicts temporal boundaries, and performs fine-grained segment analysis, jointly modeling speaker identity, gender, timestamps, and transcription. A speaker-aware cache further extends processing to audio exceeding the training context window.

![](figs/speaker_reasoner.png)

## 🌟 Highlights

- **Agentic multi-turn reasoning**: iterative global-to-local inference along the temporal axis — global speaker summary → boundary prediction → fine-grained segment decoding
- **Speaker-aware context cache**: extends processing to long-form audio beyond the training context window while preserving speaker consistency across chunks
- **Three-stage progressive training**: multi-task foundation → temporal interaction learning → cache-conditioned decoding
- **State-of-the-art performance**: outperforms strong baselines including closed-source Gemini-2.5-Pro on AliMeeting and AISHELL-4

## 📊 Results

### Segmented Evaluation (40–50s segments)

| Model | AISHELL4-Eval DER↓ | AISHELL4-Eval CER↓ | AISHELL4-Eval cpCER↓ | AISHELL4-Eval ∆cp↓ | Alimeeting-Far DER↓ | Alimeeting-Far CER↓ | Alimeeting-Far cpCER↓ | Alimeeting-Far ∆cp↓ |
|---|---|---|---|---|---|---|---|---|
| **Cascade Baselines** | | | | | | | | |
| Pyannote3.1 + Paraformer | 8.10 | 19.18 | 26.24 | 7.06 | 19.13 | 30.15 | 45.39 | 15.24 |
| **End-to-End Baselines** | | | | | | | | |
| Gemini-2.5-Pro† | 36.07 | 19.81 | 25.11 | 5.30 | 56.39 | 30.16 | 39.29 | 9.13 |
| Qwen3-Omni-30B-A3B-Instruct | 32.42 | 14.46 | 22.22 | 7.76 | 37.15 | 25.40 | 36.28 | 10.88 |
| Qwen2.5-Omni-7B | 85.68 | 33.37 | 60.45 | 27.08 | 91.77 | 38.13 | 73.38 | 35.25 |
| SpeakerLM (212.25h) | – | 17.75 | 26.14 | 8.39 | – | 18.63 | 32.22 | 13.59 |
| SpeakerLM (7638.95h) | – | 17.17 | 18.37 | 1.20 | – | 13.97 | 16.05 | 2.08 |
| VibeVoice-ASR | 10.88 | 22.30 | 26.30 | 4.00 | 20.70 | 34.67 | 40.54 | 5.87 |
| TagSpeech-Alimeeting | 37.51 | 35.70 | 53.44 | 17.74 | 52.46 | 47.11 | 68.74 | 21.63 |
| **Ours** | | | | | | | | |
| Qwen3-Omni + SOT sft (Stage 1) | – | 17.65 | 19.59 | 1.94 | – | 24.24 | 26.03 | 1.79 |
| Speaker-Reasoner Base (Stage 1) | 6.24 | 14.04 | 16.54 | 2.50 | 8.96 | 21.16 | 22.64 | 1.48 |
| Speaker-Reasoner Multi-turn (Stage 2) | 5.19 | 13.83 | 14.93 | 1.10 | 7.47 | 20.34 | 20.29 | −0.05 |
| **Speaker-Reasoner Multi-turn w/ SAC (Stage 3)** | **5.26** | **13.83** | **14.73** | **0.90** | **7.34** | **20.57** | **20.43** | **−0.14** |
| Speaker-Reasoner Base 7B | 12.00 | 15.65 | 25.60 | 9.95 | 18.43 | 24.97 | 38.12 | 13.15 |
| Speaker-Reasoner Multi-turn 7B | 9.38 | 15.31 | 22.91 | 7.60 | 15.56 | 24.33 | 34.81 | 10.48 |

† Closed-source model. DER unavailable for SpeakerLM and SOT-based models due to incompatible output formats.

### Long-form Evaluation (without segmentation)

| Model | AISHELL4-Eval DER↓ | AISHELL4-Eval cpCER↓ |
|---|---|---|
| Gemini-2.5-Pro | 15.32 | 31.59 |
| Speaker-Reasoner Multi-turn w/ SAC | 21.60 | 36.20 |

### Speaker Attribute Evaluation (AISHELL4-Eval)

| Model | Gender ACC↑ | Speaker Count ACC (SCA)↑ |
|---|---|---|
| Gemini-2.5-Pro | 94.80 | 67.03 |
| Qwen3-Omni-30B-A3B-Instruct | 97.12 | 60.49 |
| Speaker-Reasoner Multi-turn | **96.80** | **69.03** |

## Installation

### Environment Setup

```bash
git clone https://github.com/ASLP-lab/Speaker-Reasoner.git
cd Speaker-Reasoner

conda create -n speaker-reasoner python=3.10 -y
conda activate speaker-reasoner
```

Install MS-Swift and dependencies:

```bash
pip install ms-swift
```

## Model Download

Coming soon.

## Training

Coming soon.

## Inference

Coming soon.

## Citation

If you find this work useful, please cite:

```bibtex

```

## License

The code in this repository is released under the **Apache 2.0 License**.

## Contact

- **Issues**: Please open a GitHub Issue for bug reports or suggestions.
- **Email**: znlin@mail.nwpu.edu.cn, lxie@nwpu.edu.cn

<p align="center">
    <a href="http://www.nwpu-aslp.org/">
        <img src="figs/aslp.png" width="400"/>
    </a>
</p>