<script lang="ts">
  import Accordion from './Accordion.svelte';
  import Labels from './Labels.svelte';
  import {
    selectedImg,
    dataset,
    selectedImgBoxes,
    selectedCol,
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
    DetectObject,
  } from '../../types';

  $: labelType = 2;

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

  //0 = Selected
  //1 = Filtered
  //2 = All
  function getAllDetections(
    models: Models,
    imgs: Array<Image>,
    ground_truth: Array<ObjectDect>,
    selectedCol: Array<ImgData>,
    selectedImg: ImgData | undefined
  ) {
    let groundTruth: GroundTruthObj = {
      data: [],
      selected: [0, 0, 0],
    };
    let detections: Detection = {};
    if (selectedImg === undefined) {
      return;
    }

    //Find all the ground truth
    let img = imgs[selectedImg.imgId];
    if (img) {
      for (let gt of img.ground_truth) {
        groundTruth.data.push({
          id: gt,
          shape: ground_truth[gt],
          selected: false,
          type: 2,
        });
      }
    }

    //Find all instances of the models
    Object.entries(models).forEach((model) => {
      const names = model[0].split(',');
      model[1].forEach((res) => {
        Object.entries(res.detections).forEach((detection) => {
          const obj = detection[1];
          if (obj.imgId === selectedImg.imgId) {
            for (const namestr of names) {
              if (namestr === '') {
                continue;
              }
              if (!(namestr in detections)) {
                detections[namestr] = { data: [], selected: [0, 0, 0] };
              }

              detections[namestr].data.push({
                data: obj.boxes[namestr],
                selected: false,
                id: obj.id,
                type: 2,
              });
            }
          }
        });
      });
    });

    let allDetections = { ground_truth: groundTruth, detections: detections };

    //Grab groundtruth from the filtered data
    selectedCol.forEach((col) => {
      if (col.imgId === selectedImg.imgId && col.gtShape) {
        for (let gt of allDetections.ground_truth.data) {
          if (checkArray(col.gtShape, gt.shape)) {
            if (col.id === selectedImg.id) {
              gt.type = 0;
            } else {
              gt.type = 1;
            }
          }
        }
      }
    });

    //Grab objections from the filtered data
    let ids: Array<string> = [];
    selectedCol.forEach((col) => {
      if (col.imgId === selectedImg.imgId) {
        ids.push(col.id);
      }
    });

    for (const namstr in allDetections.detections) {
      allDetections.detections[namstr].data.forEach((detect) => {
        if (detect.id === selectedImg.id) {
          detect.type = 0;
        } else if (ids.includes(detect.id)) {
          detect.type = 1;
        }
      });
    }

    return allDetections;
  }
  function updateImgBox(selectImgBox: DetectObject) {
    let count = [0, 0, 0];
    const data = selectImgBox.data;
    for (const detect of data) {
      if (detect.selected) {
        for (let i = detect.type; i <= 2; i++) {
          count[i]++;
        }
      }
    }

    for (let i = 0; i <= 2; i++) {
      if (count[i] === 0) {
        selectImgBox.selected[i] = 0;
      } else if (count[i] < data.filter((x) => x.type <= i).length) {
        selectImgBox.selected[i] = 1;
      } else {
        selectImgBox.selected[i] = 2;
      }
    }
  }
  function updateImgBoxes() {
    if ($selectedImgBoxes) {
      for (const name in $selectedImgBoxes['detections']) {
        updateImgBox($selectedImgBoxes['detections'][name]);
      }
    }
    $selectedImgBoxes = $selectedImgBoxes;
  }

  function updateGroundBoxes() {
    if ($selectedImgBoxes) {
      let count = [0, 0, 0];
      const data = $selectedImgBoxes['ground_truth'].data;
      for (const detect of data) {
        if (detect.selected) {
          for (let i = detect.type; i <= 2; i++) {
            count[i]++;
          }
        }
      }
      for (let i = 0; i <= 2; i++) {
        if (count[i] === 0) {
          $selectedImgBoxes['ground_truth'].selected[i] = 0;
        } else if (count[i] < data.filter((x) => x.type <= i).length) {
          $selectedImgBoxes['ground_truth'].selected[i] = 1;
        } else {
          $selectedImgBoxes['ground_truth'].selected[i] = 2;
        }
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
  function updateEntireSet(name: string, type: number) {
    if ($selectedImgBoxes) {
      let newSetting =
        $selectedImgBoxes['detections'][name].selected[type] > 0 ? 0 : 2;
      for (let i = type; i >= 0; i--) {
        $selectedImgBoxes['detections'][name].selected[i] = newSetting;
        for (let data of $selectedImgBoxes['detections'][name].data) {
          if (data.type === i) {
            data.selected =
              $selectedImgBoxes['detections'][name].selected[i] === 2;
          }
        }
      }
      updateImgBox($selectedImgBoxes['detections'][name]);
      $selectedImgBoxes = $selectedImgBoxes;
    }
  }
  function updateEntireGroundSet(type: number) {
    if ($selectedImgBoxes) {
      let newSetting =
        $selectedImgBoxes['ground_truth'].selected[type] > 0 ? 0 : 2;
      for (let i = type; i >= 0; i--) {
        $selectedImgBoxes['ground_truth'].selected[i] = newSetting;
        for (let data of $selectedImgBoxes['ground_truth'].data) {
          if (data.type === i) {
            data.selected =
              $selectedImgBoxes['ground_truth'].selected[type] === 2;
          }
        }
      }
      updateGroundBoxes();
      $selectedImgBoxes = $selectedImgBoxes;
    }
  }
  function onLabelChange(selId: string) {
    let newLabeltype = -1;
    if (selId === 'selected') {
      newLabeltype = 1;
    } else if (selId === 'filtered') {
      newLabeltype = 2;
    } else if (selId === 'all') {
      newLabeltype = 3;
    }
    if (newLabeltype === labelType) {
      return;
    } else {
      labelType = newLabeltype;
    }
  }

  let meta: Image = undefined;
  $: if ($selectedImg) {
    meta = $dataset.imgs[$selectedImg?.imgId];
    $selectedImgBoxes = getAllDetections(
      $dataset.models,
      $dataset.imgs,
      $dataset.ground_truth,
      $selectedCol,
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
    {#if $selectedImg && $selectedImg.tags.length > 0}
      {#each $selectedImg.tags as tag}
        <p>{tag}</p>
      {/each}
    {:else}
      <p>No Tags</p>
    {/if}
  </div>
</Accordion>

{#if $selectedImgBoxes}
  {#if labelType === 1}
    <Accordion open={true}>
      <span slot="head" class="label-selection">
        <span> LABELS </span>
        <span class="label-blob">
          <input
            type="radio"
            name="payment"
            id="selected"
            on:click={() => {
              onLabelChange('selected');
            }}
            checked={labelType === 1}
          />
          <label for="selected" title="selected Image">
            <i class="fa fa-circle-o" aria-hidden="true" />
          </label>
          <input
            type="radio"
            name="payment"
            id="filtered"
            on:click={() => {
              onLabelChange('filtered');
            }}
            checked={false}
          />
          <label for="filtered" title="from selected collection">
            <i class="fa fa-dot-circle-o" aria-hidden="true" />
          </label>
          <input
            type="radio"
            name="payment"
            id="all"
            on:click={() => {
              onLabelChange('all');
            }}
            checked={false}
          />
          <label for="all" title="Across all detections">
            <i class="fa fa-circle" aria-hidden="true" />
            <!-- <span>All</span> -->
          </label>
        </span>
      </span>
      <div slot="details" id="label-select">
        <Labels
          groundTruth={$selectedImgBoxes['ground_truth']}
          detectionBoxes={$selectedImgBoxes['detections']}
          type={0}
          {updateEntireGroundSet}
          {updateGroundImg}
          {updateImg}
          {updateEntireSet}
        />
      </div>
    </Accordion>
  {:else if labelType === 2}
    <Accordion open={true}>
      <span slot="head" class="label-selection">
        <span> LABELS </span>
        <span class="label-blob">
          <input
            type="radio"
            name="payment"
            id="selected"
            on:click={() => {
              onLabelChange('selected');
            }}
            checked={false}
          />
          <label for="selected" title="selected Image">
            <i class="fa fa-circle-o" aria-hidden="true" />
          </label>
          <input
            type="radio"
            name="payment"
            id="filtered"
            on:click={() => {
              onLabelChange('filtered');
            }}
            checked={labelType === 2}
          />
          <label for="filtered" title="from selected collection">
            <i class="fa fa-dot-circle-o" aria-hidden="true" />
          </label>
          <input
            type="radio"
            name="payment"
            id="all"
            on:click={() => {
              onLabelChange('all');
            }}
            checked={false}
          />
          <label for="all" title="Across all detections">
            <i class="fa fa-circle" aria-hidden="true" />
            <!-- <span>All</span> -->
          </label>
        </span>
      </span>
      <div slot="details" id="label-select">
        <Labels
          groundTruth={$selectedImgBoxes['ground_truth']}
          detectionBoxes={$selectedImgBoxes['detections']}
          type={1}
          {updateEntireGroundSet}
          {updateGroundImg}
          {updateImg}
          {updateEntireSet}
        />
      </div>
    </Accordion>
  {:else}
    <Accordion open={true}>
      <span slot="head" class="label-selection">
        <span> LABELS </span>
        <span class="label-blob">
          <input
            type="radio"
            name="payment"
            id="selected"
            on:click={() => {
              onLabelChange('selected');
            }}
            checked={false}
          />
          <label for="selected" title="selected Image">
            <i class="fa fa-circle-o" aria-hidden="true" />
          </label>
          <input
            type="radio"
            name="payment"
            id="filtered"
            on:click={() => {
              onLabelChange('filtered');
            }}
            checked={false}
          />
          <label for="filtered" title="from selected collection">
            <i class="fa fa-dot-circle-o" aria-hidden="true" />
          </label>
          <input
            type="radio"
            name="payment"
            id="all"
            on:click={() => {
              onLabelChange('all');
            }}
            checked={labelType === 3}
          />
          <label for="all" title="Across all detections">
            <i class="fa fa-circle" aria-hidden="true" />
            <!-- <span>All</span> -->
          </label>
        </span>
      </span>
      <div slot="details" id="label-select">
        <Labels
          groundTruth={$selectedImgBoxes['ground_truth']}
          detectionBoxes={$selectedImgBoxes['detections']}
          type={2}
          {updateEntireGroundSet}
          {updateGroundImg}
          {updateImg}
          {updateEntireSet}
        />
      </div>
    </Accordion>
  {/if}
{/if}

<style>
  .label-blob {
    display: flex;
  }

  .label-selection {
    display: flex;
    gap: 5px;
  }

  label {
    margin: auto;
  }
  .fa {
    font-size: 16px;
    padding-left: 4px;
    padding-right: 4px;
    border-radius: 3px;
    cursor: pointer;
  }
  input[type='radio']:checked + label {
    background-color: #0e0f0f;
    color: #ffffff;
    border-radius: 30%;
    box-shadow: 0 15px 45px rgb(15, 16, 15, 0.2);
  }
  input[type='radio'] {
    -webkit-appearance: none;
  }
</style>
