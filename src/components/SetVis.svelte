<script lang="ts">
  import * as d3 from 'd3';
  import {
    IOU,
    dataset,
    height,
    selectedCol,
    colorMap,
    confidence,
  } from '../stores';
  import type { DataRes, ImgData, Data } from '../types';
  import { color } from '../ulit';
  import SetColumn from './vis/setColumn.svelte';

  $: mouseOverI = -1;
  $: colSelected = -1;
  $: barSelected = '';
  const metaModel = $dataset['meta']['modelNames'];
  const padding = { top: 20, right: 15, bottom: 20, left: 10 };
  const config = {
    colGap: 3,
    maxTextSize: 120,
    ytickCount: 12,
    circleRadius: 9,
    circleGap: 3,
    setSpacing: 80,
  };
  let setFliter: Array<number> = [];
  let setData: Array<ColumnType> = [];

  $: metaModel.forEach((model: string, i: number) => {
    colorMap[model] = i % color.length;
    setFliter.push(1);
  });

  // let winWidth = $windowWidth - $menuWidth;
  let winHeight = $height * 0.6;
  //Calculate the false postive and true positive
  type ColumnType = {
    name: string;
    models: Array<number>;
    modelRange: Array<number>;
    truePos: number;
    falsePos: number;
    data: DataRes[];
  };

  let data: Array<ColumnType> = [];
  function modelExists(nameArry: Array<string>, model: string) {
    let matchFound = false;
    nameArry.forEach((name) => {
      if (name === model) {
        matchFound = true;
        return true;
      }
    });
    if (matchFound) {
      return true;
    } else {
      return false;
    }
  }
  function determinePostivity(
    info: ImgData,
    confid: [number, number],
    iou: number
  ) {
    const avg = d3.mean(info.confidence, (d: number) => d);
    if (
      info !== undefined &&
      avg !== undefined &&
      avg >= confid[0] &&
      avg <= confid[1]
    ) {
      if (info !== undefined && info.iouGT >= iou) {
        return true;
      } else {
        return false;
      }
    } else {
      return false;
    }
  }

  function updateData(dset: Data, iou: number, confid: [number, number]) {
    let data: Array<ColumnType> = [];

    Object.entries(dset.models).forEach(([name, arryList]) => {
      //Generates Circle information
      let models: Array<number> = [];
      let modelRange: Array<number> = [];
      metaModel.forEach((model: string, ind: number) => {
        const nameArry = name.split(',');
        if (modelExists(nameArry, model)) {
          models.push(1);
          modelRange.push(ind);
        } else {
          models.push(0);
        }
      });
      let column: ColumnType = {
        name: name,
        models: models,
        modelRange: modelRange,
        truePos: 0,
        falsePos: 0,
        data: arryList,
      };
      //determine the number of postives
      arryList.forEach((obj) => {
        Object.entries(obj.detections).forEach(([type, info]) => {
          if (determinePostivity(info, confid, iou)) {
            column['truePos'] += 1;
          } else {
            column['falsePos'] += 1;
          }
        });
      });
      data.push(column);
    });
    return data;
  }

  $: data = updateData($dataset, $IOU, $confidence);

  $: maxY = d3.max(data, (d) => d.truePos + d.falsePos);
  $: extentY = [0, maxY === undefined ? 100 : maxY];

  $: y = d3
    .scaleLinear()
    .domain(extentY)
    .range([modelRow(metaModel.length), padding.top]);

  let yTicks: Array<number> = [];
  $: step = Math.ceil((extentY[1] - extentY[0]) / config.ytickCount / 5) * 5;

  function updateTicks(extentY: number[]) {
    for (let i = 0; i <= config.ytickCount; i++) {
      yTicks.push(i * step + extentY[0]);
    }
  }
  $: updateTicks(extentY);

  //Helper functions
  function columnSpacing(i: number) {
    return (
      padding.left +
      config.maxTextSize +
      config.colGap +
      config.circleRadius +
      config.setSpacing +
      i * (config.colGap + config.circleRadius * 2)
    );
  }
  function modelRow(j: number) {
    return (
      -padding.bottom +
      winHeight -
      j * (config.circleGap + config.circleRadius * 2)
    );
  }
  function setSpacing(i: number) {
    return (
      padding.left +
      config.maxTextSize +
      config.circleRadius +
      config.colGap * 2 +
      i * (config.circleRadius * 2 + config.colGap)
    );
  }

  function selectModel(model: ColumnType, ind: number, type: string) {
    let selection: ImgData[] = [];
    if (type === 'true positive') {
      model.data.forEach((obj) => {
        Object.entries(obj.detections).forEach(([type, info]) => {
          if (determinePostivity(info, $confidence, $IOU)) {
            selection.push(info);
          }
        });
      });
    } else if (type === 'false positive') {
      model.data.forEach((obj) => {
        Object.entries(obj.detections).forEach(([type, info]) => {
          if (!determinePostivity(info, $confidence, $IOU)) {
            selection.push(info);
          }
        });
      });
    }
    colSelected = ind;
    barSelected = type;
    $selectedCol = selection;
  }

  function selectSet() {
    setData = [];
    data.forEach((ele) => {
      const nameArry = ele.name.split(',');
      let match = true;
      setFliter.forEach((filter, idx) => {
        const modelName = metaModel[idx];
        if (filter === 0) {
          if (modelExists(nameArry, modelName)) {
            match = false;
            return;
          }
        } else if (filter === 2) {
          if (!modelExists(nameArry, modelName)) {
            match = false;
            return;
          }
        }
      });
      if (match) {
        setData.push(ele);
      }
    });
  }

  function updateSetFilters(idx: number, value: number) {
    setFliter[idx] = value;
  }
