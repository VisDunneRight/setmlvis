<script lang="ts">
  import RangeSlider from 'svelte-range-slider-pips';
  import type {SliderType} from '../../types';
  export let option:SliderType;
  let values = [option.value];
</script>
<div class="row">
  <h4 class="title">{option.name}</h4>
  <input 
    type="number" 
    id={option.id}
    bind:value={values[0]}
    step="0.01"
    class="combo"
    />
    </div>

<RangeSlider 
  min={option.min}
  max={option.max}
  step={option.step}
  bind:values={values}
  on:stop={() => {option.updatefunction(values[0])}}
  />

<style>
.title{
  padding-left:10px;
}
.combo{
  min-width:60px;
  height:30px;
  margin:2px;
}
.row{
  display:flex;
  align-items: center;
}
</style>