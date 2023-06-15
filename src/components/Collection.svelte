<script lang="ts">
  import { selectedCol, windowWidth, menuWidth } from '../stores';
  import type { ImgData, ImgInfo } from '../types';
  import DrawThumbnail from './vis/DrawThumbnail.svelte';
  export let folderName = '';
  let imgHeight = 100;
  let gap = 4;

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
    imgHeight,
    $windowWidth - $menuWidth - 8,
    gap
  );
</script>

<div class="collection-container" style:width="100%" style:height="40%">
  <div class="media-scroller" id ="scrollBar">
    {#each imgInfo as img, i}
      <DrawThumbnail
        left={img.left}
        top={img.top}
        data={img.data}
        height={img.height}
        index={i}
        {folderName}
      />
    {/each}
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

  .collection-container {
    position: absolute;
    background-color: lightgray;
    min-width: 200px;
    top:360px;
    border: 1px solid rgb(226, 226, 226);
    /* overflow-y: scroll; */
  }
</style>
