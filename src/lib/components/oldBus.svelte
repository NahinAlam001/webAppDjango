<script lang="ts">
	import type { Writable } from 'svelte/store';
	import { Handle, Position, type NodeProps } from '@xyflow/svelte';

	type $$Props = NodeProps;

	export let data: {
		busNumber: string;
		numGenerators: number;
		numLoads: number;
		numBranchesFrom: number;
		numBranchesTo: number;
	};

	const { busNumber, numGenerators, numLoads, numBranchesFrom, numBranchesTo } = data;

	const HEIGHT = 64; // px
	const numInputIntervals = numGenerators + numBranchesTo + 1;
	// const spaceBetweenInputs = HEIGHT / numInputIntervals;
	const numOutputIntervals = numLoads + numBranchesFrom + 1;
	// const spaceBetweenOutputs = HEIGHT / numOutputIntervals;
</script>

<!--
<div
	style:height="100%"
	style:display="flex"
	style:flex-direction="column"
	style:justify-content="space-between"
	style:gap="2rem"
>
 -->
{#each Array.from({ length: numGenerators }) as _, i (i)}
	<div
		id={`in-${i}`}
		style:position="absolute"
		style:right="100%"
		style:top={`${((i + 1) / numInputIntervals) * 100}%`}
		style:color="red"
	>
		G
	</div>
{/each}
{#each Array.from({ length: numBranchesTo }) as _, i (i)}
	<Handle
		isConnectable={false}
		type="target"
		id={`in-${i}`}
		position={Position.Left}
		style={`top: ${((i + 1 + numGenerators) / numInputIntervals) * 100}%`}
	/>
{/each}


<div class="flex flex-col items-center">
	{busNumber}
	<div class="busbar"></div>
</div>

{#each Array.from({ length: numLoads }) as _, i (i)}
	<div
		id={`in-${i}`}
		style:position="absolute"
		style:left="100%"
		style:top={`${((i + 1) / numOutputIntervals) * 100}%`}
		style:color="green"
	>
		L
	</div>
{/each}
<!-- <div class="h-full flex flex-col justify-between gap-8"> -->
{#each Array.from({ length: numBranchesFrom }) as _, i (i)}
	<Handle
		isConnectable={false}
		type="source"
		id={`out-${i}`}
		position={Position.Right}
		style={`top: ${((i + 1 + numLoads) / numOutputIntervals) * 100}%`}
	/>
{/each}

<!-- <Handle type="source" position={Position.Right} on:connect on:connectend on:connectstart /> -->
<style>
	/* :global(.handles) {
		display: flex;
		flex-direction: column;
		justify-content: space-between;
		gap: 0.25rem;
	} */
	:global(.busbar) {
		height: 64px; /* make sure this is the same as the HEIGHT const */
		width: 4px;
		background: darkblue;
		/*		background: white;*/
		/*		border: 1px solid #000;*/
	}
</style>
