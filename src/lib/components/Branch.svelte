<script lang="ts">
  import { onMount } from "svelte";
  import { createEventDispatcher } from "svelte";
  import { BaseEdge, EdgeLabelRenderer } from "@xyflow/svelte";

  export let source = { x: 0, y: 0 };
  export let target = { x: 0, y: 0 };
  export let sourceHandle = null;
  export let targetHandle = null;
  export let sourcePos = null;
  export let targetPos = null;

  const dispatch = createEventDispatcher();

  let edgePath = "";
  let labelX = 0;
  let labelY = 0;

  // Function to compute the path and label position
  function getBezierPath({ sourceX, sourceY, targetX, targetY }) {
    // Adjust path and label positions based on source and target positions
    const path = `M ${sourceX} ${sourceY} C ${sourceX + (targetX - sourceX) / 2} ${sourceY} ${sourceX + (targetX - sourceX) / 2} ${targetY} ${targetX} ${targetY}`;
    const labelX = (sourceX + targetX) / 2;
    const labelY = (sourceY + targetY) / 2;

    return [path, labelX, labelY];
  }

  // Reactively compute edge path and label positions
  $: [edgePath, labelX, labelY] = getBezierPath({
    sourceX: source.x,
    sourceY: source.y,
    targetX: target.x,
    targetY: target.y,
  });

  $: console.log("Edge Path:", edgePath);
  $: console.log("Label Position:", labelX, labelY);
</script>

<svg>
  <BaseEdge {source} {target} {sourceHandle} {targetHandle} path={edgePath} />
  <EdgeLabelRenderer x={labelX} y={labelY} />
</svg>

<style>
  svg {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    overflow: visible;
  }
</style>
