<script lang="ts">
  import {menuWidth, windowWidth, dataset, height} from '../stores';
  import DrawTextbox from './vis/DrawTextbox.svelte';
  let selected = $dataset['conditional-detr-resnet-50,'][1][2];
  // Try loading the figure and finding its position
  // Add svg/bounding box
  // Add Labels to indicate confidence interval
  $:compWidth = ($windowWidth - $menuWidth)/2;
  $:compHeight = $height*0.6;
  let imgWidth = selected.imgSize[0];
  let imgHeight = selected.imgSize[1];
  let imgRatio = imgWidth/imgHeight;
  function capitalize(str:string) {
      return str.charAt(0).toUpperCase() + str.slice(1);
  }
  function showConfidence(className:string, num:number){
    return capitalize(className) + ': ' + ((num*100)/100).toFixed(2)
  }

</script>
<div class="detail-container" style:width="{compWidth}px" style:height="{compHeight}px">
  <img width="{compWidth}px" src="data/fiveImages/images/{selected.imgName}" alt="selected Figure"/>
  <svg width={compWidth} height={compHeight}>
    {#each Object.entries(selected.boxes) as [name, box]}
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
</div>


<style>
  .small {
    font: 13px sans-serif;
    fill: white;
  }
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