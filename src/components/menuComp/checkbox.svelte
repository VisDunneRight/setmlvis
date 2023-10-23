<script>
  import Checked from '../../assets/checked.svelte';
  import Unchecked from '../../assets/unchecked.svelte';
  export let checked = false;
  export let updateSelection;
</script>

<label class="container">
  <input
    type="checkbox"
    {checked}
    on:click={(e) => {
      updateSelection(!checked);
    }}
  />
  <span class="checkmark">
    {#if checked === true}
      <Checked size={25} />
    {:else}
      <Unchecked size={25} />
    {/if}
  </span>
</label>

<style>
  .container {
    display: grid;
    justify-items: start;
    grid-template-columns: 1fr;
    margin: 0 0 1px;
    padding-right: 30px;
    padding-top: 5px;
    line-height: 1.5;
    cursor: unset;
    width: 24px;
  }

  /* Hide the browser's default checkbox */
  .container input {
    position: absolute;
    opacity: 0;
    cursor: pointer;
    height: 0;
    width: 0;
  }

  /* Create a custom checkbox */
  .checkmark {
    height: 25px;
    width: 25px;
    cursor: pointer;
  }

  /* Create the checkmark/indicator (hidden when not checked) */
  .checkmark:after {
    content: '';
    position: absolute;
    display: none;
  }

  /* Show the checkmark when checked */
  .container input:checked ~ .checkmark:after {
    display: block;
  }
</style>
