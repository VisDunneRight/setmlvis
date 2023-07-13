<script>
  import DuplicateIcon from '../../assets/duplicate.svelte';
  import FarWayIcon from '../../assets/far-away.svelte';
  import LowThresholdIcon from '../../assets/low-threshold-normal.svelte';
  import WrongClassIcon from '../../assets/wrong-class.svelte';
  export let color;
  export let name;
  export let x;
  export let y;
  export let type;
  let boxSize = 14;
  
</script>
<g 
  transform="translate({x - boxSize/2},{y - boxSize/2})"
>
    <rect
      width={boxSize}
      height={boxSize}
      rx={2}
      fill="{color}"
    />

    {#if type === 'duplicate'}
      <DuplicateIcon width={boxSize - 4} height={boxSize - 4} />
    {:else if type === 'far_away'}
      <FarWayIcon width={boxSize - 4} height={boxSize - 4} />
    {:else if type === 'low_threshold'}
      <LowThresholdIcon width={boxSize - 4} height={boxSize - 4} />
    {:else if type === 'wrong_class'}
      <WrongClassIcon width={boxSize - 4} height={boxSize - 4} />
    {/if}
  
  <text
    x={boxSize + 2}
    y={boxSize/2 + 2}
    text-anchor="start"
    alignment-baseline="middle"
    class="model-text">{name}</text
  >
</g>
<style>

</style>