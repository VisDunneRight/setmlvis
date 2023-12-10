<script lang="ts">
  import {
    selectedCol,
    dataset,
    selectedImgs,
    windowWidth,
    menuWidth,
    topHeight,
    height,
    tags,
  } from '../stores';
  import type { Image, ImgData, ImgInfo, Sort } from '../types';
  import { color } from '../ulit';
  import RangeSlider from 'svelte-range-slider-pips';
  import DrawThumbnail from './vis/DrawThumbnail.svelte';
  import VisToggle from './vis/VisToggle.svelte';
  import Checked from '../assets/checked.svelte';
  import Unchecked from '../assets/unchecked.svelte';
  import CheckedMinus from '../assets/checked-minus.svelte';
  import {
    Menu,
    MenuButton,
    MenuItems,
    MenuItem,
  } from '@rgossiaux/svelte-headlessui';

  import './collectionSlider.css';
  import SortUp from '../assets/sort-up.svelte';
  import SortDown from '../assets/sort-down.svelte';
  import { every } from 'd3';
  export let folderName = '';
  let imgHeight = [100];
  let gap = 4;
  $: tagText = '';
  $: selected = {};
  $: imgTags = new Array<number>();
  $: imgTags2 = new Array<number>();
  let sortBy: Sort = { sortByIOU: 0, sortByID: 1 };

  function rescaleImages(
    imageData: ImgData[],
    images: Array<Image>,
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
      let imgWidth = img === undefined ? 0 : images[img.imgId].imgSize[0];
      let imgHeight = img === undefined ? 0 : images[img.imgId].imgSize[1];
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
              : images[item.data.imgId].imgSize[0] /
                images[item.data.imgId].imgSize[1];
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
    $dataset['imgs'],
    imgHeight[0],
    $windowWidth - $menuWidth - 16,
    gap
  );

  $: collectionHeight = $height - $topHeight - 48;
  $: heightSize =
    imgInfo.length > 0
      ? imgInfo[imgInfo.length - 1].top + imgInfo[imgInfo.length - 1].height
      : 0;

  function UpdateImgTag() {
    let count = new Array($tags.length).fill(0);
    Object.entries($selectedImgs).forEach(([name, data]) => {
      data.tags.forEach((tag) => {
        count[$tags.indexOf(tag)] += 1;
      });
    });

    count.forEach((val, i) => {
      if (Object.keys($selectedImgs).length === val) {
        imgTags[i] = 2;
      } else if (val > 0) {
        imgTags[i] = 1;
      } else {
        imgTags[i] = 0;
      }
    });

    imgTags2 = [...imgTags];
  }

  function UpdateSelectedImgs(id: string, data: ImgData, checked: boolean) {
    let selectImgUpdate = { ...$selectedImgs };
    if (checked) {
      selectImgUpdate[id] = data;
    } else {
      delete selectImgUpdate[id];
    }
    selected = selectImgUpdate;
    $selectedImgs = selectImgUpdate;
    UpdateImgTag();
  }

  function addTag() {
    Object.entries(selected).forEach(([name, prop]) => {
      prop.tags.push(tagText);
    });
    if ($tags.indexOf(tagText) === -1) {
      $tags.push(tagText);
      imgTags = imgTags
        .concat(Array($tags.length).fill(0))
        .slice(0, $tags.length);
    }
    tagText = '';
    //forces updates the images
    imgInfo = imgInfo;
    UpdateImgTag();
  }

  function applyTags() {
    imgTags2.forEach((val, index) => {
      if (val === imgTags[index]) {
        return;
      }
      const tagName = $tags[index];
      //Delete
      if (val === 0) {
        Object.entries($selectedImgs).forEach(([name, data]) => {
          if (data.tags.includes(tagName)) {
            data.tags = data.tags.filter((elem) => elem !== tagName);
          }
        });
      } else {
        //Add
        Object.entries($selectedImgs).forEach(([name, data]) => {
          if (!data.tags.includes(tagName)) {
            data.tags.push(tagName);
          }
        });
      }
    });
    imgTags = imgTags2;
    imgInfo = imgInfo;
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

  function updateSorting(value: string) {
    let temp = sortBy[value];
    for (const name in sortBy) {
      sortBy[name] = 0;
    }
    if (temp < 2) {
      sortBy[value] = 2;
    } else {
      sortBy[value] = 1;
    }

    if (value === 'sortByIOU') {
      if (sortBy[value] === 2) {
        $selectedCol.sort((a, b) => a.IOU - b.IOU);
      } else {
        $selectedCol.sort((a, b) => b.IOU - a.IOU);
      }
    } else if (value === 'sortByID') {
      if (sortBy[value] === 2) {
        $selectedCol.sort((a, b) => a.imgId - b.imgId);
      } else {
        $selectedCol.sort((a, b) => b.imgId - a.imgId);
      }
    }
    imgInfo = rescaleImages(
      $selectedCol,
      $dataset['imgs'],
      imgHeight[0],
      $windowWidth - $menuWidth - 16,
      gap
    );
  }

  const handleCheck = (idx: number) => {
    if (imgTags2[idx] === 0) {
      imgTags2[idx] = 2;
    } else {
      imgTags2[idx] = 0;
    }
  };
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
        <Menu>
          <MenuButton class="tag-select"
            ><svg
              width={20}
              height={20}
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M7.0498 7.0498H7.0598M10.5118 3H7.8C6.11984 3 5.27976 3 4.63803 3.32698C4.07354 3.6146 3.6146 4.07354 3.32698 4.63803C3 5.27976 3 6.11984 3 7.8V10.5118C3 11.2455 3 11.6124 3.08289 11.9577C3.15638 12.2638 3.27759 12.5564 3.44208 12.8249C3.6276 13.1276 3.88703 13.387 4.40589 13.9059L9.10589 18.6059C10.2939 19.7939 10.888 20.388 11.5729 20.6105C12.1755 20.8063 12.8245 20.8063 13.4271 20.6105C14.112 20.388 14.7061 19.7939 15.8941 18.6059L18.6059 15.8941C19.7939 14.7061 20.388 14.112 20.6105 13.4271C20.8063 12.8245 20.8063 12.1755 20.6105 11.5729C20.388 10.888 19.7939 10.2939 18.6059 9.10589L13.9059 4.40589C13.387 3.88703 13.1276 3.6276 12.8249 3.44208C12.5564 3.27759 12.2638 3.15638 11.9577 3.08289C11.6124 3 11.2455 3 10.5118 3ZM7.5498 7.0498C7.5498 7.32595 7.32595 7.5498 7.0498 7.5498C6.77366 7.5498 6.5498 7.32595 6.5498 7.0498C6.5498 6.77366 6.77366 6.5498 7.0498 6.5498C7.32595 6.5498 7.5498 6.77366 7.5498 7.0498Z"
                stroke="#ffffff"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
              />
            </svg></MenuButton
          >

          <MenuItems>
            <div class="panel-contents">
              <div class="panel-row-input">
                <input
                  class="tags-input"
                  type="text"
                  bind:value={tagText}
                  placeholder="+tag {Object.entries($selectedImgs)
                    .length} selected sample"
                />
              </div>
              {#if tagText !== ''}
                <div class="panel-row">
                  <div
                    class="tags-button"
                    on:click={(e) => {
                      e.preventDefault();
                      addTag();
                    }}
                    on:keypress={(e) => {
                      e.preventDefault();
                      addTag();
                    }}
                  >
                    <span class="tags-span"
                      >add &quot{tagText}&quot tag to {Object.entries(
                        $selectedImgs
                      ).length} samples.</span
                    >
                  </div>
                </div>
              {:else if $tags.length > 0}
                <div class="tag-list">
                  {#each $tags as tag, i}
                    <span
                      class="tags-set"
                      on:click={(e) => handleCheck(i)}
                      on:keydown={(e) => handleCheck(i)}
                    >
                      {#if imgTags2[i] === 2}
                        <Checked size={16} color={color[i % 10]} />
                      {:else if imgTags2[i] === 1}
                        <CheckedMinus size={16} color={color[i % 10]} />
                      {:else}
                        <Unchecked size={16} color={color[i % 10]} />
                      {/if}
                      {tag}
                    </span>
                  {/each}
                </div>
              {/if}
              {#if !imgTags.every((val, idx) => val === imgTags2[idx])}
                <div class="panel-row">
                  <div
                    class="tags-button"
                    on:click={(e) => {
                      applyTags();
                    }}
                    on:keypress={(e) => {
                      applyTags();
                    }}
                  >
                    <span
                      class="tags-span"
                      style="display:flex; justify-content:center;">Apply</span
                    >
                  </div>
                </div>
              {/if}
            </div>
          </MenuItems>
        </Menu>
        <Menu>
          <MenuButton class="tag-select">
            <svg
              width={20}
              height={20}
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M16 18L16 16M16 6L20 10.125M16 6L12 10.125M16 6L16 13"
                stroke="#ffffff"
                stroke-width="1.5"
                stroke-linecap="round"
                stroke-linejoin="round"
              />
              <path
                d="M8 18L12 13.875M8 18L4 13.875M8 18L8 11M8 6V8"
                stroke="#ffffff"
                stroke-width="1.5"
                stroke-linecap="round"
                stroke-linejoin="round"
              />
            </svg>
          </MenuButton>
          <MenuItems>
            <div class="menu-option">
              <MenuItem let:active class="menu-selection" title="Sort by IOU">
                <span
                  class:active
                  on:click={(e) => updateSorting('sortByIOU')}
                  on:keypress={(e) => updateSorting('sortByIOU')}
                  style={'display: flex;'}
                >
                  {#if sortBy.sortByIOU === 2}
                    <SortUp size={15} color="#ffffff" />
                  {:else if sortBy.sortByIOU === 1}
                    <SortDown size={15} color="#ffffff" />
                  {:else}
                    <span style="width:15px" />
                  {/if}
                  Sort by IOU
                </span>
              </MenuItem>
              <MenuItem let:active class="menu-selection" title="Sort by ID">
                <span
                  class:active
                  on:click={(e) => updateSorting('sortByID')}
                  on:keypress={(e) => updateSorting('sortByID')}
                  style={'display: flex;'}
                >
                  {#if sortBy.sortByID === 2}
                    <SortUp size={15} color="#ffffff" />
                  {:else if sortBy.sortByID === 1}
                    <SortDown size={15} color="#ffffff" />
                  {:else}
                    <span style="width:15px" />
                  {/if}
                  Sort by ID
                </span>
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
          imgInfo={$dataset['imgs'][img.data.imgId]}
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
  .tags-set {
    color: rgb(255, 255, 255);
    display: flex;
    align-items: center;
    gap: 3px;
    cursor: pointer;
  }

  .tag-list {
    display: flex;
    flex-direction: column;
  }

  .tags-input {
    background-color: transparent;
    color: rgb(255, 255, 255);
    height: 2rem;
    font-size: 14px;
    border: none;
    -webkit-box-align: center;
    align-items: center;
    font-weight: bold;
    width: 100%;
  }

  .tags-button {
    cursor: pointer;
    padding-right: 0.25rem;
    display: flex;
    -webkit-box-pack: center;
    place-content: center;
    flex-direction: column;
    border-bottom: none !important;
    background-color: rgb(38, 38, 38);
    color: rgb(179, 179, 179);
    user-select: none;
    margin: 0.25rem -0.5rem;
    padding-left: 0.5rem;
    height: 2rem;
    border-radius: 0px;
  }
  .tags-span {
    white-space: nowrap;
    text-overflow: ellipsis;
    overflow: hidden;
  }

  .panel-row-input {
    font-size: 14px;
    border-bottom: 1px solid rgb(255, 109, 5);
    position: relative;
    margin: 0.5rem 0px;
  }
  .panel-row {
    font-size: 14px;
    position: relative;
    margin: 0.5rem 0px;
  }
  .panel-contents {
    background-color: rgb(26, 26, 26);
    border: 1px solid rgb(13, 13, 13);
    border-radius: 2px;
    box-shadow: rgb(26, 26, 26) 0px 2px 20px;
    box-sizing: border-box;
    margin-top: 0.6rem;
    position: absolute;
    font-size: 14px;
    padding: 0px 0.5rem;
    width: 14rem;
  }

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

  :global(.collection-menu .tag-select) {
    padding: 0.25rem 1rem;
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
