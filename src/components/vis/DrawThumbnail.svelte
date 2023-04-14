
<script lang="ts">
  import type { ImgData } from '../../types';
  import {selectedImg, openDetailView} from '../../stores';
  export let data:ImgData;
  export let height:number;
  let imgWidth = data === undefined ? 0 : data.imgSize[0];
  let imgHeight = data === undefined ? 0 : data.imgSize[1];
  let imgRatio = imgWidth/imgHeight;
  let width = height*imgRatio;
  function selectImgData(){
    $selectedImg = data;
    $openDetailView = true;
  }

</script>
<div 
  class="media-element" 
  style="width:{width}px;height:{height}px" 
  >
  {#if data}
  <button on:click={()=>{selectImgData()}}>
  <img height="{height}px" src="data/twentyFiveImages/images/{data.imgName}" alt="selected Figure"/>
  <svg width={width} height={height}>
    {#each Object.entries(data.boxes) as [, box]}
      <rect
       x={box[1]*width}
       y={box[2]*width/imgRatio}
       width={(box[3] - box[1])*width}
       height={(box[4] - box[2])*width/imgRatio}
       fill="none"
       stroke="green"
      />
    {/each}
  </svg>
</button>
  {/if}
</div>
<style>

  svg, img {
    position: absolute;
    left: 0px;
    top: 0px;
  }
  
  .media-element{
    border-radius: 0.25rem;
    /* flex: 1; */
    background-color: black;
    position: relative;    
  }
</style>