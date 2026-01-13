<div align="center">
  <div align="center">
    <h1><b>✂️🎬 Transition Detect</b></h1>
  </div>

<a href=""><img src="https://img.shields.io/badge/Python->=3.6-aff.svg"></a>
<a href=""><img src="https://img.shields.io/badge/OS-Linux%2C%20Win%2C%20Mac-pink.svg"></a>
<a href="https://github.com/SWHL/TransitionDetect/graphs/contributors"><img src="https://img.shields.io/github/contributors/SWHL/TransitionDetect?color=9ea"></a>
<a href="https://pepy.tech/project/transition_detect"><img src="https://static.pepy.tech/personalized-badge/transition_detect?period=total&units=abbreviation&left_color=grey&right_color=blue&left_text=Download"></a>
<a href="https://pypi.org/project/transition_detect/"><img alt="PyPI" src="https://img.shields.io/pypi/v/transition_detect"></a>
<a href="https://github.com/SWHL/TransitionDetect/stargazers"><img src="https://img.shields.io/github/stars/SWHL/TransitionDetect?color=ccf"></a>
<a href="https://semver.org/"><img alt="SemVer2.0" src="https://img.shields.io/badge/SemVer-2.0-brightgreen"></a>
<a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

</div>

## 简介

- 🎬 **智能转场检测**：使用 TransNetV2 深度学习模型自动检测视频中的场景转换点
- ✂️ **自动视频分割**：根据检测到的转场点自动将视频分割成多个场景片段
- 🚀 **易于使用**：提供命令行工具和 Python API 两种使用方式
- 💾 **自动模型下载**：首次使用时自动下载预训练模型
- 🖥️ **GPU/CPU 支持**：支持 CPU 和 GPU 推理，可根据环境自动选择

## 安装

### 从 PyPI 安装

```bash
pip install transition_detect
```

### 从源码安装

```bash
git clone https://github.com/SWHL/TransitionDetect.git
cd TransitionDetect
pip install -e .
```

## 依赖要求

- Python >= 3.6
- PyTorch
- ffmpeg-python
- 其他依赖见 [`requirements.txt`](./requirements.txt)

**注意**：使用前请确保系统已安装 [FFmpeg](https://ffmpeg.org/)。

## 使用方法

### 命令行使用

```bash
transition_detect <视频路径> [--save_clips_dir <输出目录>]
```

**参数说明**：

- `视频路径`：要处理的视频文件路径（必需）
- `--save_clips_dir`：保存分割后视频片段的目录（可选）

**示例**：

```bash
# 仅检测转场点，不保存视频片段
transition_detect video.mp4

# 检测转场点并保存分割后的视频片段
transition_detect video.mp4 --save_clips_dir ./outputs
```

### Python API 使用

```python
from pathlib import Path
from transition_detect.transnetv2 import TransNetV2Inference

# 初始化模型（pypi安装时，自带模型）
model = TransNetV2Inference()

# 检测转场点（不保存视频片段）
video_path = "video.mp4"
result = model(video_path)
print(result.scenes)  # 转场点列表
print(result.predictions)  # 预测结果

# 检测转场点并保存分割后的视频片段
output_dir = Path("outputs")
result = model(video_path, save_video_clips_dir=output_dir)
```

**返回结果说明**：

- `scenes`：转场点列表，格式为 `[[start_frame, end_frame], ...]`
- `predictions`：每帧的预测结果

### 使用 GPU

```python
# 指定 GPU ID（例如使用 GPU 0）
model = TransNetV2Inference(gpu_id=0)
```

## 示例

查看 `demo.py` 文件了解完整的使用示例：

```python
from pathlib import Path
from transition_detect.transnetv2 import TransNetV2Inference

model = TransNetV2Inference()

video_path = "tests/test_files/demo.mp4"
result = model(video_path, save_video_clips_dir="outputs")

print("检测到的场景数量:", len(result.scenes))
print("场景列表:", result.scenes)
```

## 项目结构

```text
TransitionDetect/
├── transition_detect/          # 主包目录
│   ├── main.py                 # 命令行入口
│   ├── config.yaml             # 配置文件
│   ├── transnetv2/             # TransNetV2 模型实现
│   │   ├── main.py             # 推理接口
│   │   ├── network.py          # 网络结构
│   │   └── typings.py         # 类型定义
│   └── utils/                  # 工具函数
│       ├── config.py           # 配置加载
│       ├── download_file.py    # 文件下载
│       ├── logger.py           # 日志工具
│       └── utils.py            # 通用工具
├── tests/                      # 测试文件
├── docs/                       # 文档
├── requirements.txt            # 依赖列表
└── setup.py                   # 安装配置
```

## 许可证

Apache-2.0 License

## 贡献者

<p align="left">
  <a href="https://github.com/SWHL/TransitionDetect/graphs/contributors">
    <img src="https://contrib.rocks/image?repo=SWHL/TransitionDetect&max=400&columns=10" width="5%"/>
  </a>
</p>

## 参考链接

- [TransNetV2](https://github.com/soCzech/TransNetV2)
- [transnetv2-pytorch](https://pypi.org/project/transnetv2-pytorch/)

## 致谢

本项目基于 TransNetV2 模型实现，感谢原作者的贡献。
