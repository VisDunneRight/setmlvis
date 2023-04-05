<script lang="ts">
import {dataset} from '../stores';
let selected = $dataset['yolos-base,'];
$:console.log('selected:', selected)
</script>
<div class="collection-container" 
     style:width="100%" 
     style:height="40%">
</div>


<style>
  .collection-container {
    position:relative;
    background-color: lightgray;
    min-width: 200px;
    bottom: 0px;
    border: 1px solid rgb(226, 226, 226);
  }
</style>