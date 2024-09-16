<script lang="ts">
  import beprcLogo from "$lib/assets/images/beprc_logo.jpg";
  import pgcbLogo from "$lib/assets/images/pgcb_logo.png";
  import { Button } from "$components/ui/button";
  import Output from "$components/Output.svelte";

  let submitted = false;
  let resolved = false;
  let ready = false;
  let powerflowText = "Simulation not run yet";
  let dynsimText = "Simulation not run yet";

  // Delay function for simulating async operations
  const delay = (ms: number) => new Promise((res) => setTimeout(res, ms));

  async function handleSubmit() {
    submitted = true;
    try {
      // Simulate a delay before fetching data
      await delay(5000);

      // Simulate fetching data from an API
      // const response = await fetch("/results");
      // const body = await response.json();
      // Uncomment above lines and handle the real API response

      // For now, simulate data fetching success
      powerflowText = "Powerflow simulation results...";
      dynsimText = "Dynamic simulation results...";

      ready = true;
      resolved = true;
    } catch (error) {
      console.error("Error fetching simulation results:", error);
      // Handle error appropriately
      powerflowText = "Error fetching powerflow simulation results.";
      dynsimText = "Error fetching dynamic simulation results.";
    }
  }
</script>

<div class="min-h-full">
  <div class="bg-primary pb-32">
    <header class="py-14">
      <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div class="mb-8 flex items-center justify-center gap-10">
          <img src={beprcLogo} alt="BEPRC Logo" class="h-32" />
          <h1
            class="text-center text-3xl font-bold tracking-tight text-background"
          >
            Cyber–Physical Systems Testbed
          </h1>
          <img src={pgcbLogo} alt="PGCB Logo" class="h-32" />
        </div>
      </div>
    </header>
  </div>

  <main class="-mt-32 grid grid-cols-2">
    <div class="relative flex max-w-none flex-col px-4 pr-0 sm:px-6 lg:px-8">
      <section
        class="w-11/12 self-center rounded-lg bg-primary-foreground px-5 py-6 shadow sm:px-6"
      >
        <iframe
          src="http://127.0.0.1:1881/"
          title="Node-RED canvas"
          frameborder="0"
          class="w-full rounded-lg"
          style="height: 100rem;"
        ></iframe>
        <Button
          id="submit-btn"
          on:click={handleSubmit}
          class="absolute bottom-0 left-1/2 inline-flex w-1/4 -translate-x-1/2 translate-y-1/2"
          >RUN SIMULATIONS</Button
        >
      </section>
    </div>

    <div class="relative flex max-w-none flex-col px-4 pr-0 sm:px-6 lg:px-8">
      <section
        class="w-11/12 self-center rounded-lg bg-primary-foreground px-5 py-6 shadow sm:px-6"
      >
        {#if ready}
          <Output class="w-full" />
        {:else}
          <p>Please run the simulation first</p>
        {/if}
      </section>
    </div>
  </main>
</div>

<style>
  /* Ensure the button is centered properly */
  #submit-btn {
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%) translateY(50%);
  }
</style>
