<script lang="ts">
  import { selectedCol } from '../stores';
  import DrawThumbnail from './vis/DrawThumbnail.svelte';
  let imgHeight = 100;
</script>
<div class="collection-container" 
     style:width="100%" 
     style:height="40%">
  <div class="media-scroller">
    {#each $selectedCol as imgInfo}
      <DrawThumbnail data={imgInfo} height={imgHeight}/>
    {/each}
  </div>
</div>


<style>
  .media-scroller {
    position: absolute;
    width: 100%;
    height: 100%;
    display: flex;
    flex-wrap: wrap;
    gap: .5rem;
    overflow: auto;
  }

  .collection-container {
    position:absolute;
    background-color: lightgray;
    min-width: 200px;
    border: 1px solid rgb(226, 226, 226);
    /* overflow-y: scroll; */
  }
</style>