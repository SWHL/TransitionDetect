# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import ffmpeg
import numpy as np

from transnetv2_pytorch.transnetv2_pytorch import TransNetV2


def get_downsample(video_path):
    # 注意去掉了-r=fps
    video_stream, err = (
        ffmpeg.input(video_path.strip(), accurate_seek=None)  # 精确寻址
        .output(
            "pipe:",
            format="rawvideo",
            pix_fmt="rgb24",
            s="48x27",
            vsync=0,  # 不改变帧时序
            avoid_negative_ts="make_zero",  # 保持原始帧率模式
        )
        .run(quiet=True)
    )

    video_buffer = np.frombuffer(video_stream, np.uint8).reshape([-1, 27, 48, 3])
    return video_buffer


model = TransNetV2()
video_path = "tests/test_files/demo.mp4"


video_frames, single_frame_pred, all_frames_pred = model.predict_video(video_path)

single_frame_pred = single_frame_pred.numpy()
all_frames_pred = all_frames_pred.numpy()
predictions = np.stack([single_frame_pred, all_frames_pred], 1)
scenes = model.predictions_to_scenes(single_frame_pred)

print("ok")
