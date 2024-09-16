<script lang="ts">
  import { Handle, Position, type NodeProps } from "@xyflow/svelte";
  import Generator from "$lib/icons/Generator.svelte";
  import Load from "$lib/icons/Load.svelte";
  import { onMount } from "svelte";

  type Data = {
    busNum: string;
    numGenerators: number;
    numLoads: number;
    numBranchesFrom: number;
    numBranchesTo: number;
    angle: string | null;
    voltage: string | null;
  };
  type $$Props = NodeProps & { data: Data };

  const BUS_HEIGHT = 64; // px
  const GENERATOR_HEIGHT = 35; // px
  const LOAD_HEIGHT = 30; // px

  export let data: Data;
  const {
    busNum,
    numGenerators,
    numLoads,
    numBranchesFrom,
    numBranchesTo,
    angle,
    voltage,
  } = data;

  const numInputIntervals = numGenerators + numBranchesTo + 1;
  const numOutputIntervals = numLoads + numBranchesFrom + 1;
  const spaceBetweenInputs =
    (BUS_HEIGHT - numGenerators * GENERATOR_HEIGHT) / numInputIntervals;
  const spaceBetweenOutputs =
    (BUS_HEIGHT - numLoads * LOAD_HEIGHT) / numOutputIntervals;

  function generatorTopOffset(i: number) {
    return i * (GENERATOR_HEIGHT + spaceBetweenInputs) + spaceBetweenInputs;
  }

  function inHandleTopOffset(i: number) {
    return (
      numGenerators * (GENERATOR_HEIGHT + spaceBetweenInputs) +
      (i + 1) * spaceBetweenInputs
    );
  }

  function loadTopOffset(i: number) {
    return i * (LOAD_HEIGHT + spaceBetweenOutputs) + spaceBetweenOutputs;
  }

  function outHandleTopOffset(i: number) {
    return (
      numLoads * (LOAD_HEIGHT + spaceBetweenOutputs) +
      (i + 1) * spaceBetweenOutputs
    );
  }

  function formatFloat(value: string | null): string {
    if (value === null) return "";
    return parseFloat(value).toFixed(2);
  }

  onMount(() => {
    console.log("RERENDERED!!!");
  });

  // Debugging logs
  $: console.log(`Bus ${busNum} Data:`, {
    numGenerators,
    numLoads,
    numBranchesFrom,
    numBranchesTo,
    angle,
    voltage,
  });

  $: console.log(`Handle positions:`, {
    generatorTopOffsets: Array.from({ length: numGenerators }).map((_, i) =>
      generatorTopOffset(i),
    ),
    inHandleTopOffsets: Array.from({ length: numBranchesTo }).map((_, i) =>
      inHandleTopOffset(i),
    ),
    loadTopOffsets: Array.from({ length: numLoads }).map((_, i) =>
      loadTopOffset(i),
    ),
    outHandleTopOffsets: Array.from({ length: numBranchesFrom }).map((_, i) =>
      outHandleTopOffset(i),
    ),
  });
</script>

<div
  class="relative my-10 block items-center border border-black bg-blue-800 text-center"
  style={`
	  height: ${BUS_HEIGHT}px;
	  width: 10px;
	`}
>
  {#if typeof voltage !== "undefined" && voltage !== null}
    <div
      class="absolute bottom-full mx-auto w-full items-center text-center text-xs text-black"
    >
      {formatFloat(voltage)} kV ∠{formatFloat(angle)}°
    </div>
  {/if}

  <div
    class="absolute top-0 mx-auto w-full items-center bg-black text-center text-xs text-border"
  >
    {busNum}
  </div>

  {#each Array.from({ length: numGenerators }) as _, i (i)}
    <div class="absolute right-full" style="top: ${generatorTopOffset(i)}px">
      <Generator />
    </div>
  {/each}
  {#each Array.from({ length: numBranchesTo }) as _, i (i)}
    <Handle
      type="target"
      id={`in-${i}`}
      position={Position.Left}
      style={`top: ${inHandleTopOffset(i)}px`}
    />
  {/each}

  {#each Array.from({ length: numLoads }) as _, i (i)}
    <div style={`position: absolute; left: 100%; top: ${loadTopOffset(i)}px`}>
      <Load />
    </div>
  {/each}
  {#each Array.from({ length: numBranchesFrom }) as _, i (i)}
    <Handle
      type="source"
      id={`out-${i}`}
      position={Position.Right}
      style={`top: ${outHandleTopOffset(i)}px`}
    />
  {/each}
</div>
