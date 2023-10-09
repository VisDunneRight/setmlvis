<script lang="ts">
  import {
    selectedCol,
    selectedImgs,
    windowWidth,
    menuWidth,
    topHeight,
    height,
  } from '../stores';
  import type { ImgData, ImgInfo } from '../types';
  import RangeSlider from 'svelte-range-slider-pips';
  import DrawThumbnail from './vis/DrawThumbnail.svelte';
  import VisToggle from './vis/VisToggle.svelte';
  import {
    Menu,
    MenuButton,
    MenuItems,
    MenuItem,
  } from '@rgossiaux/svelte-headlessui';

  import './collectionSlider.css';
  export let folderName = '';
  let imgHeight = [100];
  let gap = 4;
  $: selected = {};

  function rescaleImages(
    imageData: ImgData[],
    startingHeight: number,
    maxWidth: number,
    gap: number
  ) {
    let imgInfo: ImgInfo[] = [];
    let currentRow: ImgInfo[] = [];
    let currentWidth = 0;
    let left = 0;
    let top = 0;
    imageData.forEach((img) => {
      let imgWidth = img === undefined ? 0 : img.imgSize[0];
      let imgHeight = img === undefined ? 0 : img.imgSize[1];
      let imgRatio = imgWidth / imgHeight;
      let width = startingHeight * imgRatio;
      // if img fits add to the currentrow
      if (currentWidth + width + gap <= maxWidth) {
        currentRow.push({
          top: top,
          left: left,
          data: img,
          height: startingHeight,
        });
        left += width + gap;
        currentWidth += width + gap;
      } else {
        //if img doesn't fit look at the entire row, scale images
        let multRatio = maxWidth / currentWidth;
        let newLeft = 0;
        currentRow.forEach((item) => {
          item.height *= multRatio;
          item.left = newLeft;
          let imgRat =
            item.data === undefined
              ? 1
              : item.data.imgSize[0] / item.data.imgSize[1];
          newLeft += item.height * imgRat + gap;
        });
        //reset all values
        imgInfo = imgInfo.concat(currentRow);
        left = 0;
        top += currentRow[0].height + gap;
        currentRow = [];
        currentRow.push({
          top: top,
          left: left,
          data: img,
          height: startingHeight,
        });
        left += width + gap;
        currentWidth = width;
      }
    });
    //if there any images left in currentRow copy them over
    if (currentRow.length > 0) {
      imgInfo = imgInfo.concat(currentRow);
    }

    return imgInfo;
  }
  $: imgInfo = rescaleImages(
    $selectedCol,
    imgHeight[0],
    $windowWidth - $menuWidth - 16,
    gap
  );

  $: collectionHeight = $height - $topHeight - 48;
  $: heightSize =
    imgInfo.length > 0
      ? imgInfo[imgInfo.length - 1].top + imgInfo[imgInfo.length - 1].height
      : 0;
  function UpdateSelectedImgs(id: string, data: ImgData, checked: boolean) {
    let selectImgUpdate = { ...$selectedImgs };
    if (checked) {
      selectImgUpdate[id] = data;
    } else {
      delete selectImgUpdate[id];
    }
    selected = selectImgUpdate;
    $selectedImgs = selectImgUpdate;
  }

  function ClearAllSelectedImgs() {
    $selectedImgs = {};
    selected = {};
  }
  function ShowSelectedImgs() {
    if (Object.entries($selectedImgs).length === 0) {
      return;
    }
    let imgSelection: ImgData[] = [];
    for (const [, value] of Object.entries($selectedImgs).values()) {
      imgSelection.push(value);
    }
    $selectedCol = imgSelection;
  }
  function ClearCurrentSelectedImgs() {
    let selectImgUpdate = { ...$selectedImgs };
    for (const imgdata of $selectedCol) {
      if (imgdata.id in selectImgUpdate) {
        delete selectImgUpdate[imgdata.id];
      }
    }
    selected = selectImgUpdate;
    $selectedImgs = selectImgUpdate;
  }
  function HideSelectedImgs() {
    let imgSelection: ImgData[] = [];
    for (const imgdata of $selectedCol) {
      if (!(imgdata.id in $selectedImgs)) {
        imgSelection.push(imgdata);
      }
    }
    $selectedCol = imgSelection;
  }
  $: console.log($selectedCol);
</script>

<div
  class="collection-container"
  style:width="100%"
  style:height="100%"
  style:top="{$topHeight}px"
