<script lang="ts">
  import {height, dataset, windowWidth, menuWidth} from '../stores';
  import { onMount } from 'svelte';
  import Menu from './Menu.svelte'
  import DetailView from './DetailView.svelte'
  import SetVis from './SetVis.svelte'
  import Collection from './Collection.svelte'

  let div: HTMLDivElement;
  let gridHeight: number;
  onMount(() => {
    // Adapted from https://blog.sethcorker.com/question/how-do-you-use-the-resize-observer-api-in-svelte/
    // and https://developer.mozilla.org/en-US/docs/Web/API/ResizeObserver
    const resizeObserver = new ResizeObserver(
      (entries: ResizeObserverEntry[]) => {
        if (entries.length !== 1) {
          return;
        }
        const entry: ResizeObserverEntry = entries[0];
        if (entry.contentBoxSize) {
          const contentBoxSize = Array.isArray(entry.contentBoxSize)
            ? entry.contentBoxSize[0]
            : entry.contentBoxSize;
          $windowWidth = contentBoxSize.inlineSize;
          gridHeight = contentBoxSize.blockSize;
        } else {
          $windowWidth = entry.contentRect.width;
          gridHeight = entry.contentRect.height;
        }
      }
    );
    resizeObserver.observe(div);
    return () => resizeObserver.unobserve(div);
  });

  console.log($dataset)
</script>
<div class="widget-container" style:height="{$height}px" bind:this={div}>
<Menu/>
  <div class="vis-container" 
        style:height="{$height}px" 
        style:width="{$windowWidth - $menuWidth}px" 
        style:left="{$menuWidth}px">
    <DetailView/>
    <SetVis/>
    <Collection/>
  </div>
</div>


<style>
  .widget-container {
    width:100%;
    border: 1px solid rgb(226, 226, 226);
  }
  .vis-container{
    position: relative;
  }
</style>