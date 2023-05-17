<script>
export let x;
export let y;
export let update;
export let text;
let size = text.length * 7 + 8;
</script>

<g on:mousedown={() => update()} class="pointer">
  <rect
    x={x - size/2}
    y={y - 20/2}
    width={size}
    height={18}
    rx={4}
    fill="#bdbdbd"
  />
  <text
    x={x}
    y={y}
    text-anchor="middle"
    alignment-baseline="middle"
    class="model-text">{text}</text
  >
</g>

<style>
  .pointer {
    cursor: pointer;
  }
  .pointer:hover {
    fill: #283593;
  }
</style>