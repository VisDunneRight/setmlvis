//Shared file that contains all types used in the work

export type Data = Record<string, Array<DataRes> >
export type DataRes = {'FN': FN} & Record<string, ImgData>

export type ImgInfo = {
  height: number,
  left: number,
  top: number,
  data: ImgData
}

export type StringNumMap = {
  [index:string] : number;
}

export type ImgData = {
  IOU:number,
  boxes:object,
  confidence:Array<number>,
  gtShape:FN,
  imgName:string,
  imgSize:[number, number],
  iouGT:number,
  shape:[number, number, number, number]
} | undefined

export type MenuItem =  ButtonItem | SliderType | DoubleSliderType;

export type ButtonItem = {
  id:string,
  name:string,
  type:'button'
  updatefunction: (arg0:any) => void
}

export type SliderType = {
  id:string,
  name:string,
  type:'slider',
  min:number,
  max:number,
  step:number,
  value:number,
  updatefunction: (arg0:any) => void
}

export type DoubleSliderType = {
  id:string,
  name:string,
  type:'double-slider',
  value:number,
  value2:number,
  min:number,
  max:number,
  step:number,
  updatefunction: (arg0:any) => void
}

export type FN = [string, string, string, string, string]