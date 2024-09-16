<script lang="ts">
  import { writable } from "svelte/store";
  import {
    SvelteFlow,
    type Edge,
    type EdgeTypes,
    type Node,
    type NodeTypes,
    MarkerType,
  } from "@xyflow/svelte";
  import "@xyflow/svelte/dist/style.css";
  import BranchNode from "$lib/components/Branch.svelte";
  import BusNode from "$lib/components/Bus.svelte";
  import noderedFlow from "$lib/flow-ieee14.json";
  import Range from "$lib/components/Range.svelte";
  import watchedValues from "$lib/gen_watch.json";

  type NoderedFlowNode = Omit<(typeof noderedFlow)[number], "id" | "z"> & {
    numGenerators?: number;
    numLoads?: number;
    numBranchesFrom?: number;
    numBranchesTo?: number;
    sourceBus?: string;
  };

  const noderedFlowNodes: Record<string, NoderedFlowNode> = {};
  for (const { type, name, id, z, ...rest } of noderedFlow) {
    if (
      type === "bus-data" ||
      type === "branch-data" ||
      type === "generator-data" ||
      type === "load-data"
    ) {
      if (type !== "bus-data") {
        noderedFlowNodes[id] = { type, ...rest };
      } else {
        noderedFlowNodes[id] = {
          type,
          ...rest,
          name: name!.split(" ")[1],
          numGenerators: 0,
          numLoads: 0,
          numBranchesFrom: 0,
          numBranchesTo: 0,
        };
      }
    }
  }

  const numUsedSourceHandles: Record<string, number> = {};
  const numUsedTargetHandles: Record<string, number> = {};
  for (const node of Object.values(noderedFlowNodes)) {
    const wires = node.wires![0];
    if (node.type === "generator-data") {
      const busId = wires[0];
      noderedFlowNodes[busId].numGenerators!++;
    } else if (node.type === "branch-data") {
      const busId = wires[0];
      noderedFlowNodes[busId].numBranchesTo!++;
    } else if (node.type === "bus-data") {
      numUsedSourceHandles[node.name!] = 0;
      numUsedTargetHandles[node.name!] = 0;

      for (const outId of wires) {
        const outNode = noderedFlowNodes[outId];
        if (outNode.type == "branch-data") {
          outNode.sourceBus = node.name;
          node.numBranchesFrom!++;
        } else if (outNode.type == "load-data") {
          node.numLoads!++;
        }
      }
    }
  }

  const xScale: number = 1;
  const yScale: number = 1;
  const nodeList: Node[] = Object.values(noderedFlowNodes)
    .filter(({ type }) => type === "bus-data")
    .map(
      ({
        name: busNum,
        x,
        y,
        numGenerators,
        numLoads,
        numBranchesFrom,
        numBranchesTo,
      }) => ({
        id: busNum!,
        type: "bus",
        position: { x: x! * xScale, y: y! * yScale },
        data: {
          busNum: busNum!,
          numGenerators,
          numLoads,
          numBranchesFrom,
          numBranchesTo,
          angle: null,
          voltage: null,
        },
      }),
    );

  const edgeList: Edge[] = Object.values(noderedFlowNodes)
    .filter(({ type }) => type === "branch-data")
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
        type: "straight",
        markerEnd: { type: MarkerType.ArrowClosed },
      };
    });

  let nodes = writable<Node[]>(nodeList);
  const edges = writable(edgeList);
  const nodeTypes: NodeTypes = { bus: BusNode };
  const edgeTypes: EdgeTypes = { branch: BranchNode };

  const times = Object.keys(watchedValues).sort();
  let curTimeIndex = 0;

  function updateValues({ timeIndex }: { timeIndex: number }) {
    const valuesAtBus = watchedValues[times[timeIndex]];

    nodes.update((currentNodes) => {
      console.log("Before update:", currentNodes); // Debugging before the update

      const updatedNodes = currentNodes.map((node) => {
        if (node.data.busNum in valuesAtBus) {
          const values = valuesAtBus[node.data.busNum];
          const updatedNode = {
            ...node,
            data: {
              ...node.data,
              angle: values.angle,
              voltage: values.voltage,
            },
          };

          // Log the angle for nodes with busNum == 3
          if (node.data.busNum == "3") {
            console.log(
              `Time: ${times[timeIndex]}\n BusNum: ${node.data.busNum}, Angle: ${values.angle} Voltage: ${values.voltage}`,
            );
          }

          return updatedNode;
        }
        return node;
      });

      console.log("After update:", updatedNodes); // Debugging after the update
      return updatedNodes;
    });
  }

  $: updateValues({ timeIndex: curTimeIndex });

  const className: string = "";
  export { className as class };
</script>

<div style="height: 100vh" class={className}>
  <SvelteFlow
    {nodes}
    {edges}
    {nodeTypes}
    {edgeTypes}
    fitView
    attributionPosition="top-right"
  />
</div>

<Range
  hoverText={times.map((time) => `${parseFloat(time).toFixed(2)} s`)}
  min={0}
  max={99}
  value={curTimeIndex}
  on:change={(e) => {
    curTimeIndex = e.detail.value;
  }}
/>

<style>
  :global(.svelte-flow__handle) {
    border-style: none;
    height: 0.25rem;
    width: 0.25rem;
  }
</style>
