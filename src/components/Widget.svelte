<script lang="ts">
  import {
    height,
    windowWidth,
    menuWidth,
    openDetailView,
    dataset,
  } from '../stores';
  import { onMount } from 'svelte';
  import Menu from './Menu.svelte';
  // import DetailView from './DetailView.svelte'
  import SetVis from './SetVis.svelte';
  import Collection from './Collection.svelte';
  import DetailView from './DetailView.svelte';

  let div: HTMLDivElement;
  window.onclick = function (event: Event & { target: HTMLDivElement }) {
    if (
      event.target !== null &&
      event.target.getAttribute('id') === 'setvis-model-container'
    ) {
      $openDetailView = false;
    }
  };

  let folderName = '';
  $: if ($dataset['meta']) {
    folderName = $dataset['meta']['folderName'];
  }
  $: console.log($dataset);
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
        } else {
          $windowWidth = entry.contentRect.width;
        }
      }
    );
    resizeObserver.observe(div);
    return () => resizeObserver.unobserve(div);
  });
</script>

<!-- <header> -->
<link rel="stylesheet" href="../node_modules/svelte-material-ui/bare.css" />
<link
  rel="stylesheet"
  href="https://fonts.googleapis.com/icon?family=Material+Icons"
/>
<!-- Roboto -->
<link
  rel="stylesheet"
  href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,600,700"
/>
<!-- Roboto Mono -->
<link
  rel="stylesheet"
  href="https://fonts.googleapis.com/css?family=Roboto+Mono"
/>
<link
  rel="stylesheet"
  href="https://unpkg.com/@material/typography@14.0.0/dist/mdc.typography.css"
/>
<!-- </header> -->
<div class="widget-container" style:height="{$height}px" bind:this={div}>
  <Menu />
  <div
    class="vis-container"
    style:height="{$height}px"
    style:width="{$windowWidth - $menuWidth}px"
    style:left="{$menuWidth}px"
  >
    <SetVis />
    <Collection {folderName} />
  </div>
  <DetailView {folderName} />
</div>

<style>
  .widget-container {
    width: 100%;
    border: 1px solid rgb(226, 226, 226);
  }
  .vis-container {
    position: relative;
  }
</style>
