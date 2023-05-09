<script lang="ts">
  import RangeSlider from 'svelte-range-slider-pips';
  import type {DoubleSliderType} from '../../types';
  export let option:DoubleSliderType;
  

  let values = [option.value, option.value2];
  // value = option.value;
  // value2 = option.value2;

</script>

  <h4 class="title">{option.name}</h4>
  <div class="row">
    <input 
      type="number" 
      id={option.id}
      bind:value={values[0]}
      step="0.01"
      class="combo"
      />
      <input 
      type="number" 
      id={option.id}
      bind:value={values[1]}
      step="0.01"
      class="combo"
      />
    </div>
<RangeSlider 
  bind:values={values} 
  min={option.min} 
  max={option.max}
  step={option.step}
  on:stop={() => {option.updatefunction(values)}}
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