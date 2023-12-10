<script lang="ts">
  import {
    windowWidth,
    selectedImg,
    selectedImgIdx,
    height,
    openDetailView,
    selectedCol,
    dataset,
    selectedImgBoxes,
  } from '../stores';

  import DrawTextbox from './vis/DrawTextbox.svelte';
  import RightPanel from './detail/RightPanel.svelte';
  import { colorMap } from '../stores';
  import { color } from '../ulit';

  // Try loading the figure and finding its position
  // Add svg/bounding box
  // Add Labels to indicate confidence interval
  export let folderName: string;
  $: compWidth = $windowWidth * 0.95 - 300;
  $: compHeight = $height * 0.9;
  $: imgWidth =
    $selectedImg === undefined
      ? 0
      : $dataset.imgs[$selectedImg.imgId].imgSize[0];
  $: imgHeight =
    $selectedImg === undefined
      ? 0
      : $dataset.imgs[$selectedImg?.imgId ?? 0].imgSize[1];

  function capitalize(str: string): string {
    return str.charAt(0).toUpperCase() + str.slice(1);
  }

  function showConfidence(className: string, num: number): string {
    return capitalize(className) + ': ' + ((num * 100) / 100).toFixed(2);
  }

  function calculateAspectRatioFit(
    srcWidth: number,
    srcHeight: number,
    maxWidth: number,
    maxHeight: number
  ) {
    var ratio = Math.min(maxWidth / srcWidth, maxHeight / srcHeight);
    return { width: srcWidth * ratio, height: srcHeight * ratio };
  }

  $: newImg = calculateAspectRatioFit(
    imgWidth,
    imgHeight,
    compWidth,
    compHeight
  );

  function move2NextImg(value: number) {
    if (value >= $selectedCol.length) {
      value = 0;
    } else if (value < 0) {
      value = $selectedCol.length - 1;
    }
    $selectedImg = $selectedCol[value];
    $selectedImgIdx = value;
  }
</script>

