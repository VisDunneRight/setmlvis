<script>
  export let open = false;
  import { slide } from 'svelte/transition';
  import Plus from '../../assets/plus.svelte';
  import Minus from '../../assets/minus.svelte';
  const handleClick = () => (open = !open);
</script>

<div class="accordion">
  <button on:click={handleClick} class="header">
    <div class="text">
      <slot name="head" />
    </div>
    <div>
      <div class="text">
        <slot name="info" />
        <div class="sign">
          {#if !open}
            <Plus />
          {:else}
            <Minus />
          {/if}
        </div>
      </div>
    </div></button
  >

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

  .header {
    display: flex;
    padding: 8px 8px 8px 14px;
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
