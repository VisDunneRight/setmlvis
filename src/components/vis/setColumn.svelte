<script>
  export let col;
  export let i;
  export let config
  export let mouseOverI;
  export let winHeight;
  export let padding;
  export let modelRow;
  export let y;
  export let selectModel;
  export let colSelected;
  export let barSelected;
</script>

<rect
  x={0}
  y={config.circleRadius}
  width={config.circleRadius * 2}
  height={winHeight - padding.top}
  class={mouseOverI === i ? 'hightlight' : 'background-bar'}
/>

<g class="circles">
  {#each col.models as mod, j}
    <circle
      cx={config.circleRadius}
      cy={modelRow(j)}
      r={config.circleRadius}
      fill={mod ? '#636363' : '#f0f0f0'}
    />
  {/each}
</g>

{#if col.modelRange.length > 1}
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
  y={y(col.truePos)}
  width={config.circleRadius * 2}
  height={y(0) - y(col.truePos)}
  fill="#377eb8"
  class="pointer {colSelected === i && 'true positive' === barSelected
    ? 'selected'
    : ''}"
/>

<rect
  on:mousedown={() => selectModel(col, i, 'false positive')}
  x={0}
  y={y(col.falsePos + col.truePos)}
  width={config.circleRadius * 2}
  height={y(col.truePos) - y(col.falsePos + col.truePos)}
  fill="#e41a1c"
  class="pointer {colSelected === i && 'false positive' === barSelected
    ? 'selected'
    : ''}"
/>

<style>
  .background-bar { 
    fill: none;
    stroke: none;
    pointer-events: all;
  }
  .pointer {
    cursor: pointer;
  }
  .pointer:hover {
    fill:#283593;
  }

  .hightlight {
    fill: #fed986;
    /* pointer-events : none; */
  }
</style>