<div id="model" class="modal {$openDetailView ? 'modalon' : ''}">
  <div id="setvis-model-container" class="modal-container">
    <div class="modal-window">
      <div
        class="detail-container"
        style:width="{compWidth}px"
        style:height="{compHeight}px"
      >
        {#if $selectedImg}
          <div class="model-img">
            <button
              class="model-arrow-prev"
              on:click={() => {
                move2NextImg($selectedImgIdx - 1);
              }}
            >
              <svg class="svg-icon" viewBox="0 0 20 20">
                <path
                  fill="white"
                  d="M8.388,10.049l4.76-4.873c0.303-0.31,0.297-0.804-0.012-1.105c-0.309-0.304-0.803-0.293-1.105,0.012L6.726,9.516c-0.303,0.31-0.296,0.805,0.012,1.105l5.433,5.307c0.152,0.148,0.35,0.223,0.547,0.223c0.203,0,0.406-0.08,0.559-0.236c0.303-0.309,0.295-0.803-0.012-1.104L8.388,10.049z"
                />
              </svg>
            </button>

            <button
              class="model-arrow-next"
              on:click={() => {
                move2NextImg($selectedImgIdx + 1);
              }}
            >
              <svg class="svg-icon" viewBox="0 0 20 20">
                <path
                  fill="white"
                  d="M11.611,10.049l-4.76-4.873c-0.303-0.31-0.297-0.804,0.012-1.105c0.309-0.304,0.803-0.293,1.105,0.012l5.306,5.433c0.304,0.31,0.296,0.805-0.012,1.105L7.83,15.928c-0.152,0.148-0.35,0.223-0.547,0.223c-0.203,0-0.406-0.08-0.559-0.236c-0.303-0.309-0.295-0.803,0.012-1.104L11.611,10.049z"
                />
              </svg>
            </button>
            <div
              style:width="{newImg.width}px"
              style:height="{newImg.height}px"
              style="align-self: center;position: absolute;"
            >
              <div>
                <img
                  width="{newImg.width}px"
                  height={newImg.height}
                  src={folderName + $dataset?.imgs[$selectedImg.imgId]?.imgName}
                  alt="selected Figure"
                />
                <svg width={newImg.width} height={newImg.height}>
                  {#if $selectedImg.iouGT > 0}
                    <DrawTextbox
                      x={+$selectedImg.gtShape[1] * newImg.width}
                      y={+$selectedImg.gtShape[2] * newImg.height}
                      backgroundColor="white"
                      size={13}
                      textColor="black"
                      text="Ground truth"
                    />
                    <rect
                      x={+$selectedImg.gtShape[1] * newImg.width}
                      y={+$selectedImg.gtShape[2] * newImg.height}
                      width={(+$selectedImg.gtShape[3] -
                        +$selectedImg.gtShape[1]) *
                        newImg.width}
                      height={(+$selectedImg.gtShape[4] -
                        +$selectedImg.gtShape[2]) *
                        newImg.height}
                      fill="none"
                      stroke="white"
                    />
                  {/if}
                  {#each Object.entries($selectedImg.boxes) as [name, box]}
                    <DrawTextbox
                      x={+box[1] * newImg.width}
                      y={+box[2] * newImg.height}
                      backgroundColor={color[$colorMap[name]]}
                      textColor="white"
                      size={13}
                      text={showConfidence(box[0], +box[5])}
                    />
                    <rect
                      x={+box[1] * newImg.width}
                      y={+box[2] * newImg.height}
                      width={(+box[3] - +box[1]) * newImg.width}
                      height={(+box[4] - +box[2]) * newImg.height}
                      fill="none"
                      stroke={color[$colorMap[name]]}
                    />
                  {/each}
                  {#if $selectedImgBoxes}
                    {#each $selectedImgBoxes.ground_truth.data as dect}
                      {#if dect.selected}
                        <DrawTextbox
                          x={+dect.shape[1] * newImg.width}
                          y={+dect.shape[2] * newImg.height}
                          backgroundColor="white"
                          size={13}
                          textColor="black"
                          text="Ground truth"
                        />
                        <rect
                          x={+dect.shape[1] * newImg.width}
                          y={+dect.shape[2] * newImg.height}
                          width={(+dect.shape[3] - +dect.shape[1]) *
                            newImg.width}
                          height={(+dect.shape[4] - +dect.shape[2]) *
                            newImg.height}
                          fill="none"
                          stroke="white"
                        />
                      {/if}
                    {/each}
                    {#each Object.entries($selectedImgBoxes.detections) as [name, arrydect]}
                      {#each arrydect.data as dect}
                        {#if dect.selected}
                          <DrawTextbox
                            x={+dect.data[1] * newImg.width}
                            y={+dect.data[2] * newImg.height}
                            backgroundColor={color[$colorMap[name]]}
                            textColor="white"
                            size={13}
                            text={showConfidence(dect.data[0], +dect.data[5])}
                          />
                          <rect
                            x={+dect.data[1] * newImg.width}
                            y={+dect.data[2] * newImg.height}
                            width={(+dect.data[3] - +dect.data[1]) *
                              newImg.width}
                            height={(+dect.data[4] - +dect.data[2]) *
                              newImg.height}
                            fill="none"
                            stroke={color[$colorMap[name]]}
                          />
                        {/if}
                      {/each}
                    {/each}
                  {/if}
                </svg>
              </div>
            </div>
          </div>
          <div class="model-menu">
            <RightPanel />
          </div>
        {/if}
      </div>
    </div>
  </div>
</div>

<style>
  /* .small {
    font: 13px sans-serif;
    fill: white;
  } */

  .model-menu {
    position: relative;
    user-select: auto;
    border-left: 1px solid rgb(13, 13, 13);
    border-top-right-radius: 8px;
    display: flex;
    flex-direction: column;
    width: 300px;
    height: 100%;
    max-width: 600px;
    min-width: 200px;
    box-sizing: border-box;
    flex-shrink: 0;
    background-color: #424242;
  }

  .model-img {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-grow: 1;
  }

  .model-arrow-prev {
    cursor: pointer;
    position: absolute;
    display: flex;
    -webkit-box-align: center;
    align-items: center;
    -webkit-box-pack: justify;
    justify-content: space-between;
    z-index: 99999;
    padding: 0.75rem;
    left: 0px;
    width: 5rem;
    height: 5rem;
    background-color: darkgray;
    border: none;
    opacity: 0.6;
    transition: box-shadow 0.15s ease-in-out 0s;
  }

  .model-arrow-next {
    cursor: pointer;
    position: absolute;
    display: flex;
    -webkit-box-align: center;
    align-items: center;
    -webkit-box-pack: justify;
    justify-content: space-between;
    z-index: 99999;
    padding: 0.75rem;
    right: 0.75rem;
    width: 5rem;
    height: 5rem;
    background-color: darkgray;
    border: none;
    opacity: 0.6;
    transition: box-shadow 0.15s ease-in-out 0s;
  }
  .modal {
    position: absolute;
    width: 100%;
    height: 100%;
    background-color: var(--joy-palette-background-modalBackdrop);
    top: 0;
    z-index: 1000;
    display: block;
    visibility: hidden;
  }

  .modalon {
    display: block;
    visibility: visible;
  }

  .modal-container {
    width: 100%;
    height: 100%;
    z-index: 10000;
    -webkit-box-align: center;
    align-items: center;
    display: flex;
    -webkit-box-pack: center;
    justify-content: center;
    background-color: rgba(51, 51, 51, 0.298);
  }

  .modal-window {
    width: 95%;
    height: 90%;
    border-radius: 3px;
    z-index: 10001;
    background-color: rgba(100, 100, 100);
    border: 1px solid rgba(100, 100, 100);
    position: relative;
    display: flex;
    -webkit-box-pack: center;
    justify-content: center;
    overflow: hidden;
    box-shadow: rgb(0, 0, 0) 0px 20px 25px -20px;
  }
  svg,
  img {
    position: absolute;
    left: 0px;
    right: 0px;
  }
  .detail-container {
    -webkit-box-flex: 1;
    flex-grow: 1;
    width: 1px;
    position: relative;
    overflow: visible;
    display: flex;
  }
</style>
