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
	const spaceBetweenInputs = (BUS_HEIGHT - numGenerators * GENERATOR_HEIGHT) / numInputIntervals;
	const spaceBetweenOutputs = (BUS_HEIGHT - numLoads * LOAD_HEIGHT) / numOutputIntervals;

	function generatorTopOffset(i: number) {
		return i * (GENERATOR_HEIGHT + spaceBetweenInputs) + spaceBetweenInputs;
	}

	function inHandleTopOffset(i: number) {
		return numGenerators * (GENERATOR_HEIGHT + spaceBetweenInputs) + (i + 1) * spaceBetweenInputs;
	}

	function loadTopOffset(i: number) {
		return i * (LOAD_HEIGHT + spaceBetweenOutputs) + spaceBetweenOutputs;
	}

	function outHandleTopOffset(i: number) {
		return numLoads * (LOAD_HEIGHT + spaceBetweenOutputs) + (i + 1) * spaceBetweenOutputs;
	}

	function formatFloat(value: string | null): string {
		if (value === null) return '';
		return parseFloat(value).toFixed(2);
	}

	onMount(() => {
		console.log("RERENDERED!!!");
	});

	$: voltage, console.log(`voltage for ${busNum} is ${voltage}`);
</script>

<div
	class="relative my-10 bg-blue-800 border-black border text-center items-center block"
	style={`
		height: ${BUS_HEIGHT}px;
		width: 10px;
	`}
>
	<!-- voltage and angle: above the body -->
	{#if typeof voltage !== 'undefined' && voltage !== null}
		<div class="absolute bottom-full w-full text-black text-xs text-center items-center mx-auto">
			{formatFloat(voltage)} kV ∠{formatFloat(angle)}°
		</div>
	{/if}

	<!-- label: inside the top edge -->
	<div class="absolute top-0 w-full bg-black text-border text-xs text-center items-center mx-auto">
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
