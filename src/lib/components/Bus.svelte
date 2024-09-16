<script lang="ts">
  import { Handle, Position, type NodeProps } from "@xyflow/svelte";
  import Generator from "$lib/icons/Generator.svelte";
  import Load from "$lib/icons/Load.svelte";

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

  $: {
    console.log("Bus component re-rendering with data:", data);
    console.log("Bus number:", data.busNum);
    console.log("Angle:", data.angle);
    console.log("Voltage:", data.voltage);
  }

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
    return parseFloat(value).toFixed(3); // Increased precision for debugging
  }

  $: {
    console.log("Bus component re-rendering with data:", data);
    console.log("Bus number:", data.busNum);
    console.log("Angle:", data.angle);
    console.log("Voltage:", data.voltage);
  }
</script>

<div
  class="relative my-10 block items-center border border-black bg-blue-800 text-center"
  style={`
    height: ${BUS_HEIGHT}px;
    width: 10px;
    position: relative;
  `}
>
  <!-- voltage and angle: above the body -->
  {#if voltage !== null}
    <div
      class="absolute bottom-full mx-auto w-full items-center text-center text-xs text-black"
      style="background-color: white; padding: 2px;"
    >
      {formatFloat(voltage)} kV ∠{formatFloat(angle)}°
    </div>
  {/if}

  <!-- label: inside the top edge -->
  <div
    class="absolute top-0 mx-auto w-full items-center bg-black text-center text-xs text-border"
  >
    {busNum}
  </div>

  <!-- inputs: into the left side -->
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

  <!-- outputs: out of the right side -->
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
