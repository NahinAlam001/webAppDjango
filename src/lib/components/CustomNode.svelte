<script lang="ts">
	import { Handle, type NodeProps, Position, useUpdateNodeInternals } from '@xyflow/svelte';

	type $$Props = NodeProps;
	export let id: $$Props['id'];
	export let data: $$Props['data'];
	export let isConnectable: $$Props['isConnectable'] = true;
	export let targetPosition: $$Props['targetPosition'] = Position.Top;
	export let sourcePosition: $$Props['sourcePosition'] = Position.Bottom;

	let handles = Array.from({ length: 7 });

	const updateNodeInternals = useUpdateNodeInternals();

	$: {
		handles;
		updateNodeInternals(id);
	}

	const addHandle = (index: number) => {
		handles = [...handles, index];
	};

	const removeHandle = (index: number) => {
		handles = handles.filter((_, i) => i !== index);
	};
</script>

<Handle type="target" position={targetPosition} {isConnectable} />
<div style:display="flex" style:gap="8px" style:alignItems="center" style:padding="10">
	{data?.label}
	<button on:click={() => addHandle(handles.length)}>+</button>
	<button on:click={() => removeHandle(handles.length - 1)}>-</button>
</div>

<div style:width="100%" style:display="flex" style:gap="4px" style:justifyContent="space-around">
	{#each handles as _, index (index)}
		<Handle
			id={`handle-${index}`}
			type="source"
			position={sourcePosition}
			{isConnectable}
			style="transform: none; left: unset; position: relative;"
		/>
	{/each}
</div>
