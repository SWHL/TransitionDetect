# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from pathlib import Path
from typing import List, Optional, Union

import ffmpeg
import numpy as np
import torch
from tqdm import tqdm

from ..utils.config import cfg
from ..utils.download_file import DownloadFile, DownloadFileInput
from ..utils.logger import logger
from ..utils.utils import mkdir, trim_video_by_frames
from .network import TransNetV2
from .typings import TransnetOutput


class TransNetV2Inference:
    def __init__(
        self, model_path: Union[str, Path, None] = None, gpu_id: Optional[int] = None
    ):
        if model_path is None:
            default_model_dir = self.build_model_dir()
            model_path = self.get_or_download_default_model(default_model_dir)

        self.model = TransNetV2()
        self.model.load_state_dict(torch.load(str(model_path)))

        device = self.get_device(gpu_id)
        self.model.to(device)

    def __call__(self, video_path: Union[str, Path]):
        try:
            video_buffer = self.resize_video(video_path)
        except Exception as e:
            logger.exception(f"Try to resize video to adapt size meets error.")
            return TransnetOutput()

        try:
            scenes, predictions = self.run_infer(video_buffer)
        except Exception as e:
            logger.exception("Model Inference error.")
            return TransnetOutput()

        return TransnetOutput(scenes=scenes, predictions=predictions)

    def get_device(self, gpu_id: Optional[int] = None):
        if gpu_id is None:
            device = torch.device("cpu")
            logger.info("Using CPU device")
            return device

        device = torch.device("cpu")
        if torch.cuda.is_available():
            device = torch.device(f"cuda:{gpu_id}")
            logger.info(f"Using GPU: cuda:{gpu_id}")
        return device

    def get_or_download_default_model(self, default_model_dir: Path) -> str:
        model_url = cfg["transnetv2"]["model_path_or_url"]
        model_sha256 = cfg["transnetv2"]["SHA256"]
        model_path = default_model_dir / "transnetv2-pytorch-weights.pth"
        download_params = DownloadFileInput(
            file_url=model_url,
            save_path=model_path,
            logger=logger,
            sha256=model_sha256,
        )
        DownloadFile.run(download_params)
        return str(model_path)

    @staticmethod
    def resize_video(video_path: Union[str, Path]) -> np.ndarray:
        video_path = str(video_path)

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

    def run_infer(self, video_buffer: np.ndarray):
        single_frame_preds, all_frame_preds = self.model.predict_frames(video_buffer)
        predictions = np.stack([single_frame_preds, all_frame_preds], 1)
        scenes = self.model.predictions_to_scenes(single_frame_preds)
        return scenes.tolist(), predictions.tolist()

    @staticmethod
    def extract_video_clips_by_frames(
        video_path: Union[str, Path],
        frame_ranges: Optional[List[List[int]]],
        output_dir: Union[str, Path],
    ):
        if frame_ranges is None:
            raise ValueError("Frame indexes is empty")

        video_path = Path(video_path)
        output_dir = Path(output_dir)

        save_video_dir = output_dir / Path(video_path).stem
        mkdir(save_video_dir)

        for start_frame, end_frame in tqdm(frame_ranges, desc="extract video clips"):
            save_video_path = save_video_dir / f"{start_frame}_{end_frame}.mp4"
            trim_video_by_frames(video_path, save_video_path, start_frame, end_frame)

        logger.info(f"All video clips had saved {save_video_dir.resolve()}")

    @staticmethod
    def build_model_dir() -> Path:
        cur_dir = Path(__file__).resolve().parent
        root_dir = cur_dir.parent
        default_model_dir = root_dir / "models"
        mkdir(default_model_dir)
        return default_model_dir


class TransNetV2InferenceError(Exception):
    pass
