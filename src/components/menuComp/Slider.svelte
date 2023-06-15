<script lang="ts">
  import RangeSlider from 'svelte-range-slider-pips';
  import type { SliderType } from '../../types';
  export let option: SliderType;
  let values = [option.value];
  function updateValue(d: Event){
    const target = d.target as HTMLInputElement;
    console.log(target.value)
    values[0] = Number(target?.value) ?? 0;
    option.updatefunction(values[0]);
  }
</script>

<div class="row">
  <h4 class="title">{option.name}</h4>
  <input
    type="number"
    id={option.id}
    value={values[0]}
    on:change={(d) =>{
      updateValue(d);
    }}
    step="0.01"
    min={option.min}
    class="combo"
  />
</div>

<RangeSlider
  min={option.min}
  max={option.max}
  step={option.step}
  bind:values
  on:stop={() => {
    option.updatefunction(values[0]);
  }}
/>

<style>
  .title {
    padding-left: 10px;
  }
  .combo {
    min-width: 60px;
    height: 30px;
    margin: 2px;
  }
  .row {
    display: flex;
    align-items: center;
  }
</style>
