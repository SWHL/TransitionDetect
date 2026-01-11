# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from typing import Optional

import numpy as np
import torch

from .network import TransNetV2


class TransNetV2Inference:
    def __init__(self, model_path: str, gpu_id: Optional[int] = None):
        self.model = TransNetV2()
        self.model.load_state_dict(torch.load(model_path))

        device = self.get_device(gpu_id)
        self.model.to(device)

    def get_device(self, gpu_id: Optional[int] = None):
        if gpu_id is None:
            device = torch.device("cpu")
            return device

        device = torch.device("cpu")
        if torch.cuda.is_available():
            device = torch.device(f"cuda:{gpu_id}")
        return device

    def __call__(self, video: np.ndarray):
        single_frame_predictions, all_frame_predictions = self.model.predict_frames(
            video
        )

        predictions = np.stack([single_frame_predictions, all_frame_predictions], 1)
        scenes = self.model.predictions_to_scenes(single_frame_predictions)
        return {
            "scenes": scenes.tolist(),
            "predictions": predictions.tolist(),
        }
