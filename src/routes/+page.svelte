<script lang="ts">
  import { onMount, onDestroy } from "svelte";
  import { createEventDispatcher } from "svelte";
  import Output from "$lib/components/Output.svelte"; // Assume Output component is implemented

  const dispatch = createEventDispatcher();

  let submitted = false;
  let resolved = false;
  let ready = false;
  let powerflowText = "";
  let dynsimText = "";

  async function handleSubmit() {
    console.log("Simulation submitted.");
    try {
      // Simulate delay for fetching results
      await new Promise((resolve) => setTimeout(resolve, 5000));

      // Simulate results
      powerflowText = "Powerflow simulation results...";
      dynsimText = "Dynamic simulation results...";
      ready = true;
      resolved = true;

      console.log("Simulation results updated.");
    } catch (error) {
      console.error("Error fetching simulation results:", error);
    }
  }

  // Cleanup if needed
  onDestroy(() => {
    // Clean up logic if needed
  });
</script>

<button on:click={handleSubmit}>Run Simulation</button>

{#if resolved}
  <Output {powerflowText} {dynsimText} />
{/if}

<style>
  button {
    padding: 0.5rem 1rem;
    background-color: #3b82f6;
    color: white;
    border: none;
    border-radius: 0.25rem;
    cursor: pointer;
    font-size: 1rem;
  }

  button:hover {
    background-color: #2563eb;
  }
</style>
