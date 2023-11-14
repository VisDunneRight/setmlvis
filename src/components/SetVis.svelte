<script lang="ts">
  import * as d3 from 'd3';
  import {
    IOU,
    dataset,
    topHeight,
    selectedCol,
    colorMap,
    confidence,
    breakdown,
    windowWidth,
    menuWidth,
  } from '../stores';
  import type { DataRes, ImgData, Data } from '../types';
  import { color, colorTypes } from '../ulit';
  import SetColumn from './vis/setColumn.svelte';
  import VisButton from './vis/VisButton.svelte';
  import ColorLegend from './vis/ColorLegend.svelte';
  import Tooltip from './vis/Tooltip.svelte';
  import VisToggle from './vis/VisToggle.svelte';

  $: mouseOverI = -1;
  $: colSelected = -1;
  $: barSelected = '';

  const metaModel = $dataset['meta']['modelNames'];
  const padding = { top: 20, right: 15, bottom: 22, left: 10 };
  const config = {
    colGap: 3,
    maxTextSize: 120,
    ytickCount: 12,
    circleRadius: 9,
    circleGap: 3,
    setSpacing: 80,
    breakdownY: 70,
  };
  let setFliter: Array<number> = [];
  let setData: Array<ColumnType> = [];
  let showEmptySets = false;
  let showDifferenceSet = true;

  metaModel.forEach((model: string, i: number) => {
    $colorMap[model] = i % color.length;
    setFliter.push(1);
  });

  // let winWidth = $windowWidth - $menuWidth;
  let winHeight = $topHeight;
  //Calculate the false postive and true positive
  type ColumnType = {
    name: string;
    models: Array<number>;
    modelRange: Array<number>;
    truePos: number;
    falsePos: number;
    falseNeg: number;
    type: {
      duplicate: number;
      low_threshold: number;
      far_away: number;
      wrong_class: number;
    };
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
        return 2;
      } else {
        return 1;
      }
    } else {
      return 0;
    }
  }

  function contained(firstModels: string, secondModels: string) {
    const firstList = firstModels.split(',');
    const secondList = secondModels.split(',');

    for (const name of firstList) {
      if (!secondList.includes(name)) {
        return false;
      }
    }
    return true;
  }

  function updateData(
    dset: Data,
    iou: number,
    confid: [number, number],
    breakdown: boolean,
    showEmptySets: boolean,
    showDifferenceSet: boolean
  ) {
    if (showDifferenceSet) {
      let data: Array<ColumnType> = [];
      Object.entries(dset.models).forEach(([name, arryList]) => {
        //Generates Circle information
        let models: Array<number> = [];
        let modelRange: Array<number> = [];
        metaModel.forEach((model: string, ind: number) => {
          const nameArry = name.split(',');
          if (modelExists(nameArry, model)) {
            models.push(2);
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
          falseNeg: 0,
          type: {
            duplicate: 0,
            low_threshold: 0,
            far_away: 0,
            wrong_class: 0,
          },
          data: arryList,
        };
        //determine the number of postives
        arryList.forEach((obj) => {
          Object.entries(obj.detections).forEach(([type, info]) => {
            let positivity = determinePostivity(info, confid, iou);
            if (positivity === 2) {
              column['truePos'] += 1;
            } else if (positivity === 1) {
              column['falsePos'] += 1;
              column.type[info.category] += 1;
            }
          });
          // column['falseNeg'] += obj.FN.values.length;
        });
        if (
          showEmptySets ||
          column.truePos + column.falsePos + column.falseNeg > 0
        ) {
          data.push(column);
        }
      });
      return data;
    } else {
      let totalModels: { [key: string]: DataRes[] } = {};
      Object.entries(dset.models).forEach(([nameFirst, arryListFirst]) => {
        totalModels[nameFirst] = [...arryListFirst];
        Object.entries(dset.models).forEach(([nameSecond, arryListSecond]) => {
          if (nameFirst !== nameSecond && contained(nameFirst, nameSecond)) {
            totalModels[nameFirst] = totalModels[nameFirst].concat([
              ...arryListSecond,
            ]);
          }
        });
      });

      let data: Array<ColumnType> = [];
      Object.entries(totalModels).forEach(([name, arryList]) => {
        //Generates Circle information
        if (name.split(',').length !== 2) {
          return;
        }
        let models: Array<number> = [];
        let modelRange: Array<number> = [];
        metaModel.forEach((model: string, ind: number) => {
          const nameArry = name.split(',');
          if (modelExists(nameArry, model)) {
            models.push(2);
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
          falseNeg: 0,
          type: {
            duplicate: 0,
            low_threshold: 0,
            far_away: 0,
            wrong_class: 0,
          },
          data: arryList,
        };
        //determine the number of postives
        arryList.forEach((obj) => {
          Object.entries(obj.detections).forEach(([type, info]) => {
            let positivity = determinePostivity(info, confid, iou);
            if (positivity === 2) {
              column['truePos'] += 1;
            } else if (positivity === 1) {
              column['falsePos'] += 1;
              column.type[info.category] += 1;
            }
          });
          column['falseNeg'] += obj.FN.values.length;
          console.log(name, obj.FN);
        });
        if (
          showEmptySets ||
          column.truePos + column.falsePos + column.falseNeg > 0
        ) {
          data.push(column);
        }
      });
      return data;
    }
  }

  $: data = updateData(
    $dataset,
    $IOU,
    $confidence,
    $breakdown,
    showEmptySets,
    showDifferenceSet
  );

  $: maxY = d3.max(data, (d) => d.truePos + d.falsePos + d.falseNeg);
  $: extentY = [0, maxY === undefined ? 100 : maxY];

  $: y = d3
    .scaleLinear()
    .domain(extentY)
    .range([modelRow(metaModel.length), padding.top]);

  let yTicks: Array<number> = [];
  $: step = Math.ceil((extentY[1] - extentY[0]) / config.ytickCount / 10) * 10;

  function updateTicks(extentY: number[]) {
    yTicks = [];
    for (let i = 0; i <= config.ytickCount; i++) {
      yTicks.push(i * step + extentY[0]);
    }
  }
  $: updateTicks(extentY);

  //Helper functions
  function columnSpacing(i: number) {
    return padding.left + i * (config.colGap + config.circleRadius * 2);
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
          if (determinePostivity(info, $confidence, $IOU) === 2) {
            selection.push(info);
          }
        });
      });
    } else if (type === 'false positive') {
      model.data.forEach((obj) => {
        Object.entries(obj.detections).forEach(([type, info]) => {
          if (determinePostivity(info, $confidence, $IOU) === 1) {
            selection.push(info);
          }
        });
      });
    }
    colSelected = ind;
    barSelected = type;
    $selectedCol = selection;
  }
  function clearSet() {
    setData = [];
  }

  function selectSet() {
    setData = [];
    let setRange: Array<number> = [];
    setFliter.forEach((name, ind) => {
      if (name > 0) {
        setRange.push(ind);
      }
    });

    let column: ColumnType = {
      name: 'Group',
      models: setFliter,
      modelRange: setRange,
      truePos: 0,
      falsePos: 0,
      type: {
        duplicate: 0,
        low_threshold: 0,
        far_away: 0,
        wrong_class: 0,
      },
      data: [],
    };
    setData.push(column);
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
        ele.data.forEach((item) => {
          setData[0].data.push(item);
        });
        setData[0].falsePos += ele.falsePos;
        setData[0].truePos += ele.truePos;
        const keys = Object.keys(ele.type) as Array<keyof typeof ele.type>;
        for (const key of keys) {
          setData[0].type[key] += ele.type[key];
        }
      }
    });
  }

  function updateSetFilters(idx: number, value: number) {
    setFliter[idx] = value;
  }
  function updateSelection(iou: number, confidence: [number, number]) {
    selectSet();
  }

  function updateShowEmptySets(
    event: Event & { currentTarget: HTMLInputElement }
  ) {
    showEmptySets = event?.currentTarget?.checked;
  }

  function updateshowDifferenceSet(
    event: Event & { currentTarget: HTMLInputElement }
  ) {
    showDifferenceSet = event?.currentTarget?.checked;
  }

  $: svgWidth = columnSpacing(setData.length + 1 + data.length);
  $: if (setData.length > 0) {
    updateSelection($IOU, $confidence);
  }
  let evt: CustomEvent<any>;
  let hideTooltip = true;
  const leftPanelWidth =
    config.maxTextSize +
    config.colGap +
    config.circleRadius +
    config.setSpacing;
