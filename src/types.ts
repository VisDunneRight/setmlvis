//Shared file that contains all types used in the work

export type Data = {
  false_negatives: Record<string, Array<ImgFalse>>;
  meta: Meta;
  models: Models;
  ground_truth: Array<ObjectDect>;
  imgs: Array<Image>;
};

export type ImgFalse = {
  imageId: number;
  values: Array<ObjectDect>;
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

export type ImgBoxes =
  | {
      ground_truth: GroundTruthObj;
      detections: Detection;
    }
  | undefined;

export type GroundTruthObj = {
  data: Array<GroundTruth>;
  selected: [number, number, number];
};

export type GroundTruth = {
  id: number;
  shape: ObjectDect;
  selected: boolean;
  type: number;
};

export type DetectObject = {
  data: Array<Detect>;
  selected: [number, number, number];
};

export type Detection = {
  [key: string]: DetectObject;
};

export type Sort = {
  [key: string]: number;
};

export type Detect = { selected: boolean; data: Box; type: number; id: string };

export type Image =
  | {
      imgName: string;
      imgSize: [number, number];
      ground_truth: Array<number>;
    }
  | undefined;

export type ImgData = {
  IOU: number;
  boxes: Boxes;
  confidence: Array<number>;
  gtShape: ObjectDect;
  id: string;
  imgId: number;
  tags: Array<string>;
  weightedConfidence: number;

  category: 'duplicate' | 'low_threshold' | 'far_away' | 'wrong_class';
  iouGT: number;
  shape: [number, number, number, number];
};

export type Boxes = {
  [key: string]: Box;
};
export type Box = [string, string, string, string, string, string];

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

export type Tag = Record<string, TagInfo>;

export type TagInfo = {
  count: number;
  selected: boolean;
  name: string;
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
