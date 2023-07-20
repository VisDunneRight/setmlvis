// Copyright (c) {{ cookiecutter.author_name }}
// Distributed under the terms of the Modified BSD License.

import {
  DOMWidgetModel,
  DOMWidgetView
} from '@jupyter-widgets/base';
import type {  ISerializers} from '@jupyter-widgets/base';
import { setStoreModels } from './stores';

import { MODULE_NAME, MODULE_VERSION } from './version';

import Widget from './components/Widget.svelte'

export class SetMLVisModel extends DOMWidgetModel {
  //These are the defaults used when excuting the model
  // Any variables add to widget.py should also be added here
  defaults() {
    return {
      ...super.defaults(),
      _model_name: SetMLVisModel.model_name,
      _model_module: SetMLVisModel.model_module,
      _model_module_version: SetMLVisModel.model_module_version,
      _view_name: SetMLVisModel.view_name,
      _view_module: SetMLVisModel.view_module,
      _view_module_version: SetMLVisModel.view_module_version,
      data: {},
      num_instance: 0,
      height: 800,
      IOU:0.8,
    };
  }

  static serializers: ISerializers = {
    ...DOMWidgetModel.serializers,
    // Add any extra serializers here
  };

  static model_name = 'SetMLVisModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'SetMLVisView'; // Set to null if no view
  static view_module = MODULE_NAME; // Set to null if no view
  static view_module_version = MODULE_VERSION;
}

export class SetMLVisView extends DOMWidgetView {
  render() {
    setStoreModels(this.model);
    new Widget({ target: this.el });
  }
}