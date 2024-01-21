<script lang="ts">
  import CheckAccordion from './CheckAccordion.svelte';
  import Checked from '../../assets/checked.svelte';
  import Unchecked from '../../assets/unchecked.svelte';
  import { color } from '../../ulit';
  import { colorMap } from '../../stores';
  import type {
    Detect,
    GroundTruthObj,
    GroundTruth,
    Detection,
  } from '../../types';
  export let groundTruth: GroundTruthObj;
  export let detectionBoxes: Detection;
  export let type: number;
  export let updateEntireGroundSet: (type: number) => void;
  export let updateGroundImg: (gt: GroundTruth) => void;
  export let updateEntireSet: (name: string, type: number) => void;
  export let updateImg: (imgSelected: Detect) => void;

  $: groundTruthSe = groundTruth.data.filter((x) => x.type <= type);
  $: console.log('Work', type, groundTruth, groundTruthSe, detectionBoxes);
</script>

{#if groundTruthSe.length > 0}
  <CheckAccordion
    colorCheck={color[$colorMap['ground_truth']]}
    check={groundTruth.selected[type]}
    updateCheck={() => updateEntireGroundSet(type)}
  >
    <span slot="head">Ground Truth</span>
    <span slot="info">{groundTruthSe.length}</span>
    <div slot="details">
      {#each groundTruthSe as detection}
        {#if detection.type <= type}
          <div class="line">
            <span
              class="checkmark"
              on:click={(e) => updateGroundImg(detection)}
              on:keydown={(e) => updateGroundImg(detection)}
            >
              {#if detection.selected === true}
                <Checked size={20} color={color[$colorMap['ground_truth']]} />
              {:else}
                <Unchecked size={20} color={color[$colorMap['ground_truth']]} />
              {/if}
            </span>
            <p>ID: {detection.id}</p>
            {#if type === 0}
              <p>Type: {detection.shape[0]}</p>
              <p>x: {detection.shape[1]}</p>
              <p>y: {detection.shape[2]}</p>
              <p>x2: {detection.shape[3]}</p>
              <p>y2: {detection.shape[4]}</p>
            {/if}
          </div>
        {/if}
      {/each}
    </div>
  </CheckAccordion>
{/if}
{#each Object.entries(detectionBoxes) as detection}
  {@const detectData = detection[1].data.filter((x) => x.type <= type)}
  {@const detectDataCount = detectData.filter((x) => x.selected).length}
  {#if detectData.length > 0}
    <CheckAccordion
      colorCheck={color[$colorMap[detection[0]]]}
      check={detection[1].selected[type]}
      updateCheck={() => updateEntireSet(detection[0], type)}
    >
      <span slot="head">{detection[0]}</span>
      <span slot="info"
        >{detectDataCount > 0
          ? detectDataCount + ' of ' + detectData.length
          : detectData.length}</span
      >
      <div slot="details">
        {#each detectData as img}
          {#if img.type <= type}
            <div class="line">
              <span
                class="checkmark"
                on:click={(e) => updateImg(img)}
                on:keydown={(e) => updateImg(img)}
              >
                {#if img.selected === true}
                  <Checked size={20} color={color[$colorMap[detection[0]]]} />
                {:else}
                  <Unchecked size={20} color={color[$colorMap[detection[0]]]} />
                {/if}
              </span>
              <p>Confidence: {img.data[5]}</p>
            </div>
          {/if}
        {/each}
      </div>
    </CheckAccordion>
  {/if}
{/each}

<style>
  .checkmark {
    cursor: pointer;
  }
  .line {
    display: flex;
    gap: 0.4em;
  }
</style>
