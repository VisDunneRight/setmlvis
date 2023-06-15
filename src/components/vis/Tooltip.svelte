<!--
	@component
	Generates a hover tooltip. It creates a slot with an exposed variable via `let:detail` that contains information about the event. Use the slot to populate the body of the tooltip using the exposed variable `detail`.
 -->
 <script>
	/** @type {Object} evt – A svelte event created via [`dispatch`](https://svelte.dev/docs#createEventDispatcher) with event information under `evt.detail.e`. */
  export let evt = {};

	/** @type {Number} [offset=-10] – A y-offset from the hover point, in pixels. */
  export let offsetY = -10;
</script>



{#if evt.detail}
  <div
    class="vis-tooltip"
    style="
      top:{evt.detail.e.layerY + offsetY}px;
      left:{evt.detail.e.layerX}px;
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
    overflow-wrap: normal;
    background: rgba(255, 255, 255, 0.85);
    transform: translate(-50%, -100%);
    padding: 5px;
    z-index: 15;
  }
</style>