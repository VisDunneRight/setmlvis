<script>
  import { colorTypes } from '../../ulit';
  import { createEventDispatcher } from 'svelte';

  export let col;
  export let i;
  export let config;
  export let mouseOverI;
  export let winHeight;
  export let padding;
  export let modelRow;
  export let y;
  export let selectModel;
  export let colSelected;
  export let barSelected;
  export let breakdown;
  export let maxY;

  const dispatch = createEventDispatcher();
  let duplicate = 0;
  let far_away = 0;
  let wrong_class = 0;
  let low_threshold = 0;
  let truePos = 0;
  let falsePos = 0;
  let falseNeg = 0;
  let scaled = false;

  $: if (col.truePos + col.falsePos + col.falseNeg > maxY) {
    let newMax = col.truePos + col.falsePos + col.falseNeg;
    falseNeg = (col.falseNeg / newMax) * maxY;
    truePos = (col.truePos / newMax) * maxY;
    falsePos = (col.falsePos / newMax) * maxY;
    duplicate = truePos + (col.type.duplicate / newMax) * maxY;
    far_away = duplicate + (col.type.far_away / newMax) * maxY;
    wrong_class = far_away + (col.type.wrong_class / newMax) * maxY;
    low_threshold = wrong_class + (col.type.low_threshold / newMax) * maxY;
    scaled = true;
  } else {
    truePos = col.truePos;
    falsePos = col.falsePos;
    falseNeg = col.falseNeg;
    duplicate = col.truePos + col.type.duplicate;
    far_away = duplicate + col.type.far_away;
    wrong_class = far_away + col.type.wrong_class;
    low_threshold = wrong_class + col.type.low_threshold;
    scaled = false;
  }
</script>

