<script lang="ts">
  export let size = 13;
  export let x: number;
  export let y: number;
  export let text: string;
  export let backgroundColor: string;
  export let textColor = 'white';

  let boxWidth = text.length * (size / 2) + 3;
</script>

<rect
  {x}
  y={y - size - 2}
  width="{boxWidth}px"
  height="{size + 2}px"
  fill={backgroundColor}
  stroke={backgroundColor}
  style="--font-size: {size}"
/>
<text id={text} {x} y={y - 2} fill={textColor} class="small">{text}</text>

<style>
  .small {
    font: var(--font-size) + 'px' Monospace;
  }
</style>
