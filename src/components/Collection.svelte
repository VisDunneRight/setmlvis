<script lang="ts">
import {dataset} from '../stores';
let selected = $dataset['yolos-base,'];
import DrawThumbnail from './vis/DrawThumbnail.svelte';
let imgHeight = 100;
console.log($dataset, selected);
</script>
<div class="collection-container" 
     style:width="100%" 
     style:height="40%">
  <div class="media-scroller">
  {#each Object.entries(selected) as [, arryList]}
    {#if !(Object.entries(arryList).length === 1 && 'FN' in arryList)}
      {#each Object.entries(arryList) as [name, obj]}
        {#if name !== 'FN'}
            <DrawThumbnail data={obj} height={imgHeight}/>
        {/if}
      {/each}
    {/if}
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