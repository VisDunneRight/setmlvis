<!--
	@component
	Generates a hover tooltip. It creates a slot with an exposed variable via `let:detail` that contains information about the event. Use the slot to populate the body of the tooltip using the exposed variable `detail`.
 -->
 <script>
	/** @type {Object} evt – A svelte event created via [`dispatch`](https://svelte.dev/docs#createEventDispatcher) with event information under `evt.detail.e`. */
  export let evt = {};
  export let width = 200;
	/** @type {Number} [offset=-10] – A y-offset from the hover point, in pixels. */
  const numEleHeight = Object.keys(evt?.detail.props).length * 23 + 30;
  $:offsetY = evt?.detail.e.offsetY <= numEleHeight ? numEleHeight : -10;

  let eleWidth = 0;
  Object.entries(evt.detail.props).forEach((name, value) =>{
    const length = name.length + value.toString.length + 2;
    eleWidth = Math.max(eleWidth, length*9);
  })
  $: offsetX = 0;
  $: if(evt?.detail.e.offsetX <= eleWidth) {
    offsetX = eleWidth;
  } else if(width - evt?.detail.e.offsetX  <= eleWidth) {
    offsetX = -eleWidth;
  }
  // $: offsetX = evt?.detail.e.offsetX <= eleWidth ? eleWidth: 0;
  
  //  offsetX =  width - evt?.detail.e.offsetX  <= eleWidth ? - eleWidth: 0
</script>



{#if evt.detail}
  <div
    class="vis-tooltip"
    style="
      top:{evt.detail.e.layerY + offsetY}px;
      left:{evt.detail.e.layerX + offsetX}px;
    "
  >
    <slot detail={evt.detail}></slot>
  </div>
{/if}

<style>
  .vis-tooltip {
    position: absolute;
    border: 1px solid #ccc;
		font-size: 13px;
    white-space: nowrap;
    background: rgba(255, 255, 255, 0.85);
    transform: translate(-50%, -100%);
    padding: 5px;
    z-index: 15;
  }
</style>