# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class TransnetOutput:
    scenes: Optional[List[List[int]]] = None
    predictions: Optional[List[List[float]]] = None
