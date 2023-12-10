import type { Writable } from 'svelte/store';
import type { DOMWidgetModel } from '@jupyter-widgets/base';

import { writable } from 'svelte/store';
import type { Data, ImgData, StringNumMap, ImgBoxes } from './types';

// //boilerplate code that will be ignored for now
// interface WidgetWritable<T> extends Writable<T> {
//   setModel: (m: DOMWidgetModel) => void;
// }

// export function WidgetWritable<T>(name_: string, value_: T): WidgetWritable<T> {
//   const name: string = name_;
//   const internalWritable: Writable<any> = writable(value_);
//   let model: DOMWidgetModel;

//   return {
//     set: (v: any) => {
//       internalWritable.set(v);
//       if (model) {
//         model.set(name, v);
//         model.save_changes();
//       }
//     },
//     subscribe: internalWritable.subscribe,
//     update: (func: any) => {
//       internalWritable.update((v: any) => {
//         const output = func(v);
//         if (model) {
//           model.set(name, output);
//           model.save_changes();
//         }
//         return output;
//       })
//     },
//     setModel: (m: DOMWidgetModel) => {
//       model = m;
//       const modelValue = model.get(name);
//       if (modelValue) internalWritable.set(modelValue)
//       model.on('change:' + name, () => internalWritable.set(model.get(name)), null)
//     }
//   }
// }

function createSyncedWidget<T>(
  name_: string,
  value_: T,
  model: DOMWidgetModel
): Writable<T> {
  const name: string = name_;
  const internalWritable: Writable<T> = writable(value_);

  // TODO: type this
  const modelValue = model.get(name);
  if (modelValue !== undefined) {
    internalWritable.set(modelValue);
  }

  // when the model changes, update the store
  model.on('change:' + name, () => internalWritable.set(model.get(name)), null);

  return {
    // when the store changes, update the model
    set: (v: T) => {
      internalWritable.set(v);
      if (model) {
        model.set(name, v);
        model.save_changes();
      }
    },
    subscribe: internalWritable.subscribe,
    update: (func: (v: T) => T) => {
      internalWritable.update((v: T) => {
        const output = func(v);
        if (model) {
          model.set(name, output);
          model.save_changes();
        }
        return output;
      });
    },
  };
}

// Declare stores with their associated Traitlets here.
export let dataset: Writable<Data>;
export let selectedCol: Writable<ImgData[]>;
export let selectedImgs: Writable<Record<string, ImgData>>;
export let selectedImgBoxes: Writable<ImgBoxes>;
export let num_instances: Writable<number>;
export let height: Writable<number>;
export let IOU: Writable<number>;

// Stores that are not synced with traitlets
export let windowWidth: Writable<number>;
export let menuWidth: Writable<number>;
export let selectedImg: Writable<ImgData | undefined>;
export let selectedImgIdx: Writable<number>;
export let openDetailView: Writable<boolean>;
export let openCollectionMenu: Writable<boolean>;
export let breakdown: Writable<boolean>;
export let colorMap: Writable<StringNumMap>;
export let confidence: Writable<[number, number]>;
export let detectionSize: Writable<[number, number]>;
export let topHeight: Writable<number>;
export let tags: Writable<Array<string>>;

// Set the model for each store you create.
export function setStoreModels(model: DOMWidgetModel): void {
  //Stores that are synced with python

  dataset = createSyncedWidget<Data>(
    'dataset',
    {
      meta: {
        folderName: '',
        modelNames: [],
        SetIOU: 0.8,
      },
      models: {},
      ground_truth: [],
      imgs: [],
    },
    model
  );
  selectedCol = createSyncedWidget<ImgData[]>('selectedCol', [], model);
  selectedImgs = createSyncedWidget<Record<string, ImgData>>(
    'selectedImgs',
    {},
    model
  );
  console.log(model);
  num_instances = createSyncedWidget<number>('num_instances', 0, model);
  height = createSyncedWidget<number>('height', 800, model);
  IOU = createSyncedWidget<number>('IOU', 0.8, model);

  //Stores that are not synced with python
  topHeight = writable(300);
  windowWidth = writable(600);
  menuWidth = writable(200);
  selectedImg = writable(undefined);
  selectedImgBoxes = writable(undefined);
  selectedImgIdx = writable(-1);
  openDetailView = writable(false);
  openCollectionMenu = writable(false);
  breakdown = writable(false);
  colorMap = writable<StringNumMap>({});
  confidence = writable<[number, number]>([0.7, 1.0]);
  detectionSize = writable<[number, number]>([0.01, 0.4]);
  tags = writable<Array<string>>([]);
}
