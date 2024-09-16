<script lang="ts">
  import { onMount } from "svelte";
  import { createEventDispatcher } from "svelte";
  import { fly, fade } from "svelte/transition";

  // Props
  export let min = 0;
  export let max = 100;
  export let initialValue = 0;
  export let id = null;
  export let value =
    typeof initialValue === "string" ? parseInt(initialValue) : initialValue;
  export let hoverText: string[] = [];

  // Node Bindings
  let container = null;
  let thumb = null;
  let progressBar = null;
  let element = null;

  // Internal State
  let elementX = null;
  let currentThumb = null;
  let holding = false;
  let thumbHover = false;
  let keydownAcceleration = 0;
  let accelerationTimer = null;

  // Dispatch 'change' events
  const dispatch = createEventDispatcher();

  let mouseEventShield;
  let resizeWindow;
  let setValue;
  let onTrackEvent;
  let onHover;
  let onDragStart;
  let onDragEnd;
  let isMouseInElement;
  let onKeyPress;
  let calculateNewValue;
  let updateValueOnEvent;

  onMount(() => {
    // Mouse shield used onMouseDown to prevent any mouse events penetrating other elements,
    // ie. hover events on other elements while dragging. Especially for Safari
    mouseEventShield = document.createElement("div");
    mouseEventShield.setAttribute("class", "mouse-over-shield");
    mouseEventShield.addEventListener("mouseover", (e) => {
      e.preventDefault();
      e.stopPropagation();
    });

    resizeWindow = () => {
      elementX = element.getBoundingClientRect().left;
    };

    // Allows both bind:value and on:change for parent value retrieval
    setValue = (val) => {
      value = val;
      dispatch("change", { value });
      console.log("Value set to:", value);
    };

    onTrackEvent = (e) => {
      // Update value immediately before beginning drag
      updateValueOnEvent(e);
      onDragStart(e);
    };

    onHover = (e) => {
      thumbHover = !thumbHover;
    };

    onDragStart = (e) => {
      // If mouse event add a pointer events shield
      if (e.type === "mousedown") document.body.append(mouseEventShield);
      currentThumb = thumb;
    };

    onDragEnd = (e) => {
      // If using mouse - remove pointer event shield
      if (e.type === "mouseup") {
        if (document.body.contains(mouseEventShield))
          document.body.removeChild(mouseEventShield);
        // Needed to check whether thumb and mouse overlap after shield removed
        if (isMouseInElement(e, thumb)) thumbHover = true;
      }
      currentThumb = null;
    };

    // Check if mouse event cords overlay with an element's area
    isMouseInElement = (event, element) => {
      let rect = element.getBoundingClientRect();
      let { clientX: x, clientY: y } = event;
      if (x < rect.left || x >= rect.right) return false;
      if (y < rect.top || y >= rect.bottom) return false;
      return true;
    };

    // Accessible keypress handling
    onKeyPress = (e) => {
      // Max out at +/- 10 to value per event (50 events / 5)
      // 100 below is to increase the amount of events required to reach max velocity
      if (keydownAcceleration < 50) keydownAcceleration++;
      let throttled = Math.ceil(keydownAcceleration / 5);

      if (e.key === "ArrowUp" || e.key === "ArrowRight") {
        if (value + throttled > max || value >= max) {
          setValue(max);
        } else {
          setValue(value + throttled);
        }
      }
      if (e.key === "ArrowDown" || e.key === "ArrowLeft") {
        if (value - throttled < min || value <= min) {
          setValue(min);
        } else {
          setValue(value - throttled);
        }
      }

      // Reset acceleration after 100ms of no events
      clearTimeout(accelerationTimer);
      accelerationTimer = setTimeout(() => (keydownAcceleration = 1), 100);
    };

    calculateNewValue = (clientX) => {
      // Find distance between cursor and element's left cord (20px / 2 = 10px) - Center of thumb
      let delta = clientX - (elementX + 10);

      // Use width of the container minus (5px * 2 sides) offset for percent calc
      let percent = (delta * 100) / (container.clientWidth - 10);

      // Limit percent 0 -> 100
      percent = percent < 0 ? 0 : percent > 100 ? 100 : percent;

      // Limit value min -> max
      setValue(parseInt((percent * (max - min)) / 100) + min);
    };

    // Handles both dragging of touch/mouse as well as simple one-off click/touches
    updateValueOnEvent = (e) => {
      // touchstart && mousedown are one-off updates, otherwise expect a currentPointer node
      if (!currentThumb && e.type !== "touchstart" && e.type !== "mousedown")
        return false;

      if (e.stopPropagation) e.stopPropagation();
      if (e.preventDefault) e.preventDefault();

      // Get client's x cord either touch or mouse
      const clientX =
        e.type === "touchmove" || e.type === "touchstart"
          ? e.touches[0].clientX
          : e.clientX;

      calculateNewValue(clientX);
    };
  });

  // React to left position of element relative to window
  $: if (element) elementX = element.getBoundingClientRect().left;

  // Set a class based on if dragging
  $: holding = Boolean(currentThumb);

  // Update progressbar and thumb styles to represent value
  $: if (progressBar && thumb) {
    // Limit value min -> max
    value = value > min ? value : min;
    value = value < max ? value : max;

    let percent = ((value - min) * 100) / (max - min);
    let offsetLeft = (container.clientWidth - 10) * (percent / 100) + 5;

    // Update thumb position + active range track width
    thumb.style.left = `${offsetLeft}px`;
    progressBar.style.width = `${offsetLeft}px`;

    console.log("Thumb position:", offsetLeft);
    console.log("Progress bar width:", progressBar.style.width);
  }
