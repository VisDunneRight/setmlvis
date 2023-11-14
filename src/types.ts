//Shared file that contains all types used in the work

export type Data = {
  meta: Meta;
  models: Models;
  ground_truth: Array<ObjectDect>;
  imgs: Array<Image>;
};
export type Models = Record<string, Array<DataRes>>;

export type DataRes = {
  detections: Record<string, ImgData>;
  FN: FN;
};

export type ImgInfo = {
  height: number;
  left: number;
  top: number;
  data: ImgData;
};

export type Meta = {
  folderName: string;
  modelNames: Array<string>;
  SetIOU: number;
};

export type StringNumMap = Record<string, number>;

export type Image = {
  imgName: string;
  imgSize: [number, number];
  ground_truth: Array<number>;
};

export type ImgData = {
  IOU: number;
  boxes: object;
  confidence: Array<number>;
  gtShape: ObjectDect;
  id: string;
  imgId: number;

  category: 'duplicate' | 'low_threshold' | 'far_away' | 'wrong_class';
  iouGT: number;
  shape: [number, number, number, number];
};

export type MenuItem = SliderType | DoubleSliderType;

export type ButtonItem = {
  id: string;
  name: string;
  type: 'button';
  updatefunction: (arg0: any) => void;
};

export type SliderType = {
  id: string;
  name: string;
  type: 'slider';
  min: number;
  max: number;
  step: number;
  value: number;
  updatefunction: (arg0: any) => void;
};

export type DoubleSliderType = {
  id: string;
  name: string;
  type: 'double-slider';
  value: number;
  value2: number;
  min: number;
  max: number;
  step: number;
  updatefunction: (arg0: any) => void;
};

export type FN = ObjectDect;

export type ObjectDect = [string, string, string, string, string];
