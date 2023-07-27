<script>
  export let enabled = true;
  export let height = 25;
  export let message = 'active';
  export let offmessage = message;
  export let activeColor = '#0380b3';
  export let inactiveColor = '#384c60';
  export let update;
  let width = message.length * 12 > 100 ? message.length * 12 : 100;
</script>

<div
  class="vistoggle-btn"
  style:height="{height}px"
  style:width="{width}px"
  style:background-color={inactiveColor}
>
  <label for="checkbox-{message}" class="cf">
    <input
      type="checkbox"
      id="checkbox-{message}"
      checked={enabled}
      on:change={update}
    />
    <span
      style:height="{height}px"
      style:width="{width - 30}px"
      style:background-color={activeColor}
      style:margin-left="{-(width - 30)}px">{message}</span
    >
    <i class="indicator" style:height="{height}px">
      <svg
        version="1.1"
        id="toggle"
        xmlns="http://www.w3.org/2000/svg"
        xmlns:xlink="http://www.w3.org/1999/xlink"
        x="0px"
        y="0px"
        viewBox="0 0 33 33"
        style="enable-background:new 0 0 33 33;"
        xml:space="preserve"
      >
        <path
          class="circ path"
          style="fill:none;stroke-width:3;stroke-linejoin:round;stroke-miterlimit:10;"
          d="M6.2,6.2L6.2,6.2
      c-5.7,5.7-5.7,14.8,0,20.5l0,0c5.7,5.7,14.8,5.7,20.5,0l0,0c5.7-5.7,5.7-14.8,0-20.5l0,0C21.1,0.6,11.9,0.6,6.2,6.2z"
        />
        <polyline
          class="cross path"
          style="fill:none;stroke:#CD4C10;stroke-width:3;stroke-linejoin:round;stroke-miterlimit:10;"
          points=" 11.4,11.4 21.6,21.6 "
        />
        <polyline
          class="cross path"
          style="fill:none;stroke:#CD4C10;stroke-width:3;stroke-linejoin:round;stroke-miterlimit:10;"
          points="21.6,11.4 11.4,21.6	"
        />
        <polyline
          class="tick path"
          style="fill:none;stroke:#557D25;stroke-width:3;stroke-linejoin:round;stroke-miterlimit:10;"
          points="10,17.3 13.8,21.1 
        23,11.9 "
        />
      </svg>
    </i>
    <span style:height="{height}px" style:width="{width - 30}px"
      >{offmessage}</span
    >
  </label>
</div>

<style>
  .vistoggle-btn {
    background: #384c60;
    height: 50px;
    width: 150px;
    overflow: hidden;
    border-radius: 4px;
    cursor: pointer;
  }
  .vistoggle-btn label {
    cursor: pointer;
  }
  .vistoggle-btn span {
    float: left;
    color: #fff;
    font-family: Arial;
    font-weight: bold;
    text-align: center;
    width: 66%;
    height: 100%;
    background: #0380b3;
    display: block;
    font-size: 14px;
    display: flex;
    justify-content: center;
    align-items: center;
    -webkit-transition: margin 0.2s linear;
    -moz-transition: margin 0.2s linear;
    -ms-transition: margin 0.2s linear;
    -o-transition: margin 0.2s linear;
    transition: margin 0.2s linear;
    margin-left: -66%;
  }
  .vistoggle-btn span ~ span {
    margin-left: 0;
    background: none;
  }
  .vistoggle-btn .indicator {
    display: flex;
    justify-content: center;
    float: left;
    background: #ccc;
    height: 100%;
    width: 30px;
    padding: 4px;
    box-sizing: border-box;
  }
  .vistoggle-btn input:checked + span {
    margin-left: 0 !important;
  }
  .vistoggle-btn input {
    opacity: 0;
    position: absolute;
    left: -10000px;
  }
  .circ {
    stroke: #cd4c10;
    transition: stroke 1s 0.2s;
  }
  .vistoggle-btn input:checked ~ .indicator .circ {
    stroke: #557d25;
    opacity: 1;
  }
  .tick {
    stroke-dasharray: 20;
    stroke-dashoffset: 20;
    transition: stroke-dashoffset 0.3s;
    transition-delay: 0s;
  }
  .vistoggle-btn input:checked ~ .indicator .tick {
    opacity: 1;
    stroke-dashoffset: 0;
    transition-delay: 0.5s;
  }
  .cross {
    /* opacity: 1; */
    stroke-dasharray: 15;
    stroke-dashoffset: 0;
    transition: stroke-dashoffset 0.25s ease-in;
    transition-delay: 0.5s;
  }
  .cross + .cross {
    transition-delay: 0.25s;
  }
  .vistoggle-btn input:checked ~ .indicator .cross {
    opacity: 0;
    transition: stroke-dashoffset 0.5s ease, opacity 0.5s ease;
    transition-delay: 0;
    stroke-dashoffset: 15;
  }
</style>
