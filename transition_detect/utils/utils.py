# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import hashlib
import subprocess
from pathlib import Path
from typing import Union


def get_file_sha256(file_path: Union[str, Path], chunk_size: int = 65536) -> str:
    with open(file_path, "rb") as file:
        sha_signature = hashlib.sha256()
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            sha_signature.update(chunk)

    return sha_signature.hexdigest()


def mkdir(dir_path):
    Path(dir_path).mkdir(parents=True, exist_ok=True)


def trim_video_by_frames(
    video_path: Union[str, Path],
    output_path: Union[str, Path],
    start_frame: int,
    end_frame: int,
    verbose: bool = False,
) -> str:
    """
    从视频中精确提取指定帧范围 [start_frame, end_frame) 的片段，
    并同步裁剪音频（如有），输出为 H.264 + AAC 的 MP4 视频。
    Args:
        video_path: 输入视频路径
        output_path: 输出视频路径
        start_frame: 起始帧（包含）
        end_frame: 结束帧（不包含）
        verbose: 是否显示 FFmpeg 日志
    """
    video_path = Path(video_path)
    output_path = Path(output_path)

    # 获取视频帧率（用于计算时长）
    ffprobe_cmd = [
        "ffprobe",
        "-v",
        "quiet",
        "-select_streams",
        "v:0",
        "-show_entries",
        "stream=avg_frame_rate",
        "-of",
        "csv=p=0",
        str(video_path),
    ]
    result = subprocess.run(ffprobe_cmd, capture_output=True, text=True, check=True)
    avg_frame_rate = result.stdout.strip()

    if not avg_frame_rate or avg_frame_rate == "N/A":
        raise ValueError(f"无法获取视频帧率: {video_path}")

    # 解析帧率（如 "30/1" 或 "2997/100"）
    try:
        if "/" in avg_frame_rate:
            num, den = map(int, avg_frame_rate.split("/"))
            fps = num / den
        else:
            fps = float(avg_frame_rate)
    except Exception as e:
        raise ValueError(f"无效的帧率格式 '{avg_frame_rate}': {e}")

    total_frames = end_frame - start_frame
    if total_frames <= 0:
        raise ValueError("end_frame 必须大于 start_frame")

    start_time = start_frame / fps
    duration = total_frames / fps

    command = ["ffmpeg", "-i", str(video_path)]

    vf = f"trim=start_frame={start_frame}:end_frame={end_frame},setpts=PTS-STARTPTS"
    command.extend(["-vf", vf])

    af = f"atrim=start={start_time}:duration={duration},asetpts=PTS-STARTPTS"
    command.extend(["-af", af])

    command.extend(["-frames:v", str(total_frames)])

    command.extend(
        [
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",  # 音频转为 AAC（兼容性好）
            "-b:a",
            "128k",  # 音频码率
        ]
    )

    if not verbose:
        command.extend(["-loglevel", "quiet"])

    command.extend(["-y", str(output_path)])

    subprocess.run(command, check=True)
    return str(output_path)
