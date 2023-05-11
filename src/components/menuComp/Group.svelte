<script lang="ts">
  import type { MenuItem } from '../../types';
  import Slider from './Slider.svelte';
  import DoubleSlider from './DoubleSlider.svelte';
  export let groups: Array<MenuItem>;
</script>

{#each groups as option}
  <div class="option-item">
    {#if option.type === 'slider'}
      <Slider {option} />
    {:else if option.type === 'double-slider'}
      <DoubleSlider {option} />
    {/if}
  </div>
{/each}

<style>
  .option-item {
    padding-top: 5px;
  }
</style>
