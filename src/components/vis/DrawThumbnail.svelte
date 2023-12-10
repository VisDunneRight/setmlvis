<script lang="ts">
  import type { Image, ImgData } from '../../types';
  import DuplicateIcon from '../../assets/duplicate.svelte';
  import FarWayIcon from '../../assets/far-away.svelte';
  import LowThresholdIcon from '../../assets/low-threshold-normal.svelte';
  import WrongClassIcon from '../../assets/wrong-class.svelte';
  import Checkbox from '../menuComp/checkbox.svelte';

  import {
    selectedImg,
    openDetailView,
    colorMap,
    selectedImgIdx,
    breakdown,
    IOU,
    tags,
  } from '../../stores';
  import { color, colorTypes } from '../../ulit';

  export let data: ImgData;
  export let index: number;
  export let height: number;
  export let top: number;
  export let left: number;
  export let imgInfo: Image;
  export let folderName = '';
  export let selected: boolean;
  export let updateSelection: (checked: boolean) => void;

  $: imgWidth = data === undefined ? 0 : imgInfo.imgSize[0];
  $: imgHeight = data === undefined ? 0 : imgInfo.imgSize[1];
  $: imgRatio = imgWidth / imgHeight;
  $: width = height * imgRatio;

  function selectImgData() {
    $selectedImg = data;
    $selectedImgIdx = index;
    $openDetailView = true;
  }
  let iconSize = 14;
</script>

<div
  class="media-element"
  style="width:{width}px;height:{height}px;left:{left}px;top:{top}px;"
>
  {#if data}
    <button
      on:click={() => {
        selectImgData();
      }}
      class="button"
    >
      <img
        height="{height}px"
        src={folderName + imgInfo.imgName}
        alt="selected Figure"
      />

      <svg {width} {height}>
        {#each Object.entries(data.boxes) as [name, box]}
          <rect
            x={box[1] * width}
            y={(box[2] * width) / imgRatio}
            width={(box[3] - box[1]) * width}
            height={((box[4] - box[2]) * width) / imgRatio}
            class={'box-rect'}
            stroke={color[$colorMap[name]]}
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
        {#if $breakdown === true}
          {#if data.iouGT >= $IOU}
            <polygon points="0,0 0,36 36,0" fill={colorTypes['true_pos']} />
          {:else}
            <polygon points="0,0 0,36 36,0" fill={colorTypes[data.category]} />
            {#if data.category === 'duplicate'}
              <DuplicateIcon width={iconSize} height={iconSize} />
            {:else if data.category === 'far_away'}
              <FarWayIcon width={iconSize + 6} height={iconSize + 6} />
            {:else if data.category === 'low_threshold'}
              <LowThresholdIcon width={iconSize} height={iconSize} />
            {:else if data.category === 'wrong_class'}
              <WrongClassIcon width={iconSize} height={iconSize} />
            {/if}
          {/if}
        {/if}
        <title>{imgInfo.imgName}</title>
      </svg>
    </button>
    <div class="tag-display">
      {#each data.tags as tag}
        <div
          title={tag}
          style="background-color:{color[$tags.indexOf(tag) % 10]};"
        >
          {tag}
        </div>
      {/each}
    </div>
    <div class="checkbox-pos {selected === true ? 'checkbox-show' : ''}">
      <div />
      <Checkbox checked={selected} {updateSelection} />
    </div>
  {/if}
</div>

<style>
  .tag-display {
    position: absolute;
    bottom: 0;
    padding: 0.5rem;
    max-height: 100%;
    overflow-y: auto;
    scrollbar-width: none;
    width: 100%;
    pointer-events: none;
    font-family: Palanquin, sans-serif;
    font-weight: 700;
    font-size: 14px;
    overflow: hidden;
  }
  .tag-display > div {
    display: inline-block;
    box-sizing: content-box;
    height: 1em;
    margin: 0 2px;
    padding: 3px;
    color: white;
    font-size: 12px;
    line-height: 12px;
    border-radius: 3px;
    font-weight: 700;
    text-align: center;
    vertical-align: bottom;
    pointer-events: auto;
    max-width: calc(100% - 8px);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  svg,
  img {
    position: absolute;
    left: 0px;
    top: 0px;
  }
  svg:hover,
  svg:active {
    background: rgba(0, 0, 0, 0.6);
  }
  .box-rect {
    fill: none;
    stroke-width: 2px;
  }

  .checkbox-pos {
    position: absolute;
    left: 0px;
    top: 0px;
    display: flex;
    width: 100%;
    justify-content: space-between;
    align-items: baseline;
    opacity: 0;
  }
  .checkbox-show {
    opacity: 1;
    visibility: visible;
    background: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0));
  }

  .checkbox-pos:hover,
  .checkbox-pos:active {
    opacity: 1;
    visibility: visible;
    background: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0));
  }

  .media-element {
    border-radius: 0.25rem;
    /* flex: 1; */
    background-color: black;
    position: absolute;
  }
</style>
