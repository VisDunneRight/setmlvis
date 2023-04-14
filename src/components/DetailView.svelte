<script lang="ts">
  import {menuWidth, windowWidth, selectedImg, height, openDetailView} from '../stores';
  import DrawTextbox from './vis/DrawTextbox.svelte';

  // Try loading the figure and finding its position
  // Add svg/bounding box
  // Add Labels to indicate confidence interval
  $:compWidth = $windowWidth * .95;
  $:compHeight = $height * .9;
  $:imgWidth = $selectedImg === undefined ? 0 : $selectedImg.imgSize[0];
  $:imgHeight = $selectedImg === undefined ? 0 : $selectedImg.imgSize[1];
  function capitalize(str:string): string {
      return str.charAt(0).toUpperCase() + str.slice(1);
  }
  function showConfidence(className:string, num:number): string{
    return capitalize(className) + ': ' + ((num*100)/100).toFixed(2)
  }

  function calculateAspectRatioFit(srcWidth:number, srcHeight:number,
                                   maxWidth:number, maxHeight:number) {
    var ratio = Math.min(maxWidth / srcWidth, maxHeight / srcHeight);
    return { width: srcWidth*ratio, height: srcHeight*ratio };
  }

  $:newImg = calculateAspectRatioFit(imgWidth, imgHeight, compWidth, compHeight);

</script>

<div id="model" class="modal {$openDetailView ? 'modalon': ''}">
  <div id="setvis-model-container" class="modal-container">
    <div class="modal-window">
      <div class="detail-container" style:width="{compWidth}px" style:height="{compHeight}px">
        {#if $selectedImg}
         <div style:width="{newImg.width}px" style:height="{newImg.height}px" 
              style="align-self: center;position: absolute;">
            <img 
                width="{newImg.width}px" 
                height="{newImg.height}" 
                src="data/twentyFiveImages/images/{$selectedImg.imgName}" alt="selected Figure"/>
              <svg width={newImg.width} height={newImg.height}>
                {#each Object.entries($selectedImg.boxes) as [, box]}
                  <DrawTextbox 
                    x={box[1]*newImg.width} 
                    y={box[2]*newImg.height}
                    backgroundColor="green"
                    size={13}
                    text={showConfidence(box[0], box[5])}
                    />
                  <rect
                  x={box[1]*newImg.width}
                  y={box[2]*newImg.height}
                  width={(box[3] - box[1])*newImg.width}
                  height={(box[4] - box[2])*newImg.height}
                  fill="none"
                  stroke="green"
                  />
              {/each}
            </svg>
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


 .modal-container{
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
  svg, img {
    position:absolute;
    left:0px;
    right:0px;
  }
  .detail-container {
    -webkit-box-flex: 1;
    flex-grow: 1;
    width: 1px;
    position: relative;
    overflow: visible;
    display: flex;
    flex-direction: column;
  }
</style>