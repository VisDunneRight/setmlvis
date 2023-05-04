<script lang="ts">
  import * as d3 from 'd3';
  import { IOU, dataset, height, selectedCol, colorMap } from '../stores';
  import type { DataRes, ImgData } from '../types';
  import { color } from '../ulit';

  const metaModel = $dataset['meta']['modelNames'];
  const padding = { top: 20, right: 15, bottom: 20, left: 10 };
  const config = {
    colGap: 3,
    maxTextSize: 120,
    ytickCount: 12,
    circleRadius: 9,
    circleGap: 3,
  };

  metaModel.forEach((model:string, i:number)=>{
    colorMap[model] = i % color.length;
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
  $:console.log(IOU)
  Object.entries($dataset).forEach(([name, arryList]) => {
    if (name === 'meta') {
      return;
    }
    //Generates Circle information
    let column: ColumnType = {};
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
    column['name'] = name;
    column['models'] = models;
    column['modelRange'] = modelRange;
    column['truePos'] = 0;
    column['falsePos'] = 0;
    column['data'] = arryList;
    //determine the number of postives
    arryList.forEach((obj) => {
      Object.entries(obj).forEach(([type, info]) => {
        if (type !== 'FN') {
          // console.log(info);
          const avg = d3.mean(info?.confidence ?? 1.0, (d: string) => +d);
          if (avg !== undefined && avg > $IOU) {
            column['truePos'] += 1;
          } else {
            column['falsePos'] += 1;
          }
        }
      });
    });
    data.push(column);
  });
  const maxY = d3.max(data, (d) => d.truePos + d.falsePos);
  let extentY: [number, number] = [0, maxY === undefined ? 100 : maxY];

  $: y = d3
    .scaleLinear()
    .domain(extentY)
    .range([modelRow(metaModel.length), padding.top]);

  let yTicks: Array<number> = [];
  let step = (extentY[1] - extentY[0])/config.ytickCount;
  step = Math.ceil(step/5) * 5;
  $:console.log(step);
  for(let i = 0; i <= config.ytickCount; i++){
    yTicks.push(i*step + extentY[0])
  }
  // for (
  //   let i = extentY[0];
  //   i < Math.ceil(extentY[1] / config.ytickCount) + 1;
  //   i += 1
  // ) {
  //   yTicks.push(i * config.ytickCount);
  // }

  //Helper functions
  function columnSpacing(i: number) {
    return (
      padding.left +
      config.maxTextSize +
      config.colGap +
      config.circleRadius +
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

  function selectModel(model: ColumnType, type: string) {
    let selection: ImgData[] = [];
    if (type === 'true positive') {
      model.data.forEach((obj) => {
        Object.entries(obj).forEach(([type, info]) => {
          if (type !== 'FN') {
            const avg = d3.mean(info.confidence, (d: string) => +d);
            if (avg !== undefined && avg >= $IOU) {
              selection.push(info);
            }
          }
        });
      });
    } else if (type === 'false positive') {
      model.data.forEach((obj) => {
        Object.entries(obj).forEach(([type, info]) => {
          if (type !== 'FN') {
            const avg = d3.mean(info.confidence, (d: string) => +d);
            if (avg !== undefined && avg <= $IOU) {
              selection.push(info);
            }
          }
        });
      });
    }

    $selectedCol = selection;
    console.log($selectedCol);
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
      {/each}
    </g>
    <g class="y-axis">
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
    <g class="column">
      {#each data as col, i}
        <g class="circles">
          {#each col.models as mod, j}
            <circle
              cx={columnSpacing(i)}
              cy={modelRow(j)}
              r={config.circleRadius}
              fill={mod ? '#636363' : '#f0f0f0'}
            />
          {/each}
        </g>
        {#if col.modelRange.length > 1}
          <line
            x1={columnSpacing(i)}
            y1={modelRow(col.modelRange[0])}
            x2={columnSpacing(i)}
            y2={modelRow(col.modelRange[col.modelRange.length - 1])}
            stroke-width="4"
            stroke="#636363"
          />
        {/if}
        <rect
          on:mousedown={() => selectModel(col, 'true positive')}
          x={columnSpacing(i) - config.circleRadius}
          y={y(col.truePos)}
          width={config.circleRadius * 2}
          height={y(0) - y(col.truePos)}
          fill="#377eb8"
        />
        <rect
          on:mousedown={() => selectModel(col, 'false positive')}
          x={columnSpacing(i) - config.circleRadius}
          y={y(col.falsePos + col.truePos)}
          width={config.circleRadius * 2}
          height={y(col.truePos) - y(col.falsePos + col.truePos)}
          fill="#e41a1c"
        />
      {/each}
    </g>
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
