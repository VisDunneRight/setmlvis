<script lang="ts">
  import Group from './menuComp/Group.svelte';
  import { fly } from 'svelte/transition';
  import { height, menuWidth, IOU, confidence, detectionSize } from '../stores';
  import type { MenuItem } from '../types';
  import rawMenu from '../menu.json';
  const menu = rawMenu as MenuItem[];

  let menuOpen = true;
  function openMenu(value: boolean) {
    if (value) {
      $menuWidth = 200;
    } else {
      $menuWidth = 0;
    }
    menuOpen = value;
  }
  let menuMap: Record<string, MenuItem> = {};

  menu.forEach((menuItem) => {
    menuMap[menuItem.id] = menuItem;
  });

  menuMap['truePositiveIOU'].updatefunction = function (value: number) {
    $IOU = value;
  };

  menuMap['confidence'].updatefunction = function (values: [number, number]) {
    if (values[0] > values[1]) {
      $confidence = [values[1], values[0]];
    } else {
      $confidence = values;
    }
  };
  menuMap['detectionSize'].updatefunction = function (
    values: [number, number]
  ) {
    $detectionSize = values;
  };
  //Set the starting value for the function to user passed value
  menuMap['truePositiveIOU'].value = $IOU;
  //https://iconsvg.xyz/
</script>

{#if menuOpen === true}
  <div
    transition:fly={{ x: -200, duration: 2000 }}
    class="menu-container {!menuOpen ? 'hide' : ''}"
    style:width="{$menuWidth}px"
    style:height="{$height}px"
  >
    <div class="menu-buttons">
      <button class="close-button" on:click={() => openMenu(false)}>
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          stroke="#000000"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <path d="M11 17l-5-5 5-5M18 17l-5-5 5-5" />
        </svg>
      </button>
    </div>
    <div class="accordion-container">
      <Group groups={menu} />
    </div>
  </div>
{:else}
  <button class="open-button" on:click={() => openMenu(true)}>
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="#000000"
      stroke-width="2"
      stroke-linecap="round"
      stroke-linejoin="round"
    >
      <path d="M13 17l5-5-5-5M6 17l5-5-5-5" />
    </svg>
  </button>
{/if}

<style>
  .open-button {
    padding: 0px;
    height: 25px;
    left: 0px;
    position: absolute;
    background-color: white;
    border: 1px solid gray;
    border-radius: 3px;
    margin: 2px;
    z-index: 1;
  }
  .close-button {
    padding: 0px;
    height: 25px;
    right: 0px;
    position: absolute;
    background-color: white;
    border: 1px solid gray;
    border-radius: 3px;
    margin: 2px;
  }
  .menu-buttons {
    height: 28px;
  }
  .hide {
    display: none;
  }
  .menu-container {
    min-width: 200px;
    z-index: 2;
    position: relative;
    float: left;
    border: 1px solid rgb(226, 226, 226);
    padding: 0px 4px 0px 4px;
  }
</style>
