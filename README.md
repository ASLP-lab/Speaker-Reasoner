<h1 align="center">Speaker-Reasoner: Scaling Interaction Turns and Reasoning Patterns for Timestamped Speaker-Attributed ASR</h1>

<div align="center">

<div style="text-align: center;">
  <img src="https://img.shields.io/badge/Python-3.10+-blue" alt="Python">
  <img src="https://img.shields.io/badge/License-Apache%202.0-green" alt="License">
  <a href="https://aslp-lab.github.io/Speaker-Reasoner-Demo/">
    <img src="https://img.shields.io/badge/Demo-page-blue" alt="Demo">
  </a>
  <a href="https://arxiv.org/abs/2604.03074">
    <img src="https://img.shields.io/badge/arXiv-paper-red" alt="arXiv Paper">
  </a>
  <a href="https://huggingface.co/collections/ASLP-lab/speaker-reasoner">
    <img src="https://img.shields.io/badge/HuggingFace-Models-ffd21e" alt="HuggingFace">
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

## 🎬 Demo Video

<div align="center">
  <video src="https://github.com/ASLP-lab/Speaker-Reasoner/raw/main/figs/Demo-video.mp4" controls width="80%"></video>
</div>

## 📖 Introduction

Speaker-Reasoner is an end-to-end Speech LLM for **timestamped speaker-attributed ASR** featuring agentic multi-turn temporal reasoning. Instead of single-pass inference, the model iteratively analyzes global audio structure, autonomously predicts temporal boundaries, and performs fine-grained segment analysis, jointly modeling speaker identity, gender, timestamps, and transcription. A speaker-aware cache further extends processing to audio exceeding the training context window.

![](figs/speaker_reasoner.png)

## 🌟 Highlights

- **Agentic multi-turn reasoning**: iterative global-to-local inference along the temporal axis — global speaker summary → boundary prediction → fine-grained segment decoding
- **Speaker-aware context cache**: extends processing to long-form audio beyond the training context window while preserving speaker consistency across chunks
- **Three-stage progressive training**: multi-task foundation → temporal interaction learning → cache-conditioned decoding
- **State-of-the-art performance**: outperforms strong baselines including closed-source Gemini-2.5-Pro on AliMeeting and AISHELL-4
- 🔥 **Bilingual & Scaled up**: extended training on 4,194 hours of multi-domain data, natively supporting English and Mandarin across complex multi-speaker scenarios

## 📊 Results

### Comprehensive Multi-Domain Evaluation

<p>We further scaled up Speaker-Reasoner with 4,194 hours of bilingual (ZH/EN) training data. The model demonstrates superior performance across diverse scenarios, including challenging video domains and various public meeting datasets.</p>

<div style="overflow-x: auto;">
<table style="white-space: nowrap;">
  <thead>
    <tr>
      <th rowspan="2">Model</th>
      <th colspan="4" align="center">Video-Internal-Eval</th>
      <th colspan="4" align="center">Video-Internal-Eval-zh</th>
      <th colspan="4" align="center">Video-Internal-Eval-en</th>
      <th colspan="4" align="center">AISHELL4-Eval</th>
      <th colspan="4" align="center">Alimeeting-Far</th>
      <th colspan="4" align="center">AMI-SDM</th>
      <th colspan="4" align="center">MLC-SLM-Eval-1</th>
      <th colspan="4" align="center">MLC-SLM-Eval-2</th>
    </tr>
    <tr>
      <th>WER↓</th><th>cpWER↓</th><th>DER↓</th><th>∆cp↓</th>
      <th>WER↓</th><th>cpWER↓</th><th>DER↓</th><th>∆cp↓</th>
      <th>WER↓</th><th>cpWER↓</th><th>DER↓</th><th>∆cp↓</th>
      <th>WER↓</th><th>cpWER↓</th><th>DER↓</th><th>∆cp↓</th>
      <th>WER↓</th><th>cpWER↓</th><th>DER↓</th><th>∆cp↓</th>
      <th>WER↓</th><th>cpWER↓</th><th>DER↓</th><th>∆cp↓</th>
      <th>WER↓</th><th>cpWER↓</th><th>DER↓</th><th>∆cp↓</th>
      <th>WER↓</th><th>cpWER↓</th><th>DER↓</th><th>∆cp↓</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Gemini-2.5-Pro</td>
      <td>22.47</td><td>44.13</td><td>74.05</td><td>21.66</td>
      <td>18.28</td><td>40.97</td><td>69.35</td><td>22.69</td>
      <td>55.40</td><td>68.82</td><td>100.95</td><td>13.42</td>
      <td>19.81</td><td>25.11</td><td>36.07</td><td>5.30</td>
      <td>30.16</td><td>39.29</td><td>56.39</td><td>9.13</td>
      <td>31.66</td><td>39.98</td><td>50.28</td><td>8.32</td>
      <td>36.87</td><td>41.88</td><td>42.33</td><td>5.01</td>
      <td>26.73</td><td>32.19</td><td>46.19</td><td>5.46</td>
    </tr>
    <tr>
      <td>VibeVoice-ASR</td>
      <td>16.45</td><td>58.60</td><td>47.18</td><td>42.15</td>
      <td>17.70</td><td>62.06</td><td>47.65</td><td>44.36</td>
      <td>7.11</td><td>32.65</td><td>44.62</td><td>25.54</td>
      <td>22.19</td><td>26.16</td><td>8.94</td><td>3.97</td>
      <td>34.31</td><td>39.92</td><td>19.62</td><td>5.61</td>
      <td>30.53</td><td>35.86</td><td>21.00</td><td>5.33</td>
      <td>10.30</td><td>13.45</td><td>6.27</td><td>3.15</td>
      <td><b>7.97</b></td><td><b>11.38</b></td><td><b>3.14</b></td><td>3.41</td>
    </tr>
    <tr>
      <td><b>Speaker-Reasoner Multi-turn</b></td>
      <td><b>6.27</b></td><td><b>24.43</b></td><td><b>15.33</b></td><td><b>18.16</b></td>
      <td><b>6.50</b></td><td><b>25.81</b></td><td><b>16.68</b></td><td><b>19.31</b></td>
      <td><b>4.42</b></td><td><b>16.31</b></td><td><b>7.58</b></td><td><b>11.89</b></td>
      <td><b>7.13</b></td><td><b>8.14</b></td><td><b>3.38</b></td><td><b>1.01</b></td>
      <td><b>19.72</b></td><td><b>19.92</b></td><td><b>6.70</b></td><td><b>0.20</b></td>
      <td><b>23.29</b></td><td><b>25.16</b></td><td><b>13.56</b></td><td><b>1.87</b></td>
      <td><b>9.17</b></td><td><b>11.74</b></td><td><b>4.76</b></td><td><b>2.57</b></td>
      <td>8.54</td><td>11.76</td><td>4.35</td><td><b>3.22</b></td>
    </tr>
  </tbody>
