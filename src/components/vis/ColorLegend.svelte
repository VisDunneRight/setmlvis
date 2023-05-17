<script>
  export let color;
  export let name;
  export let x;
  export let y;
  let boxSize = 14;
</script>
<rect
    x={x - boxSize/2}
    y={y - boxSize/2}
    width={boxSize}
    height={boxSize}
    rx={2}
    fill="{color}"
  />
  <text
    x={x + boxSize/2 + 2}
    y={y + 2}
    text-anchor="start"
    alignment-baseline="middle"
    class="model-text">{name}</text
  >
<style>

</style>