</script>

<div class="set-vis-container" style:width="100%" style:height="{winHeight}px">
  <div class="left-panel">
    <svg
      style:width="{leftPanelWidth}px"
      style:height="{winHeight}px"
      style="Max-Width:{leftPanelWidth}px"
      class="svg-container"
    >
      <g class="model-names">
        {#each metaModel as modelName, i}
          <rect
            x={padding.left}
            y={modelRow(i) - config.circleRadius}
            width={config.maxTextSize}
            height={config.circleRadius * 2}
            fill={color[$colorMap[modelName]]}
            opacity=".25"
          />
          <text
            x={padding.left + config.maxTextSize - config.colGap}
            y={modelRow(i)}
            text-anchor="end"
            alignment-baseline="middle"
            class="model-text"
          >
            <title>{modelName}</title>
            {modelName.length * 7.5 < config.maxTextSize
              ? modelName
              : modelName.slice(0, config.maxTextSize / 7 - 3) + '...'}</text
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
        <VisButton
          x={setSpacing(1) - config.circleRadius}
          y={modelRow(metaModel.length - 1) - 25}
          update={selectSet}
          text={'Confirm'}
        />

        <VisButton
          x={setSpacing(-1) - config.circleRadius}
          y={modelRow(metaModel.length - 1) - 25}
          update={clearSet}
          text={'X'}
        />
      </g>
      <g class="color-legend">
        <g>
          <g transform="translate(2 {config.breakdownY - 6})">
            <svg
              fill="#000000"
              height="10px"
              width="10px"
              version="1.1"
              id="Capa_1"
              xmlns="http://www.w3.org/2000/svg"
              xmlns:xlink="http://www.w3.org/1999/xlink"
              viewBox="0 0 490 490"
              xml:space="preserve"
              ><g
                id="SVGRepo_iconCarrier"
                transform={$breakdown ? 'rotate(90 250 250)' : ''}
              >
                <path d="M15.541,490V0l458.917,245.009L15.541,490z" />
              </g></svg
            >
          </g>
          <text
            x={16}
            y={config.breakdownY}
            text-anchor="start"
            alignment-baseline="middle"
            font-weight="bold"
            on:mousedown={() => {
              $breakdown = !$breakdown;
            }}
            class="model-text pointer">{'Breakdown'}</text
          >
        </g>
        {#if $breakdown}
          <ColorLegend
            x={20}
            y={config.breakdownY + 1 * 15}
            color={colorTypes['low_threshold']}
            name={'low_threshold'}
            type={'low_threshold'}
          />
          <ColorLegend
            x={20}
            y={config.breakdownY + 2 * 15}
            color={colorTypes['wrong_class']}
            name={'Wrong Class'}
            type={'wrong_class'}
          />
          <ColorLegend
            x={20}
            y={config.breakdownY + 3 * 15}
            color={colorTypes['far_away']}
            name={'Far Away'}
            type={'far_away'}
          />
          <ColorLegend
            x={20}
            y={config.breakdownY + 4 * 15}
            color={colorTypes['duplicate']}
            name={'Duplicate'}
            type={'duplicate'}
          />
        {/if}
      </g>
      <g class="y-axis">
        <text
          x={leftPanelWidth - 24}
          y="15"
          text-anchor="end"
          alignment-baseline="middle">Detections</text
        >
        {#each yTicks as tick}
          <g
            class="tick tick-{tick}"
            transform="translate({leftPanelWidth}, {y(tick)})"
          >
            <text x="-3" alignment-baseline="middle">{tick}</text>
          </g>
        {/each}
      </g>
    </svg>
    <div style:position="absolute" style:left="3px" style:top="5px">
      <VisToggle
        message="Empty Set"
        enabled={showEmptySets}
        update={updateShowEmptySets}
      />
    </div>
    <div style:position="absolute" style:left="3px" style:top="32px">
      <VisToggle
        message="Difference"
        enabled={showDifferenceSet}
        update={updateshowDifferenceSet}
      />
    </div>
  </div>
  <div
    class="set-vis"
    style:left="{leftPanelWidth}px"
    style:width="{$windowWidth - $menuWidth - leftPanelWidth}px"
    style:height="{winHeight}px"
    style="Max-Width:{$windowWidth - $menuWidth - leftPanelWidth}px"
  >
    <svg
      style:width="{svgWidth}px"
      style:height="{winHeight}px"
      style="Max-Width:{svgWidth}px"
      class="svg-container"
    >
      {#each yTicks as tick}
        <g
          class="tick tick-{tick}"
          transform="translate({columnSpacing(0) -
            config.circleRadius -
            config.circleGap}, {y(tick)})"
        >
          <line
            x2={(setData.length > 0 ? setData.length : 0) *
              (config.colGap + config.circleRadius * 2)}
          />
        </g>
        <g
          class="tick tick-{tick}"
          transform="translate({columnSpacing(
            setData.length > 0 ? setData.length + 1 : 0
          ) -
            config.circleRadius -
            config.circleGap}, {y(tick)})"
        >
          <line x2={columnSpacing(data.length > 0 ? data.length + 1 : 0)} />
        </g>
      {/each}
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
            breakdown={$breakdown}
            on:mousemove={(event) => {
              evt = event;
              hideTooltip = false;
            }}
            on:mouseout={() => (hideTooltip = true)}
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
            mouseOverI = i + (setData.length > 0 ? setData.length + 1 : 0);
          }}
          on:focus={() => {
            mouseOverI = i + (setData.length > 0 ? setData.length + 1 : 0);
          }}
          on:mouseout={() => {
            mouseOverI = -1;
          }}
          on:blur={() => {
            mouseOverI = -1;
          }}
          transform="translate({columnSpacing(
            i + (setData.length > 0 ? setData.length + 1 : 0)
          ) - config.circleRadius}, {0})"
        >
          <SetColumn
            {col}
            i={i + (setData.length > 0 ? setData.length + 1 : 0)}
            {config}
            {mouseOverI}
            {winHeight}
            {padding}
            {modelRow}
            {y}
            {selectModel}
            colSelected={colSelected +
              (setData.length > 0 ? setData.length + 1 : 0)}
            {barSelected}
            breakdown={$breakdown}
            on:mousemove={(event) => {
              evt = event;
              hideTooltip = false;
            }}
            on:mouseout={() => (hideTooltip = true)}
          />
        </g>
      {/each}
    </svg>

    {#if hideTooltip !== true}
      <Tooltip
        {evt}
        let:detail
        width={$windowWidth - $menuWidth - leftPanelWidth}
      >
        <!-- For the tooltip, do another data join because the hover event only has the data from the geography data -->
        {@const tooltipData = { ...detail.props }}
        {#each Object.entries(tooltipData) as [key, value]}
          {@const keyCapitalized = key.replace(/^\w/, (d) => d.toUpperCase())}
          <div class="row"><span>{keyCapitalized}:</span> {value}</div>
        {/each}
      </Tooltip>
    {/if}
  </div>
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
  .set-vis {
    position: absolute;
    overflow-x: scroll;
    overflow-y: hidden;
  }
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
    position: absolute;
    min-width: 200px;
    border: 1px solid rgb(226, 226, 226);
  }
  .set-vis::-webkit-scrollbar {
    height: 6px;
  }

  .set-vis::-webkit-scrollbar-track {
    background-color: #e4e4e4;
    border-radius: 100px;
  }

  .set-vis::-webkit-scrollbar-thumb {
    background-color: #d4aa70;
    border-radius: 100px;
  }
</style>
