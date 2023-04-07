<script lang="ts">
  import {menuWidth, windowWidth, selectedImg, height} from '../stores';
  import DrawTextbox from './vis/DrawTextbox.svelte';
  // Try loading the figure and finding its position
  // Add svg/bounding box
  // Add Labels to indicate confidence interval
  $:compWidth = ($windowWidth - $menuWidth)/2;
  $:compHeight = $height*0.6;
  $:imgWidth = $selectedImg === undefined ? 0 : $selectedImg.imgSize[0];
  $:imgHeight = $selectedImg === undefined ? 0 : $selectedImg.imgSize[1];
  $:imgRatio = imgWidth/imgHeight;
  function capitalize(str:string): string {
      return str.charAt(0).toUpperCase() + str.slice(1);
  }
  function showConfidence(className:string, num:number): string{
    return capitalize(className) + ': ' + ((num*100)/100).toFixed(2)
  }

</script>
<div class="detail-container" style:width="{compWidth}px" style:height="{compHeight}px">
  {#if $selectedImg}
    <img width="{compWidth}px" src="data/fiveImages/images/{$selectedImg.imgName}" alt="selected Figure"/>
    <svg width={compWidth} height={compHeight}>
      {#each Object.entries($selectedImg.boxes) as [, box]}
        <DrawTextbox 
          x={box[1]*compWidth} 
          y={box[2]*compWidth/imgRatio}
          backgroundColor="green"
          size={13}
          text={showConfidence(box[0], box[5])}
          />
        <rect
        x={box[1]*compWidth}
        y={box[2]*compWidth/imgRatio}
        width={(box[3] - box[1])*compWidth}
        height={(box[4] - box[2])*compWidth/imgRatio}
        fill="none"
        stroke="green"
        />
      {/each}
    </svg>
  {/if}
</div>


<style>
  /* .small {
    font: 13px sans-serif;
    fill: white;
  } */
  svg, img {
    position: absolute;
    left: 0px;
    top: 0px;
  }
  .detail-container {
    position: absolute;
    right:0px;
    min-width: 200px;
    border: 1px solid rgb(226, 226, 226);
  }
</style>