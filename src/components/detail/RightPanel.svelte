<script lang="ts">
  import Accordion from './Accordion.svelte';
  import CheckAccordion from './CheckAccordion.svelte';
  import {
    selectedImg,
    selectedImgIdx,
    dataset,
    detectionSize,
    colorMap,
  } from '../../stores';
  import { color } from '../../ulit';

  function getAllDetections(models, selectedImg) {
    let detections = { 'Ground-Truth': [] };
    Object.entries(models).forEach((model) => {
      const names = model[0].split(',');
      if (names.length !== 2) {
        return;
      }

      detections[names[0]] = [];
      model[1].forEach((res) => {
        Object.entries(res.detections).forEach((detection) => {
          const obj = detection[1];
          if (obj.imgName === selectedImg.imgName) {
            detections[names[0]].push(obj);
          }
        });
      });
    });
    return detections;
  }

  $: allDetection = getAllDetections($dataset.models, $selectedImg);
</script>

<Accordion>
  <span slot="head">METADATA</span>
  <div slot="details">
    <p><b>Id:</b> {$selectedImg?.id}</p>
    <p><b>Name:</b> {$selectedImg?.imgName}</p>
    <p>
      <b>Width:</b>
      {$selectedImg?.imgSize[0]}, height: {$selectedImg?.imgSize[1]}
    </p>
  </div>
</Accordion>
<Accordion>
  <span slot="head">TAGS</span>
  <div slot="details">
    <p>We going to add tag information here.</p>
  </div>
</Accordion>

<Accordion open={true}>
  <span slot="head">LABELS</span>
  <div slot="details">
    {#each Object.entries(allDetection) as detection}
      {#if detection[1].length > 0 || detection[0] === 'Ground-Truth'}
        <CheckAccordion colorCheck={color[$colorMap[detection[0]]]}>
          <span slot="head">{detection[0]}</span>
          <span slot="info">{detection[1].length}</span>
          <div slot="details">
            {#each detection[1] as img}
              <p>id: {img.id}</p>
            {/each}
          </div>
        </CheckAccordion>
      {/if}
    {/each}
  </div>
</Accordion>

<style>
</style>