{#if colSelected === i}
  {@const offsetY = 4}
  {@const offsetX = 3}
  {#if barSelected === 'true positive'}
    <rect
      x={-offsetX}
      y={y(truePos) - offsetY}
      width={config.circleRadius * 2 + 2 * offsetX}
      height={y(0) - y(truePos) + offsetY * 2}
      class={'group'}
      ry={8}
    />
  {:else if barSelected === 'false positive'}
    <rect
      x={-offsetX}
      y={y(falsePos + truePos) - offsetY}
      width={config.circleRadius * 2 + 2 * offsetX}
      height={y(truePos) - y(falsePos + truePos) + offsetY * 2}
      class={'group'}
      ry={8}
    />
  {/if}
{/if}

<rect
  x={0}
  y={config.circleRadius}
  width={config.circleRadius * 2}
  height={winHeight - padding.top + 4}
  class={mouseOverI === i
    ? 'hightlight'
    : col.name === 'Group'
    ? 'group'
    : 'background-bar'}
  ry={col.name === 'Group' ? 8 : 0}
/>

<g class="circles">
  {#each col.models as mod, j}
    {#if col.name !== 'Group'}
      <circle
        cx={config.circleRadius}
        cy={modelRow(j)}
        r={config.circleRadius}
        fill={mod ? '#636363' : '#f0f0f0'}
      />
    {:else if mod === 2 || mod === 0}
      <circle
        cx={config.circleRadius}
        cy={modelRow(j)}
        r={config.circleRadius}
        fill={mod ? '#636363' : '#f0f0f0'}
        stroke={'#636363'}
        stroke-width={'2px'}
      />
    {:else}
      <g>
        <circle
          cx={config.circleRadius}
          cy={modelRow(j)}
          r={config.circleRadius - 1}
          fill={'#f0f0f0'}
        />
        <path
          d="M {config.circleRadius} {modelRow(j) + config.circleRadius}
                  a{config.circleRadius - 1}, {config.circleRadius - 1} 
                  0 0,0 0,
                  {-config.circleRadius * 2}"
          fill={'#636363'}
        />
        <circle
          cx={config.circleRadius}
          cy={modelRow(j)}
          r={config.circleRadius - 1}
          fill="none"
          stroke={'#636363'}
          stroke-width={'2px'}
        />
      </g>
    {/if}
  {/each}
</g>

{#if col.modelRange.length > 1 && col.name !== 'Group'}
  <line
    x1={config.circleRadius}
    y1={modelRow(col.modelRange[0])}
    x2={config.circleRadius}
    y2={modelRow(col.modelRange[col.modelRange.length - 1])}
    stroke-width="4"
    stroke="#636363"
  />
{/if}

<rect
  on:mousedown={() => selectModel(col, i, 'true positive')}
  x={0}
  y={y(truePos)}
  width={config.circleRadius * 2}
  height={y(0) - y(truePos)}
  fill={colSelected === i && barSelected === 'true positive'
    ? colorTypes['true_pos_selected']
    : colorTypes['true_pos']}
  class="pointer {colSelected === i && 'true positive' === barSelected
    ? 'selected'
    : ''}"
  on:mouseover={(e) =>
    dispatch('mousemove', { e, props: { 'True Pos': col.truePos } })}
  on:focus={(e) =>
    dispatch('mousemove', { e, props: { 'True Pos': col.truePos } })}
  on:mousemove={(e) =>
    dispatch('mousemove', { e, props: { 'True Pos': col.truePos } })}
  on:mouseout={(e) => dispatch('mouseout')}
  on:blur={(e) => dispatch('mouseout')}
/>

{#if breakdown === false}
  <rect
    on:mousedown={() => selectModel(col, i, 'false positive')}
    x={0}
    y={y(falsePos + truePos)}
    width={config.circleRadius * 2}
    height={y(truePos) - y(falsePos + truePos)}
    fill={colSelected === i && barSelected === 'false positive'
      ? colorTypes['false_pos_selected']
      : colorTypes['false_pos']}
    class="pointer {colSelected === i && 'false positive' === barSelected
      ? 'selected'
      : ''}"
    on:mouseover={(e) =>
      dispatch('mousemove', { e, props: { 'False Pos': col.falsePos } })}
    on:focus={(e) =>
      dispatch('mousemove', { e, props: { 'False Pos': col.falsePos } })}
    on:mousemove={(e) =>
      dispatch('mousemove', { e, props: { 'False Pos': col.falsePos } })}
    on:mouseout={(e) => dispatch('mouseout')}
    on:blur={(e) => dispatch('mouseout')}
  />
{:else}
  {@const falseProp = {
    'Low Threshold': col.type.low_threshold,
    'Wrong Class': col.type.wrong_class,
    'Far Away': col.type.far_away,
    Duplicate: col.type.duplicate,
  }}
  <g
    on:mousedown={() => selectModel(col, i, 'false positive')}
    on:mouseover={(e) => dispatch('mousemove', { e, props: falseProp })}
    on:focus={(e) => dispatch('mousemove', { e, props: falseProp })}
    on:mousemove={(e) => dispatch('mousemove', { e, props: falseProp })}
    on:mouseout={(e) => dispatch('mouseout')}
    on:blur={(e) => dispatch('mouseout')}
  >
    <rect
      x={0}
      y={y(duplicate)}
      width={config.circleRadius * 2}
      height={y(truePos) - y(duplicate)}
      fill={colorTypes['duplicate']}
    />
    <rect
      x={0}
      y={y(far_away)}
      width={config.circleRadius * 2}
      height={y(duplicate) - y(far_away)}
      fill={colorTypes['far_away']}
    />
    <rect
      x={0}
      y={y(wrong_class)}
      width={config.circleRadius * 2}
      height={y(far_away) - y(wrong_class)}
      fill={colorTypes['wrong_class']}
    />
    <rect
      x={0}
      y={y(low_threshold)}
      width={config.circleRadius * 2}
      height={y(wrong_class) - y(low_threshold)}
      fill={colorTypes['low_threshold']}
    />
    <rect
      x={0}
      y={y(low_threshold)}
      width={config.circleRadius * 2}
      height={y(truePos) - y(low_threshold)}
      stroke="none"
      stroke-width="3"
      fill="none"
      rx="2"
      class="false-pointer {colSelected === i &&
      'false positive' === barSelected
        ? 'selected'
        : ''}"
    />
  </g>
{/if}

<!-- Adding False Negative -->
<rect
  on:mousedown={() => selectModel(col, i, 'false negative')}
  x={0}
  y={y(falseNeg + falsePos + truePos)}
  width={config.circleRadius * 2}
  height={y(falsePos + truePos) - y(falseNeg + falsePos + truePos)}
  fill={colorTypes['false_neg']}
  class="pointer {colSelected === i && 'false negative' === barSelected
    ? 'selected'
    : ''}"
  on:mouseover={(e) =>
    dispatch('mousemove', { e, props: { 'False Neg': col.falseNeg } })}
  on:focus={(e) =>
    dispatch('mousemove', { e, props: { 'False Neg': col.falseNeg } })}
  on:mousemove={(e) =>
    dispatch('mousemove', { e, props: { 'False Neg': col.falseNeg } })}
  on:mouseout={(e) => dispatch('mouseout')}
  on:blur={(e) => dispatch('mouseout')}
/>

<!-- Add Stroke scaled-->
{#if scaled}
  <line
    x1={0}
    x2={config.circleRadius * 2}
    y1={y(maxY - 7)}
    y2={y(maxY - 5)}
    style="stroke:white; stroke-width:1;"
  />
  <line
    x1={0}
    x2={config.circleRadius * 2}
    y1={y(maxY - 5)}
    y2={y(maxY - 3)}
    style="stroke:white; stroke-width:1;"
  />
{/if}

<!-- 'duplicate': number,
'low_threshold': number,
'far_way': number,
'wrong_class': number -->
<style>
  .group {
    fill: #cccccc;
    stroke: #bdbdbd;
    stroke-width: 2;
    pointer-events: all;
  }

  .background-bar {
    fill: none;
    stroke: none;
    pointer-events: all;
  }
  .pointer {
    cursor: pointer;
  }
  .pointer:hover {
    fill: #283593;
  }

  .false-pointer {
    cursor: pointer;
    pointer-events: all;
  }
  .false-pointer:hover {
    stroke: #283593;
  }

  .hightlight {
    fill: #fed986;
    /* pointer-events : none; */
  }
</style>