>
  <div class="media-scroller" id="scrollBar">
    <div class="collection-menu">
      <div style="display:flex; align-items:center;gap:1rem;">
        <Menu>
          <MenuButton class="img-select">
            <span>{Object.entries($selectedImgs).length}</span>
            <svg
              class="svg-icon"
              focusable="false"
              aria-hidden="true"
              viewBox="0 0 24 24"
              data-testid="CheckIcon"
              ><path
                d="M9 16.17 4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"
              /></svg
            >
          </MenuButton>
          <MenuItems>
            <div class="menu-option">
              <MenuItem
                let:active
                class="menu-selection"
                title="Clear images from current collection"
              >
                <span
                  class:active
                  on:click={ClearCurrentSelectedImgs}
                  on:keypress={ClearCurrentSelectedImgs}
                  >Clear Current Selected Images</span
                >
              </MenuItem>
              <MenuItem
                let:active
                class="menu-selection"
                title="Clear all images selected"
              >
                <span
                  class:active
                  on:click={ClearAllSelectedImgs}
                  on:keypress={ClearAllSelectedImgs}
                  >Clear All Selected Images</span
                >
              </MenuItem>
              <MenuItem
                let:active
                class="menu-selection"
                title="Show all images selected"
              >
                <span
                  class:active
                  on:click={ShowSelectedImgs}
                  on:keypress={ShowSelectedImgs}>Only Show Selected Images</span
                >
              </MenuItem>
              <MenuItem
                let:active
                class="menu-selection"
                title="Hide selected images"
              >
                <span
                  class:active
                  on:click={HideSelectedImgs}
                  on:keypress={HideSelectedImgs}>Hide Selected Images</span
                >
              </MenuItem>
            </div>
          </MenuItems>
        </Menu>
        <VisToggle
          message={'Group Images'}
          activeColor="blueviolet"
          inactiveColor="#540077"
        />
      </div>
      <div style="display:flex;color:#f3edeb;">
        <div class="collection-count">
          <div>
            <span>{imgInfo.length}</span>
            images
          </div>
        </div>
        <div class="image-size">
          <RangeSlider
            pips
            min={100}
            max={300}
            step={10}
            bind:values={imgHeight}
            id="reverse-pips"
          />
        </div>
      </div>
    </div>
    <div class="collection-area" style:height="{collectionHeight}px">
      {#each imgInfo as img, i}
        <DrawThumbnail
          left={img.left}
          top={img.top}
          data={img.data}
          height={img.height}
          index={i}
          {folderName}
          selected={img.data.id in selected}
          updateSelection={(checked) => {
            UpdateSelectedImgs(img.data.id, img.data, checked);
          }}
        />
      {/each}
      <div class="bottom-spacing" style:top="{heightSize}px" />
    </div>
  </div>
</div>

<style>
  .media-scroller {
    position: absolute;
    width: 100%;
    height: 100%;
    overflow-y: auto;
    overflow-x: hidden;
  }

  .collection-menu {
    position: sticky;
    top: 0px;
    display: flex;
    width: 100%;
    height: 48px;
    padding: 7px;
    z-index: 2;
    justify-content: space-between;
    background: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0));
  }

  .menu-option {
    background-color: rgb(26, 26, 26);
    border: 1px solid rgb(13, 13, 13);
    border-radius: 2px;
    box-shadow: rgb(26, 26, 26) 0px 2px 20px;
    box-sizing: border-box;
    margin-top: 0.6rem;
    position: absolute;
    width: auto;
    z-index: 801;
    font-size: 14px;
    padding: 0px 0.5rem;
    min-width: 14rem;
    opacity: 1;
    z-index: 100001;
    right: unset;
  }

  :global(.collection-menu .img-select) {
    width: 50px;
    padding: 0.25rem 0.75rem;
    line-height: 2rem;
    border-radius: 1rem;
    border: none;
    align-items: center;
    background-color: blueviolet;
    color: rgb(255, 255, 255);
    cursor: pointer;
    display: flex;
    justify-content: space-between;
  }

  :global(.collection-menu .menu-selection) {
    cursor: pointer;
    margin: 0px -0.5rem;
    padding: 0.25rem 0.5rem;
    font-weight: bold;
    display: flex;
    -webkit-box-pack: center;
    place-content: center;
    flex-direction: column;
    text-decoration: none;
    color: rgb(179, 179, 179);
  }
  .svg-icon {
    user-select: none;
    width: 1em;
    display: inline-block;
    fill: currentcolor;
    flex-shrink: 0;
    transition: fill 200ms cubic-bezier(0.4, 0, 0.2, 1) 0ms;
    font-size: 1.5rem;
  }

  .media-scroller {
    position: absolute;
    width: 100%;
    height: 100%;
    overflow-y: auto;
    overflow-x: hidden;
  }
  .collection-count {
    display: flex;
    -webkit-box-pack: center;
    place-content: center;
    flex-direction: column;
    margin: 0px 0.25rem;
    padding-right: 1rem;
    font-weight: bold;
  }
  .image-size {
    width: 10rem;
    padding-right: 1rem;
  }

  /* #scrollBar::-webkit-scrollbar-track
{
	-webkit-box-shadow: inset 0 0 6px rgba(0,0,0,0.3);
	border-radius: 5px;
	background-color: #F5F5F5;
}

#scrollBar::-webkit-scrollbar
{
	width: 8px;
	background-color: #F5F5F5;
}

#scrollBar::-webkit-scrollbar-thumb
{
	border-radius: 5px;
	-webkit-box-shadow: inset 0 0 6px rgba(0,0,0,.3);
	background-color: #555;
} */
  .collection-area {
    position: relative;
    overflow-y: scroll;
    padding-bottom: 10px;
  }
  .collection-container {
    position: absolute;
    background-color: lightgray;
    min-width: 200px;
    top: 360px;
    border: 1px solid rgb(226, 226, 226);
    /* overflow-y: scroll; */
  }
  .bottom-spacing {
    height: 10px;
    width: 100%;
    position: absolute;
  }
</style>