</table>
</div>

### Segmented Evaluation (40–50s segments)

<div style="overflow-x: auto;">
<table style="white-space: nowrap;">
  <thead>
    <tr>
      <th rowspan="2">Model</th>
      <th colspan="4" align="center">AISHELL4-Eval</th>
      <th colspan="4" align="center">Alimeeting-Far</th>
    </tr>
    <tr>
      <th>DER↓</th><th>CER↓</th><th>cpCER↓</th><th>∆cp↓</th>
      <th>DER↓</th><th>CER↓</th><th>cpCER↓</th><th>∆cp↓</th>
    </tr>
  </thead>
  <tbody>
    <tr><td colspan="9"><b>Cascade Baselines</b></td></tr>
    <tr><td>Pyannote3.1 + Paraformer</td><td>8.10</td><td>19.18</td><td>26.24</td><td>7.06</td><td>19.13</td><td>30.15</td><td>45.39</td><td>15.24</td></tr>
    <tr><td colspan="9"><b>End-to-End Baselines</b></td></tr>
    <tr><td>Gemini-2.5-Pro†</td><td>36.07</td><td>19.81</td><td>25.11</td><td>5.30</td><td>56.39</td><td>30.16</td><td>39.29</td><td>9.13</td></tr>
    <tr><td>Qwen3-Omni-30B-A3B-Instruct</td><td>32.42</td><td>14.46</td><td>22.22</td><td>7.76</td><td>37.15</td><td>25.40</td><td>36.28</td><td>10.88</td></tr>
    <tr><td>Qwen2.5-Omni-7B</td><td>85.68</td><td>33.37</td><td>60.45</td><td>27.08</td><td>91.77</td><td>38.13</td><td>73.38</td><td>35.25</td></tr>
    <tr><td>SpeakerLM (212.25h)</td><td>–</td><td>17.75</td><td>26.14</td><td>8.39</td><td>–</td><td>18.63</td><td>32.22</td><td>13.59</td></tr>
    <tr><td>SpeakerLM (7638.95h)</td><td>–</td><td>17.17</td><td>18.37</td><td>1.20</td><td>–</td><td>13.97</td><td>16.05</td><td>2.08</td></tr>
    <tr><td>VibeVoice-ASR</td><td>10.88</td><td>22.30</td><td>26.30</td><td>4.00</td><td>20.70</td><td>34.67</td><td>40.54</td><td>5.87</td></tr>
    <tr><td>TagSpeech-Alimeeting</td><td>37.51</td><td>35.70</td><td>53.44</td><td>17.74</td><td>52.46</td><td>47.11</td><td>68.74</td><td>21.63</td></tr>
    <tr><td colspan="9"><b>Ours</b></td></tr>
    <tr><td>Qwen3-Omni + SOT sft (Stage 1)</td><td>–</td><td>17.65</td><td>19.59</td><td>1.94</td><td>–</td><td>24.24</td><td>26.03</td><td>1.79</td></tr>
    <tr><td>Speaker-Reasoner Base (Stage 1)</td><td>6.24</td><td>14.04</td><td>16.54</td><td>2.50</td><td>8.96</td><td>21.16</td><td>22.64</td><td>1.48</td></tr>
    <tr><td>Speaker-Reasoner Multi-turn (Stage 2)</td><td>5.19</td><td>13.83</td><td>14.93</td><td>1.10</td><td>7.47</td><td>20.34</td><td>20.29</td><td>−0.05</td></tr>
    <tr><td><b>Speaker-Reasoner Multi-turn w/ SAC (Stage 3)</b></td><td><b>5.26</b></td><td><b>13.83</b></td><td><b>14.73</b></td><td><b>0.90</b></td><td><b>7.34</b></td><td><b>20.57</b></td><td><b>20.43</b></td><td><b>−0.14</b></td></tr>
    <tr><td>Speaker-Reasoner Base 7B</td><td>12.00</td><td>15.65</td><td>25.60</td><td>9.95</td><td>18.43</td><td>24.97</td><td>38.12</td><td>13.15</td></tr>
    <tr><td>Speaker-Reasoner Multi-turn 7B</td><td>9.38</td><td>15.31</td><td>22.91</td><td>7.60</td><td>15.56</td><td>24.33</td><td>34.81</td><td>10.48</td></tr>
  </tbody>
