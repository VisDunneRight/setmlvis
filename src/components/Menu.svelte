<script lang="ts">
  import {height, menuWidth} from '../stores';
</script>
<div class="menu-container" style:width="{$menuWidth}px" style:height="{$height}px">
</div>


<style>
  .menu-container {
    background-color: red;
    min-width: 200px;
    z-index: 2;
    position: relative;
    float: left;
    border: 1px solid rgb(226, 226, 226);
  }
</style>