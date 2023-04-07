//Shared file that contains all types used in the work

export type Data = Record<string, Array<DataRes> >

export type DataRes = Record<string, FNorImgData>

export type FNorImgData = ImgData | FN


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

export type FN = [string, string, string, string, string]