</table>
</div>

† Closed-source model. DER unavailable for SpeakerLM and SOT-based models due to incompatible output formats.

### Long-form Evaluation (without segmentation)

<div style="overflow-x: auto;">
<table style="white-space: nowrap;">
  <thead>
    <tr>
      <th>Model</th>
      <th>AISHELL4-Eval DER↓</th>
      <th>AISHELL4-Eval cpCER↓</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Gemini-2.5-Pro</td><td>15.32</td><td>31.59</td></tr>
    <tr><td>Speaker-Reasoner Multi-turn w/ SAC</td><td>21.60</td><td>36.20</td></tr>
  </tbody>
</table>
</div>

### Speaker Attribute Evaluation (AISHELL4-Eval)

<div style="overflow-x: auto;">
<table style="white-space: nowrap;">
  <thead>
    <tr>
      <th>Model</th>
      <th>Gender ACC↑</th>
      <th>Speaker Count ACC (SCA)↑</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Gemini-2.5-Pro</td><td>94.80</td><td>67.03</td></tr>
    <tr><td>Qwen3-Omni-30B-A3B-Instruct</td><td>97.12</td><td>60.49</td></tr>
    <tr><td>Speaker-Reasoner Multi-turn</td><td><b>96.80</b></td><td><b>69.03</b></td></tr>
  </tbody>
</table>
</div>

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

We provide the pre-trained model weights on Hugging Face. You can download the corresponding versions based on your requirements:

| Model Version | Description | Language | Download |
| :--- | :--- | :---: | :---: |
| **Speaker-Reasoner** | The standard multi-turn model evaluated in the main paper. | ZH | [🤗 Hugging Face](https://huggingface.co/ASLP-lab/Speaker-Reasoner) |
| **Speaker-Reasoner-4194h** | Scaled-up version trained on 4,194 hours of multi-domain data. | ZH/EN | [🤗 Hugging Face](https://huggingface.co/ASLP-lab/Speaker-Reasoner-4194h) |

## Training

Coming soon.

## Inference

### vLLM

Speaker-Reasoner is built on top of [Qwen3-Omni-30B-A3B-Instruct](https://huggingface.co/Qwen/Qwen3-Omni-30B-A3B-Instruct). To run it, you will need to install a custom branch of vLLM from source.

```bash
git clone -b qwen3_omni https://github.com/wangxiongts/vllm.git
cd vllm
pip install -r requirements/build.txt
pip install -r requirements/cuda.txt
export VLLM_PRECOMPILED_WHEEL_LOCATION=https://wheels.vllm.ai/a5dd03c1ebc5e4f56f3c9d3dc0436e9c582c978f/vllm-0.9.2-cp38-abi3-manylinux1_x86_64.whl
VLLM_USE_PRECOMPILED=1 pip install -e . -v --no-build-isolation
# If you meet an "Undefined symbol" error while using VLLM_USE_PRECOMPILED=1, please use "pip install -e . -v" to build from source.
# Install the Transformers
pip install git+https://github.com/huggingface/transformers
pip install accelerate
pip install qwen-omni-utils -U
pip install -U flash-attn --no-build-isolation
```

> For more details on compiling vLLM from source, refer to the [vLLM official documentation](https://docs.vllm.ai/en/latest/getting_started/installation/gpu.html#set-up-using-python-only-build-without-compilation).

## Citation

If you find this work useful, please cite:

```bibtex
@article{lin2026speakerreasoner,
  title={Speaker-Reasoner: Scaling Interaction Turns and Reasoning Patterns for Timestamped Speaker-Attributed ASR}, 
  author={Zhennan Lin and Shuai Wang and Zhaokai Sun and Pengyuan Xie and Chuan Xie and Jie Liu and Qiang Zhang and Lei Xie},
  year={2026},
  eprint={2604.03074},
  archivePrefix={arXiv},
  primaryClass={eess.AS},
  url={https://arxiv.org/abs/2604.03074}, 
}
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
