<script lang="ts">
  import type { MenuItem } from '../../types';
  import Slider from './Slider.svelte';
  import DoubleSlider from './DoubleSlider.svelte';
  export let option: MenuItem;
</script>

<div class="option-item">
  {#if option.type === 'slider'}
    <Slider {option} />
  {:else if option.type === 'double-slider'}
    <DoubleSlider {option} />
  {/if}
</div>

<style>
  .option-item {
    padding-top: 5px;
  }
</style>
