<script>
  import { colorTypes } from '../../ulit';

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
  export let breakdown;

  let duplicate = col.truePos + col.type.duplicate;
  let far_away = duplicate + col.type.far_away;
  let wrong_class = far_away + col.type.wrong_class;
  let normal = wrong_class + col.type.normal;
</script>

<rect
  x={0}
  y={config.circleRadius}
  width={config.circleRadius * 2}
  height={winHeight - padding.top + 4}
  class='{mouseOverI === i ? 'hightlight' : col.name === 'Group' ? 'group':'background-bar'}'
  ry={col.name === 'Group' ? 8 :0}
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
    {:else}
      {#if mod === 2 || mod === 0}
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
    {/if}

  {/each}
</g>

{#if col.modelRange.length > 1 &&  col.name !== 'Group'}
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
  fill="{colorTypes['true_pos']}"
  class="pointer {colSelected === i && 'true positive' === barSelected
    ? 'selected'
    : ''}"
/>

{#if breakdown === false }
  <rect
    on:mousedown={() => selectModel(col, i, 'false positive')}
    x={0}
    y={y(col.falsePos + col.truePos)}
    width={config.circleRadius * 2}
    height={y(col.truePos) - y(col.falsePos + col.truePos)}
    fill="{colorTypes['false_pos']}"
    class="pointer {colSelected === i && 'false positive' === barSelected
      ? 'selected'
      : ''}"
  />
{:else}
  <g on:mousedown={() => selectModel(col, i, 'false positive')} >
    <rect
      x={0}
      y={y(duplicate)}
      width={config.circleRadius * 2}
      height={y(col.truePos) - y(duplicate)}
      fill="{colorTypes['duplicate']}"
    />
    <rect
      x={0}
      y={y(far_away)}
      width={config.circleRadius * 2}
      height={y(duplicate) - y(far_away)}
      fill="{colorTypes['far_away']}"
    />
    <rect
      x={0}
      y={y(wrong_class)}
      width={config.circleRadius * 2}
      height={y(far_away) - y(wrong_class)}
      fill="{colorTypes['wrong_class']}"
    />
    <rect
      x={0}
      y={y(normal)}
      width={config.circleRadius * 2}
      height={y(wrong_class) - y(normal)}
      fill="{colorTypes['normal']}"
    />
    <rect
      x={0}
      y={y(normal)}
      width={config.circleRadius * 2}
      height={y(col.truePos) - y(normal)}
      stroke="none"
      stroke-width = "3"
      fill= "none"
      rx="2"
      class="false-pointer {colSelected === i && 'false positive' === barSelected
        ? 'selected'
        : ''}"
      />
  </g>
{/if}
<!-- 'duplicate': number,
'normal': number,
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
    fill:#283593;
  }

  .false-pointer {
    cursor: pointer;
    pointer-events: all;
  }
  .false-pointer:hover {
    stroke:#283593;
  }

  .hightlight {
    fill: #fed986;
    /* pointer-events : none; */
  }
</style>