</script>

<div class="set-vis-container" style:width="100%" style:height="{winHeight}px">
  <svg width="100%" height={winHeight} class="svg-container">
    <g class="model-names">
      {#each metaModel as modelName, i}
        <rect
          x={padding.left}
          y={modelRow(i) - config.circleRadius}
          width={config.maxTextSize}
          height={config.circleRadius * 2}
          fill={color[colorMap[modelName]]}
          opacity=".25"
        />
        <text
          x={padding.left + config.maxTextSize - config.colGap}
          y={modelRow(i)}
          text-anchor="end"
          alignment-baseline="middle"
          class="model-text"
          >{modelName.length * 7 < config.maxTextSize
            ? modelName
            : modelName.slice(0, config.maxTextSize / 7) + '...'}</text
        >
        <circle
          cx={setSpacing(0)}
          cy={modelRow(i)}
          r={config.circleRadius}
          fill={'#f0f0f0'}
          stroke={setFliter[i] === 0 ? '#757de8' : '#636363'}
          stroke-width={setFliter[i] === 0 ? '4px' : '2px'}
          on:mousedown={() => updateSetFilters(i, 0)}
        />
        <g on:mousedown={() => updateSetFilters(i, 1)}>
          <circle
            cx={setSpacing(1)}
            cy={modelRow(i)}
            r={config.circleRadius - 1}
            fill={'#f0f0f0'}
          />
          <path
            d="M {setSpacing(1)} {modelRow(i) + config.circleRadius}
                   a{config.circleRadius - 1}, {config.circleRadius - 1} 
                   0 0,0 0,
                   {-config.circleRadius * 2}"
            fill={'#636363'}
          />
          <circle
            cx={setSpacing(1)}
            cy={modelRow(i)}
            r={config.circleRadius - 1}
            fill="none"
            stroke={setFliter[i] === 1 ? '#757de8' : '#636363'}
            stroke-width={setFliter[i] === 1 ? '4px' : '2px'}
          />
        </g>
        <circle
          cx={setSpacing(2)}
          cy={modelRow(i)}
          r={config.circleRadius - 1}
          fill={'#636363'}
          stroke={setFliter[i] === 2 ? '#757de8' : '#636363'}
          stroke-width={setFliter[i] === 2 ? '4px' : '2px'}
          on:mousedown={() => updateSetFilters(i, 2)}
        />
      {/each}
      <line
        x1={setSpacing(3) - config.colGap}
        y1={modelRow(0) + config.circleRadius}
        x2={setSpacing(3) - config.colGap}
        y2={modelRow(metaModel.length - 1) - config.circleRadius}
        stroke-width="4"
        stroke-linecap="round"
        stroke="#9e9e9e"
      />
      <g on:mousedown={() => selectSet()} class="pointer">
        <rect
          x={setSpacing(0) - config.circleRadius}
          y={modelRow(metaModel.length - 1) - 40}
          width={setSpacing(2) -
            setSpacing(0) +
            config.circleRadius +
            2 * config.colGap}
          height={20}
          rx={4}
          fill="#bdbdbd"
        />
        <text
          x={setSpacing(0) - config.circleRadius + 4}
          y={modelRow(metaModel.length - 1) - 30}
          text-anchor="start"
          alignment-baseline="middle"
          class="model-text">Confirm</text
        >
      </g>
    </g>
    <g class="y-axis">
      <text
        x={columnSpacing(0) - 30}
        y="15"
        text-anchor="end"
        alignment-baseline="middle">Detections</text
      >
      {#each yTicks as tick}
        <g
          class="tick tick-{tick}"
          transform="translate({columnSpacing(0) -
            config.circleRadius -
            config.circleGap}, {y(tick)})"
        >
          <line x2="100%" />
          <text x="-3" alignment-baseline="middle">{tick}</text>
        </g>
      {/each}
    </g>

    {#each setData as col, i}
      <g
        class="column"
        on:mouseover={() => {
          mouseOverI = i;
        }}
        on:focus={() => {
          mouseOverI = i;
        }}
        on:mouseout={() => {
          mouseOverI = -1;
        }}
        on:blur={() => {
          mouseOverI = -1;
        }}
        transform="translate({columnSpacing(i) - config.circleRadius}, {0})"
      >
        <SetColumn
          {col}
          {i}
          {config}
          {mouseOverI}
          {winHeight}
          {padding}
          {modelRow}
          {y}
          {selectModel}
          {colSelected}
          {barSelected}
        />
      </g>
    {/each}
  {#if setData.length > 0}
    <line
      x1={columnSpacing(setData.length)}
      y1={modelRow(0) + config.circleRadius}
      x2={columnSpacing(setData.length)}
      y2={modelRow(metaModel.length - 1) - config.circleRadius}
      stroke-width="4"
      stroke-linecap="round"
      stroke="#9e9e9e"
    />
  {/if}

    {#each data as col, i}
      <g
        class="column"
        on:mouseover={() => {
          mouseOverI = i + (setData.length > 0 ? setData.length + 1: 0);
        }}
        on:focus={() => {
          mouseOverI = i +(setData.length > 0 ? setData.length + 1: 0);
        }}
        on:mouseout={() => {
          mouseOverI = -1;
        }}
        on:blur={() => {
          mouseOverI = -1;
        }}
        transform="translate({columnSpacing(i + (setData.length > 0 ? setData.length + 1: 0)) - config.circleRadius}, {0})"
      >
        <SetColumn
          {col}
          i = {i + (setData.length > 0 ? setData.length + 1: 0)}
          {config}
          {mouseOverI}
          {winHeight}
          {padding}
          {modelRow}
          {y}
          {selectModel}
          colSelected = {colSelected + (setData.length > 0 ? setData.length + 1: 0)}
          {barSelected}
        />
      </g>
    {/each}
  </svg>
</div>

<style>
  /* .model-names {

  }
  .model-text {

  }
  .y-axis {

  }
  .column {

  } */
  .selected {
    border: 1px solid #636363;
  }

  .pointer {
    cursor: pointer;
  }
  .pointer:hover {
    fill: #283593;
  }

  .tick {
    font-family: Helvetica, Arial;
    font-size: 0.725em;
    font-weight: 200;
  }

  .tick line {
    stroke: #e2e2e2;
    stroke-dasharray: 2;
  }

  .tick text {
    fill: #636363;
    text-anchor: end;
  }
  .svg-container {
    position: absolute;
    left: 0px;
    top: 0px;
  }
  .set-vis-container {
    position: relative;
    min-width: 200px;
    border: 1px solid rgb(226, 226, 226);
  }
</style>
