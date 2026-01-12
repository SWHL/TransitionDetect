# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from pathlib import Path

from transition_detect.transnetv2 import TransNetV2Inference

model = TransNetV2Inference()

video_path = "tests/test_files/demo.mp4"
output_dir = Path("outputs")
result = model(video_path, save_video_clips_dir=output_dir)

print("ok")
