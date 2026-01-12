# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import sys
from pathlib import Path

cur_dir = Path(__file__).resolve().parent
root_dir = cur_dir.parent
sys.path.append(str(root_dir))

from transition_detect.transnetv2 import TransNetV2Inference

test_dir = cur_dir / "test_files"

model = TransNetV2Inference()


def test_normal():
    video_path = test_dir / "demo.mp4"
    result = model(video_path)
    assert result.scenes == [[0, 93], [94, 185], [186, 264], [265, 387], [388, 629]]
