# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from pathlib import Path

import yaml

cur_dir = Path(__file__).resolve().parent
root_dir = cur_dir.parent

config_path = root_dir / "config.yaml"
with open(config_path, "rb") as f:
    cfg = yaml.load(f, Loader=yaml.Loader)
