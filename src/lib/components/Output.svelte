<script lang="ts">
	import { writable } from 'svelte/store';
	import {
		SvelteFlow,
		type Edge,
		type EdgeTypes,
		type Node,
		type NodeTypes,
		MarkerType,
		useSvelteFlow,
	} from '@xyflow/svelte';
	import '@xyflow/svelte/dist/style.css';
	import BranchNode from '$lib/components/Branch.svelte';
	import BusNode from '$lib/components/Bus.svelte';
	import noderedFlow from '$lib/flow-ieee14.json';

	// import { Slider } from "$lib/components/ui/slider";
	import Range from "$lib/components/Range.svelte";

	import watchedValues from '$lib/gen_watch.json';
    import { updated } from '$app/stores';
    import { onMount } from 'svelte';


	type NoderedFlowNode = Omit<(typeof noderedFlow)[number], 'id' | 'z'> & {
		numGenerators?: number;
		numLoads?: number;
		numBranchesFrom?: number;
		numBranchesTo?: number;

		/** bus number  */
		sourceBus?: string;
	};
	/** Node-RED node's id to Node-RED node */
	const noderedFlowNodes: Record<string, NoderedFlowNode> = {};
	for (const { type, name, id, z, ...rest } of noderedFlow) {
		// z is discarded
		if (
			type === 'bus-data' ||
			type === 'branch-data' ||
			type === 'generator-data' ||
			type === 'load-data'
		) {
			if (type !== 'bus-data') {
				noderedFlowNodes[id] = { type, ...rest };
			} else {
				noderedFlowNodes[id] = {
					type,
					...rest,
					name: name!.split(' ')[1], // bus number
					numGenerators: 0,
					numLoads: 0,
					numBranchesFrom: 0,
					numBranchesTo: 0
				};
			}
		}
	}

	const numUsedSourceHandles: Record<string, number> = {};
	const numUsedTargetHandles: Record<string, number> = {};
	for (const node of Object.values(noderedFlowNodes)) {
		const wires = node.wires![0];
		if (node.type === 'generator-data') {
			const busId = wires[0];
			noderedFlowNodes[busId].numGenerators!++;
		} else if (node.type === 'branch-data') {
			const busId = wires[0];
			noderedFlowNodes[busId].numBranchesTo!++;
		} else if (node.type === 'bus-data') {
			numUsedSourceHandles[node.name!] = 0;
			numUsedTargetHandles[node.name!] = 0;

			for (const outId of wires) {
				const outNode = noderedFlowNodes[outId];
				if (outNode.type == 'branch-data') {
					outNode.sourceBus = node.name; // bus number
					node.numBranchesFrom!++;
				} else if (outNode.type == 'load-data') {
					node.numLoads!++;
				}
			}
		}
	}

	const xScale: number = 1;
	const yScale: number = 1;
	const nodeList: Node[] = Object.values(noderedFlowNodes)
		.filter(({ type }) => type === 'bus-data')
		.map(({ name: busNum, x, y, numGenerators, numLoads, numBranchesFrom, numBranchesTo }) => {
			return {
				id: busNum!,
				type: 'bus',
				position: { x: x! * xScale, y: y! * yScale },
				data: {
					busNum: busNum!,
					numGenerators,
					numLoads,
					numBranchesFrom,
					numBranchesTo,
					angle: null,
					voltage: null,
				}
			} satisfies Node;
		});

	const edgeList: Edge[] = Object.values(noderedFlowNodes)
		.filter(({ type }) => type === 'branch-data')
		.map(({ sourceBus, wires }) => {
			const source = sourceBus!;
			const target = noderedFlowNodes[wires![0][0]].name!;
			return {
				id: `${source}-${target}`,
				source,
				target,
				sourceHandle: `out-${numUsedSourceHandles[source]++}`,
				targetHandle: `in-${numUsedTargetHandles[target]++}`,
				animated: true,
				type: 'straight',
				markerEnd: { type: MarkerType.ArrowClosed }
			} satisfies Edge;
		});

	let nodes = writable<Node[]>(nodeList);
	const edges = writable(edgeList);
	const nodeTypes: NodeTypes = { bus: BusNode };
	const edgeTypes: EdgeTypes = { branch: BranchNode };

	// const timeSeries: Record<string, Record<string, { angle: string, voltage: string }>> = {};
	// const times: Array<any> = [];
	// for (const item of genWatchData) {
	// 	const { time, ...rest } = item;
	// 	timeSeries[time] = rest.data;
	// 	times.push(time);
	// }

	const times = Object.keys(watchedValues).sort();
	let curTimeIndex = 0;
	// const { updateNodeData } = useSvelteFlow();
	// let sliderThumbValues = [0];
	function updateValues({ timeIndex }: { timeIndex: number }) {
		const valuesAtBus: Record<string, { angle: string, voltage: string }> = watchedValues[times[timeIndex]];
		// Object.entries(valuesAtBus).forEach(([busNum, { angle, voltage }]) => {
		// 	console.log(busNum, angle, voltage);
		// 	updateNodeData(busNum, { angle, voltage });
		// });
		$nodes.forEach((node) => {
			if (node.data.busNum in valuesAtBus) {
				const values = valuesAtBus[node.data.busNum];
				node.data = {
					...node.data,
					angle: values.angle,
					voltage: values.voltage,
				};
				$nodes = $nodes;
				console.log(node.data.busNum, values, $nodes);
			}
		});
		// console.log($nodes);
		// const valuesAtBus: Record<string, { angle: string, voltage: string }> = genWatchData[times[timeIndex]];
		// // console.log(valuesAtBus);
		// const newNodes = $nodes
		// 	.filter((node) => node.data.busNum in valuesAtBus)
		// 	.map((node) => {
		// 		const values = valuesAtBus[node.data.busNum];
		// 		console.log(values, node.data.busNum);
		// 		node.data = {
		// 			...node.data,
		// 			angle: values.angle,
		// 			voltage: values.voltage,
		// 		};
		// 		return node;
		// 	});
		// $nodes = newNodes;
	}
	$: updateValues({ timeIndex: curTimeIndex }), console.log(`curTimeIndex: ${curTimeIndex}`);

	const className: string = "";
	export { className as class };
</script>


<div style="height: 100vh" class={className}>
	<SvelteFlow {nodes} {edges} {nodeTypes} {edgeTypes} fitView attributionPosition="top-right" />
</div>

<!-- <Slider value={sliderThumbValues} max={100} onValueChange={(newPositions) => sliderThumbValues = newPositions} /> -->
<Range
	hoverText={times.map((time) => `${parseFloat(time).toFixed(2)} s`)}
	min={0}
	max={99}
	value={curTimeIndex}
	on:change={(e) => {
		curTimeIndex = e.detail.value;
		// updateValues({ timeIndex: curTimeIndex });
	}}
/>


<style>
	/* reduce visibility of the black circles */
	:global(.svelte-flow__handle) {
		border-style: none;
		height: 0.25rem;
		width: 0.25rem;
	}
</style>
