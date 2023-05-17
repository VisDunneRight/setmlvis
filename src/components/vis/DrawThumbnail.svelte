<script lang="ts">
  import type { ImgData } from '../../types';
  import {
    selectedImg,
    openDetailView,
    colorMap,
    selectedImgIdx,
    breakdown
  } from '../../stores';
  import { color, colorTypes } from '../../ulit';

  export let data: ImgData;
  export let index: number;
  export let height: number;
  export let top: number;
  export let left: number;
  export let folderName = '';

  $: imgWidth = data === undefined ? 0 : data.imgSize[0];
  $: imgHeight = data === undefined ? 0 : data.imgSize[1];
  $: imgRatio = imgWidth / imgHeight;
  $: width = height * imgRatio;
  function selectImgData() {
    $selectedImg = data;
    $selectedImgIdx = index;
    $openDetailView = true;
  }
  $:console.log($breakdown);
</script>

<div
  class="media-element"
  style="width:{width}px;height:{height}px;left:{left}px;top:{top}px;{$breakdown ? 'border:3px ridge ' + colorTypes[data.category]+';': ''}"
>
  {#if data}
    <button
      on:click={() => {
        selectImgData();
      }}
    >
      <img
        height="{height}px"
        src={folderName + data.imgName}
        alt="selected Figure"
      />
      <svg {width} {height}>
        {#each Object.entries(data.boxes) as [name, box]}
          <rect
            x={box[1] * width}
            y={(box[2] * width) / imgRatio}
            width={(box[3] - box[1]) * width}
            height={((box[4] - box[2]) * width) / imgRatio}
            fill="none"
            stroke={color[$colorMap[name]]}
            stroke-width="2"
          />
        {/each}
        {#if data.iouGT > 0}
          <rect
            x={+data.gtShape[1] * width}
            y={(+data.gtShape[2] * width) / imgRatio}
            width={(+data.gtShape[3] - +data.gtShape[1]) * width}
            height={((+data.gtShape[4] - +data.gtShape[2]) * width) / imgRatio}
            fill="none"
            stroke="white"
          />
        {/if}
      </svg>
    </button>
  {/if}
</div>

<style>
  svg,
  img {
    position: absolute;
    left: 0px;
    top: 0px;
  }

  .media-element {
    border-radius: 0.25rem;
    /* flex: 1; */
    background-color: black;
    position: absolute;
  }
</style>
