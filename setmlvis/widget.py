#!/usr/bin/env python
# coding: utf-8

# Copyright (c) {{ cookiecutter.author_name }}.
# Distributed under the terms of the Modified BSD License.

"""
TODO: Add module docstring
"""

from ipywidgets import DOMWidget
from traitlets import Unicode, Int, Float, Dict
from typing import Union
from pathlib import Path
import json
from ._frontend import module_name, module_version


class SetMLVisWidget(DOMWidget):
    """TODO: Add docstring here
    """
    _model_name = Unicode('SetMLVisModel').tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_name = Unicode('SetMLVisView').tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)

    dataset = Dict({}).tag(sync=True)

    num_instances = Int(0).tag(sync=True)
    IOU = Float(0.8).tag(sync=True)
    height = Int(800).tag(sync=True)
    # selectedCol = List([]).tag(sync=True)
    selectedImgs = Dict({}).tag(sync=True)
    def __init__(
        self,
        data: Union[str, Path, dict],
        height: int = 800,
        IOU: float = 0.8,
        **kwargs,
    ):
        super().__init__(**kwargs)

        # if data is a path or string, then read the file at that path
        # if isinstance(data, Path) or isinstance(data, str):
        #     path = Path(data).resolve()

        #     if not path.exists():
        #         raise OSError(f"Cannot read {path}")

        #     json_data = path.read_text(encoding="utf-8")
        #     data = json.loads(json_data)


        # synced widget state
        self.dataset = data
        self.num_instances = 10
        self.height = height
        self.IOU = IOU