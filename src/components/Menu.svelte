<script lang="ts">
  import Group from './menuComp/Group.svelte';
  import { fly } from 'svelte/transition';
  import VisToggle from './vis/VisToggle.svelte';

  import { color } from '../ulit';
  import CheckAccordion from './detail/CheckAccordion.svelte';
  import Checked from '../assets/checked.svelte';
  import Unchecked from '../assets/unchecked.svelte';
  import {
    height,
    menuWidth,
    IOU,
    confidence,
    detectionSize,
    weightedConfidence,
    showWeightedConfidence,
    tags,
    showTags,
    dataset,
    selectedCol,
    barSelected,
    colSelected,
  } from '../stores';
  import type { ImgData, MenuItem } from '../types';
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

  menuMap['weightedconfidence'].updatefunction = function (
    values: [number, number]
  ) {
    if (values[0] > values[1]) {
      $weightedConfidence = [values[1], values[0]];
    } else {
      $weightedConfidence = values;
    }
  };
  menuMap['detectionSize'].updatefunction = function (
    values: [number, number]
  ) {
    $detectionSize = values;
  };
  function updateWConf() {
    $showWeightedConfidence = !$showWeightedConfidence;
  }
  //Set the starting value for the function to user passed value
  menuMap['truePositiveIOU'].value = $IOU;
  //https://iconsvg.xyz/

  function updateShowTags() {
    $showTags = !$showTags;
  }
  function updateTagSelection() {
    let selection: ImgData[] = [];
    Object.entries($dataset.models).forEach(([name, dataInfo]) => {
      dataInfo.forEach((dataRes) => {
        Object.entries(dataRes.detections).forEach(([type, info]) => {
          for (const tag of info.tags) {
            if (tag in $tags && $tags[tag].selected) {
              selection.push(info);
              break;
            }
          }
        });
      });
    });
    $selectedCol = selection;
  }
  function handleCheck(tagName: string) {
    $tags[tagName].selected = !$tags[tagName].selected;
    updateTagSelection();
    $barSelected = '';
    $colSelected = -1;
  }
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
    <!-- Add check  -->
    <VisToggle
      message={'WTD Confidence'}
      activeColor="blueviolet"
      inactiveColor="#540077"
      enabled={$showWeightedConfidence}
      update={updateWConf}
    />
    <div class="accordion-container">
      {#each menu as option}
        {#if option.name !== 'Weighted Confidence' && option.name !== 'Confidence'}
          <Group {option} />
        {:else if $showWeightedConfidence && option.name === 'Weighted Confidence'}
          <Group {option} />
        {:else if !$showWeightedConfidence && option.name === 'Confidence'}
          <Group {option} />
        {/if}
      {/each}
      <!-- on:click={(e) => updateImg(img)}
              on:keydown={(e) => updateImg(img)} -->
      <CheckAccordion
        check={$showTags === true ? 2 : 0}
        updateCheck={updateShowTags}
      >
        <span slot="head">Tags</span>
        <span slot="info">{Object.keys($tags).length}</span>
        <div slot="details">
          {#if Object.keys($tags).length > 0}
            {#each Object.entries($tags) as [name, tag], i}
              <div class="line">
                <span
                  class="checkmark"
                  on:click={(e) => handleCheck(name)}
                  on:keydown={(e) => handleCheck(name)}
                >
                  {#if tag.selected}
                    <Checked size={20} color={color[i % 10]} />
                  {:else}
                    <Unchecked size={20} color={color[i % 10]} />
                  {/if}
                  <span>{name}</span>
                </span>
                <span class="text-line">{tag.count}</span>
              </div>
            {/each}
          {:else}
            <p>No Tags</p>
          {/if}
        </div>
      </CheckAccordion>
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
    box-sizing: border-box;
  }
  .checkmark {
    cursor: pointer;
    align-items: center;
    display: flex;
    gap: 5px;
  }
  .text-line {
    padding-right: 10px;
  }
  .line {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #f4f4f4;
    padding: 2px;
  }
</style>
