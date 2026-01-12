# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import argparse
from pathlib import Path

from .transnetv2 import TransNetV2Inference


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("video_path", type=Path)
    parser.add_argument("--save_clips_dir", type=str, default=None)
    args = parser.parse_args()

    video_path = args.video_path
    save_clips_dir = args.save_clips_dir

    model = TransNetV2Inference()

    result = model(video_path, save_video_clips_dir=save_clips_dir)
    print(result)


if __name__ == "__main__":
    main()