</script>

<svelte:window
  on:touchmove|nonpassive={updateValueOnEvent}
  on:touchcancel={onDragEnd}
  on:touchend={onDragEnd}
  on:mousemove={updateValueOnEvent}
  on:mouseup={onDragEnd}
  on:resize={resizeWindow}
/>
<div class="range">
  <div
    class="range__wrapper"
    tabindex="0"
    on:keydown={onKeyPress}
    bind:this={element}
    role="slider"
    aria-valuemin={min}
    aria-valuemax={max}
    aria-valuenow={value}
    {id}
    on:mousedown={onTrackEvent}
    on:touchstart={onTrackEvent}
  >
    <div class="range__track" bind:this={container}>
      <div class="range__track--highlighted" bind:this={progressBar} />
      <div
        class="range__thumb"
        class:range__thumb--holding={holding}
        bind:this={thumb}
        on:touchstart={onDragStart}
        on:mousedown={onDragStart}
        on:mouseover={() => (thumbHover = true)}
        on:mouseout={() => (thumbHover = false)}
      >
        {#if holding || thumbHover}
          <div
            class="range__tooltip"
            in:fly={{ y: 7, duration: 200 }}
            out:fade={{ duration: 100 }}
          >
            Time: <strong style="font-weight: bold">{hoverText[value]}</strong>
          </div>
        {/if}
      </div>
    </div>
  </div>
</div>

<svelte:head>
  <style>
    .mouse-over-shield {
      position: fixed;
      top: 0px;
      left: 0px;
      height: 100%;
      width: 100%;
      background-color: rgba(255, 0, 0, 0);
      z-index: 10000;
      cursor: grabbing;
    }
  </style>
</svelte:head>

<style>
  .range {
    position: relative;
    flex: 1;
  }

  .range__wrapper {
    min-width: 100%;
    position: relative;
    padding: 0.5rem;
    box-sizing: border-box;
    outline: none;
  }

  .range__wrapper:focus-visible > .range__track {
    box-shadow:
      0 0 0 2px white,
      0 0 0 3px var(--track-focus, #6185ff);
  }

  .range__track {
    position: relative;
    background-color: var(--track-background, #d1d5db);
    border-radius: 1px;
    height: 0.5rem;
    cursor: pointer;
    transition: box-shadow 150ms ease;
  }

  .range__track--highlighted {
    background-color: var(--track-highlighted, #3b82f6);
    border-radius: 1px;
    height: 0.5rem;
    position: absolute;
    top: 0;
    left: 0;
    transition: width 150ms ease;
  }

  .range__thumb {
    width: 1rem;
    height: 1rem;
    border-radius: 50%;
    background-color: var(--thumb-background, #3b82f6);
    position: absolute;
    cursor: pointer;
    top: 50%;
    transform: translateY(-50%);
    transition: background-color 150ms ease;
  }

  .range__thumb--holding {
    background-color: var(--thumb-hover, #2563eb);
  }

  .range__tooltip {
    position: absolute;
    bottom: 1.5rem;
    background-color: var(--tooltip-background, #000);
    color: var(--tooltip-color, #fff);
    border-radius: 4px;
    padding: 0.25rem 0.5rem;
    font-size: 0.75rem;
  }
</style>
