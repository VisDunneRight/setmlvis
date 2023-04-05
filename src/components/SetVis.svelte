<script lang="ts">
 import {menuWidth, windowWidth} from '../stores';
 $:console.log('Width:', $windowWidth)
</script>
<div class="set-vis-container" 
    style:width="{($windowWidth - $menuWidth)/2}px" 
    style:height="60%">
</div>


<style>
  .set-vis-container {
    position: relative;
    background-color: blue;
    min-width: 200px;
    border: 1px solid rgb(226, 226, 226);
  }
</style>