# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from pathlib import Path

from transition_detect.transnetv2.main import TransNetV2Inference
from transition_detect.utils.utils import get_downsample, mkdir, trim_video_by_frames

model_path = "transition_detect/models/transnetv2-pytorch-weights.pth"
model = TransNetV2Inference(model_path)

video_path = "tests/test_files/demo.mp4"
video_buffer = get_downsample(video_path)
result = model(video_buffer)

scenes = result["scenes"]

save_dir = Path("outputs") / Path(video_path).stem
mkdir(save_dir)

for start_frame, end_frame in scenes:
    save_video_path = save_dir / f"{start_frame}_{end_frame}.mp4"
    trim_video_by_frames(video_path, save_video_path, start_frame, end_frame)
