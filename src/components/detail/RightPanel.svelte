<script lang="ts">
  import Accordion from './Accordion.svelte';
  import CheckAccordion from './CheckAccordion.svelte';
  import Checked from '../../assets/checked.svelte';
  import Unchecked from '../../assets/unchecked.svelte';
  import {
    selectedImg,
    dataset,
    colorMap,
    selectedImgBoxes,
  } from '../../stores';
  import type {
    Image,
    Models,
    ObjectDect,
    ImgData,
    Detect,
    GroundTruthObj,
    GroundTruth,
    Detection,
  } from '../../types';
  import { color } from '../../ulit';

  function checkArray(a: Array<any>, b: Array<any>) {
    if (a.length !== b.length) {
      return false;
    }
    for (let i = 0; i < a.length; i++) {
      if (a[i] !== b[i]) {
        return false;
      }
    }
    return true;
  }

  function getAllDetections(
    models: Models,
    imgs: Array<Image>,
    ground_truth: Array<ObjectDect>,
    selectedImg: ImgData | undefined
  ) {
    let groundTruth: GroundTruthObj = { data: [], selected: 0 };
    let detections: Detection = {};
    if (selectedImg === undefined) {
      return;
    }

    let img = imgs[selectedImg.imgId];
    if (selectedImg.gtShape) {
      console.log(selectedImg.gtShape, img.ground_truth);
      for (let gt of img.ground_truth) {
        if (!checkArray(selectedImg.gtShape, ground_truth[gt])) {
          groundTruth.data.push({
            id: gt,
            shape: ground_truth[gt],
            selected: false,
          });
        }
      }
    }
    Object.entries(models).forEach((model) => {
      const names = model[0].split(',');

      model[1].forEach((res) => {
        Object.entries(res.detections).forEach((detection) => {
          const obj = detection[1];
          if (obj.imgId === selectedImg.imgId) {
            for (const namestr of names) {
              if (namestr === '' || !(namestr in selectedImg.boxes)) {
                continue;
              }
              if (!(namestr in detections)) {
                detections[namestr] = { data: [], selected: 0 };
              }
              if (!checkArray(selectedImg.boxes[namestr], obj.boxes[namestr])) {
                detections[namestr].data.push({
                  data: obj.boxes[namestr],
                  selected: false,
                  id: obj.id,
                });
              }
            }
          }
        });
      });
    });
    return { ground_truth: groundTruth, detections: detections };
  }

  function updateImgBoxes() {
    if ($selectedImgBoxes) {
      for (const name in $selectedImgBoxes['detections']) {
        let count = 0;
        const data = $selectedImgBoxes['detections'][name].data;
        for (const detect of data) {
          if (detect.selected) {
            count++;
          }
        }
        if (count === 0) {
          $selectedImgBoxes['detections'][name].selected = 0;
        } else if (count < data.length) {
          $selectedImgBoxes['detections'][name].selected = 1;
        } else {
          $selectedImgBoxes['detections'][name].selected = 2;
        }
      }
    }
    $selectedImgBoxes = $selectedImgBoxes;
  }
  function updateGroundBoxes() {
    if ($selectedImgBoxes) {
      let count = 0;
      const data = $selectedImgBoxes['ground_truth'].data;
      for (const detect of data) {
        if (detect.selected) {
          count++;
        }
      }
      if (count === 0) {
        $selectedImgBoxes['ground_truth'].selected = 0;
      } else if (count < data.length) {
        $selectedImgBoxes['ground_truth'].selected = 1;
      } else {
        $selectedImgBoxes['ground_truth'].selected = 2;
      }
    }
    $selectedImgBoxes = $selectedImgBoxes;
  }

  function updateImg(imgSelected: Detect) {
    imgSelected.selected = !imgSelected.selected;
    updateImgBoxes();
  }
  function updateGroundImg(gt: GroundTruth) {
    gt.selected = !gt.selected;
    updateGroundBoxes();
  }
  function updateEntireSet(name: string) {
    if ($selectedImgBoxes) {
      $selectedImgBoxes['detections'][name].selected =
        $selectedImgBoxes['detections'][name].selected > 0 ? 0 : 2;
      for (let data of $selectedImgBoxes['detections'][name].data) {
        data.selected = $selectedImgBoxes['detections'][name].selected === 2;
      }
      $selectedImgBoxes = $selectedImgBoxes;
    }
  }
  function updateEntireGroundSet() {
    if ($selectedImgBoxes) {
      $selectedImgBoxes['ground_truth'].selected =
        $selectedImgBoxes['ground_truth'].selected > 0 ? 0 : 2;
      for (let data of $selectedImgBoxes['ground_truth'].data) {
        data.selected = $selectedImgBoxes['ground_truth'].selected === 2;
      }
      $selectedImgBoxes = $selectedImgBoxes;
    }
  }
  let meta: Image = undefined;
  $: if ($selectedImg) {
    meta = $dataset.imgs[$selectedImg?.imgId];
    $selectedImgBoxes = getAllDetections(
      $dataset.models,
      $dataset.imgs,
      $dataset.ground_truth,
      $selectedImg
    );
  }
