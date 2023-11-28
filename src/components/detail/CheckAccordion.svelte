<script>
  import { slide } from 'svelte/transition';
  import UpArrow from '../../assets/up-arrow.svelte';
  import DownArrow from '../../assets/down-arrow.svelte';
  import Checked from '../../assets/checked.svelte';
  import CheckedMinus from '../../assets/checked-minus.svelte';
  import Unchecked from '../../assets/unchecked.svelte';

  export let open = false;
  export let check = 0;
  export let hasCheck = true;
  export let colorCheck = '#424242';
  export let updateCheck = undefined;

  const handleClick = () => (open = !open);
  const handleCheck = () => {
    if (check === 0) {
      check = 2;
    } else {
      check = 0;
    }
    if (updateCheck) {
      updateCheck();
    }
  };
</script>

<div class="accordion">
  <div class="line">
    {#if hasCheck}
      <span class="checkmark" on:click={handleCheck} on:keydown={handleCheck}>
        {#if check === 2}
          <Checked size={20} color={colorCheck} />
        {:else if check === 1}
          <CheckedMinus size={24} color={colorCheck} />
        {:else}
          <Unchecked size={20} color={colorCheck} />
        {/if}
      </span>
    {/if}
    <button on:click={handleClick} class="header">
      <div class="text">
        <slot name="head" />
      </div>
      <div style="display: flex;">
        <slot name="info" />
        <div class="sign">
          {#if open}
            <UpArrow />
          {:else}
            <DownArrow />
          {/if}
        </div>
      </div>
    </button>
  </div>

  {#if open}
    <div class="details" transition:slide>
      <slot name="details" />
    </div>
  {/if}
</div>

<style>
  div.accordion {
    background-color: #eee;
    color: #444;
    width: 100%;
    transition: 0.4s;
  }

  .sign {
    font-size: 1.5em;
  }
  .line {
    display: flex;
    align-items: center;
    padding: 6px;
  }
  .checkmark {
    cursor: pointer;
  }

  .header {
    display: flex;
    width: 100%;
    cursor: pointer;
    text-align: left;
    justify-content: space-between;
    border: none;
    outline: none;
  }

  .text {
    flex: 1;
    margin-right: 5px;
  }

  div.details {
    background-color: #cecece;
    padding-left: 2rem;
  }
</style>
