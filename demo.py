# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from pathlib import Path

from transition_detect.transnetv2.main import TransNetV2Inference

model = TransNetV2Inference()

video_path = "tests/test_files/demo.mp4"
result = model(video_path)

output_dir = Path("outputs")
model.extract_video_clips_by_frames(video_path, result.scenes, output_dir)