</script>

<Accordion>
  <span slot="head">METADATA</span>
  <div slot="details">
    <p><b>Id:</b> {$selectedImg?.imgId}</p>
    <p><b>Name:</b> {meta?.imgName}</p>
    <p>
      <b>Width:</b>
      {meta?.imgSize[0]}, height: {meta?.imgSize[1]}
    </p>
  </div>
</Accordion>
<Accordion>
  <span slot="head">TAGS</span>
  <div slot="details">
    <p>We going to add tag information here.</p>
  </div>
</Accordion>
<Accordion>
  <span slot="head">SELECTED LABELS</span>
  <div slot="details">
    {#if $selectedImg}
      <CheckAccordion colorCheck={color[$colorMap['ground_truth']]}>
        <span slot="head">Ground Truth</span>
        <span slot="info">{1}</span>
        <div slot="details">
          <p>Type: {$selectedImg.gtShape[0]}</p>
          <p>x: {$selectedImg.gtShape[1]}</p>
          <p>y: {$selectedImg.gtShape[2]}</p>
          <p>x2: {$selectedImg.gtShape[3]}</p>
          <p>y2: {$selectedImg.gtShape[4]}</p>
        </div>
      </CheckAccordion>
      {#each Object.entries($selectedImg.boxes) as detection}
        <CheckAccordion colorCheck={color[$colorMap[detection[0]]]} check={0}>
          <span slot="head">{detection[0]}</span>
          <span slot="info">{1}</span>
          <div slot="details">
            <div class="line">
              <p>Confidence: {detection[1][5]}</p>
            </div>
          </div>
        </CheckAccordion>
      {/each}
    {/if}
  </div>
</Accordion>

<Accordion open={true}>
  <span slot="head">ALL LABELS</span>
  <div slot="details">
    {#if $selectedImgBoxes}
      {#if $selectedImgBoxes['ground_truth'].data.length > 0}
        <CheckAccordion
          colorCheck={color[$colorMap['ground_truth']]}
          check={$selectedImgBoxes['ground_truth'].selected}
          updateCheck={updateEntireGroundSet}
        >
          <span slot="head">Ground Truth</span>
          <span slot="info"
            >{$selectedImgBoxes['ground_truth'].data.length}</span
          >
          <div slot="details">
            {#each $selectedImgBoxes['ground_truth'].data as detection}
              <div class="line">
                <span
                  class="checkmark"
                  on:click={(e) => updateGroundImg(detection)}
                  on:keydown={(e) => updateGroundImg(detection)}
                >
                  {#if detection.selected === true}
                    <Checked
                      size={20}
                      color={color[$colorMap['ground_truth']]}
                    />
                  {:else}
                    <Unchecked
                      size={20}
                      color={color[$colorMap['ground_truth']]}
                    />
                  {/if}
                </span>
                <p>ID: {detection.id}</p>
              </div>
            {/each}
          </div>
        </CheckAccordion>
      {/if}
      {#each Object.entries($selectedImgBoxes['detections']) as detection}
        {#if detection[1].data.length > 0}
          <CheckAccordion
            colorCheck={color[$colorMap[detection[0]]]}
            check={detection[1].selected}
            updateCheck={() => updateEntireSet(detection[0])}
          >
            <span slot="head">{detection[0]}</span>
            <span slot="info">{detection[1].data.length}</span>
            <div slot="details">
              {#each detection[1].data as img}
                <div class="line">
                  <span
                    class="checkmark"
                    on:click={(e) => updateImg(img)}
                    on:keydown={(e) => updateImg(img)}
                  >
                    {#if img.selected === true}
                      <Checked
                        size={20}
                        color={color[$colorMap[detection[0]]]}
                      />
                    {:else}
                      <Unchecked
                        size={20}
                        color={color[$colorMap[detection[0]]]}
                      />
                    {/if}
                  </span>
                  <p>Confidence: {img.data[5]}</p>
                </div>
              {/each}
            </div>
          </CheckAccordion>
        {/if}
      {/each}
    {/if}
  </div>
</Accordion>

<style>
  .checkmark {
    cursor: pointer;
  }
  .line {
    display: flex;
    gap: 0.4em;
  }
</style>
