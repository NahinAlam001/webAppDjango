<script lang="ts">
  // import * as Tabs from "$lib/components/ui/tabs";
  import beprcLogo from "$lib/assets/images/beprc_logo.jpg";
  import pgcbLogo from "$lib/assets/images/pgcb_logo.png";

  let submitted = false;
  let resolved = false;
  // let resultsPromise: Promise<Response>;

  // let branchPowerflow;
  // let generatorPowers;
  // let busVoltagesAndPhaseAngles;

  // let powerflowText: string = "Simulation not run yet";
  // let dynsimText: string = "Simulation not run yet";
  let ready: boolean = false;
  const delay = ms => new Promise(res => setTimeout(res, ms));

  async function handleSubmit() {
    submitted = true;
    // const response = await fetch("/results");
    // const body = await response.json();
    // console.log(body.pf);
    // console.log(body.ds);
    // powerflowText = body.pf;
    // dynsimText = body.ds;
    await delay(5000);
    ready = true;
    resolved = true;
    // console.log(await body?.getReader().read());
/*
    // console.log(`Response: ${JSON.stringify(response)}`);
    const body = JSON.parse(await response.json());
    // console.log(`Response: ${body}`);
    // for (const key in body) {
    //   console.log(`${key}: ${body[key]}`);
    // }
    branchPowerflow = body["branchPowerflow"];
    console.log(`branchPowerflow: ${branchPowerflow}`);
    generatorPowers = body["generatorPower"];
    console.log(`generatorPowers: ${generatorPowers}`);
    busVoltagesAndPhaseAngles = body["busVoltagesAndPhaseAngles"];
    console.log(`busVoltagesAndPhaseAngles: ${busVoltagesAndPhaseAngles}`);
    resolved = true;
*/

    // {}).catch((reason) => {
    //   console.log(JSON.stringify(reason));
    // }).finally(() => {
    //   console.log(`Nothing found`);
    // });
  }

  // type BranchPowerflow = {
  //   bus1: number;
  //   bus2: number;
  //   ckt: string;
  //   p: number;
  //   q: number;
  // };
  // type GeneratorPower = {
  //   busNumber: number;
  //   genId: number;
  //   pGen: number;
  //   qGen: number;
  // };
  // type BusVoltageAndPhaseAngle = {};
  // type Results = {
  //   branchPowerflow: Array<BranchPowerflow>;
  //   generatorPowers: Array<GeneratorPower>;
  //   busVoltagesAndPhaseAngles: Array<BusVoltageAndPhaseAngle>;
  // };
  // import data from "$lib/assets/output.json";
  // import { ArrowUpDown, MoreHorizontal, ChevronsUpDown } from "lucide-svelte";
  // import {
  //   Table,
  //   TableBody,
  //   TableCaption,
  //   TableCell,
  //   TableHead,
  //   TableHeader,
  //   TableRow,
  // } from "$components/ui/table";
  import { Button } from "$components/ui/button";
  import { SvelteFlowProvider } from "@xyflow/svelte";
  import Output from "$components/Output.svelte";

  // function sort(data: Array<any>, key: string, asc: boolean = true): void {
  //   data.sort((a, b) => {
  //     if (a[key] == b[key]) return 0;
  //     const aThenB = a[key] < b[key];
  //     return aThenB == asc ? -1 : +1;
  //   });
  // }

  // function toggleDarkMode() {
  //   window.document.body.classList.toggle("dark");
  // }

  // let isOpen = false;
</script>

<!-- <Button on:click={toggleDarkMode}>Dark Mode</Button> -->

<div class="min-h-full">
  <div class="bg-primary pb-32">
    <header class="py-14">
      <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div class="flex justify-center mb-8 gap-10 items-center">
          <img src={beprcLogo} alt="BEPRC Logo" class="h-32" />
          <h1 class="text-center text-3xl font-bold tracking-tight text-background">
            Cyber–Physical Systems Testbed
          </h1>
          <img src={pgcbLogo} alt="PGCB Logo" class="h-32" />
        </div>
      </div>
    </header>
  </div>

  <main class="-mt-32 grid grid-cols-2">
    <div class="relative flex max-w-none flex-col px-4 sm:px-6 lg:px-8 pr-0 lg:pr-0 sm:pr-0">
      <section
        class="rounded-lg bg-primary-foreground px-5 py-6 shadow sm:px-6 w-11/12 self-center"
      >
        <iframe
          src="http://127.0.0.1:1881/"
          title="Node-RED canvas"
          frameborder="0"
          class="w-full rounded-lg"
          style="height: 100rem;"
        />
        <Button
          id="submit-btn"
          on:click={handleSubmit}
          class="absolute bottom-0 left-1/2 inline-flex -translate-x-1/2 translate-y-1/2 w-1/4"
          >RUN SIMULATIONS</Button
        >
      </section>
    </div>

    <div class="relative flex max-w-none flex-col px-4 sm:px-6 lg:px-8 pr-0 lg:pr-0 sm:pr-0">
      <section
        class="rounded-lg bg-primary-foreground px-5 py-6 shadow sm:px-6 w-11/12 self-center"
      >
        <!-- <SvelteFlowProvider> -->
          {#if ready}
            <Output class="w-full" />
          {:else}
            <p>Please run the simulation first</p>
          {/if}
        <!-- </SvelteFlowProvider> -->
      </section>
    </div>

<!--
    <div class="relative flex max-w-none flex-col px-4 sm:px-6 lg:px-8 pl-0 lg:pl-0 sm:pl-0">
      <section class="rounded-lg px-5 py-6 shadow sm:px-6 w-11/12 self-center">

        <Tabs.Root value="powerflow" class="w-full" style="height: 100rem;">
          <Tabs.List class="w-full">
            <Tabs.Trigger class=w-ful value="powerflow">Powerflow</Tabs.Trigger>
            <Tabs.Trigger class=w-ful value="dynsim">Dynamic Simulation</Tabs.Trigger>
          </Tabs.List>
          <Tabs.Content value="powerflow">
            {#if ready}
              <pre>{powerflowText}</pre>
            {:else}
              {dynsimText}
            {/if}
 -->
          <!--
          <Accordion type="single" collapsible class="w-full">
            <AccordionItem value="powerflow">
              <AccordionTrigger>BRANCH POWERFLOW</AccordionTrigger>
              <AccordionContent>
                {#if !submitted}
                  No design submitted.
                {:else if !resolved}
                  Calculating results...
                {:else}
                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead>
                          <Button variant="ghost"
                            >Bus 1 <ArrowUpDown class="ml-2 h-4 w-4" /></Button
                          >
                        </TableHead>
                        <TableHead>Bus 2</TableHead>
                        <TableHead>CKT</TableHead>
                        <TableHead>Real power, <math><mi>P</mi></math></TableHead>
                        <TableHead>Reactive power, <math><mi>Q</mi></math></TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {#each branchPowerflow as pf}
                        <TableRow>
                          <TableCell>{pf.bus1}</TableCell>
                          <TableCell>{pf.bus2}</TableCell>
                          <TableCell>{pf.ckt}</TableCell>
                          <TableCell>{formatFloat(pf.p)}</TableCell>
                          <TableCell>{formatFloat(pf.q)}</TableCell>
                        </TableRow>
                      {/each}
                    </TableBody>
                  </Table>
                {/if}
              </AccordionContent>
            </AccordionItem>
            <AccordionItem value="generator_power">
              <AccordionTrigger>GENERATOR POWERS</AccordionTrigger>
              <AccordionContent>
                {#if !submitted}
                  No design submitted.
                {:else if !resolved}
                  Calculating results...
                {:else}
                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead>
                          <Button variant="ghost"
                            >Bus Number <ArrowUpDown
                              class="ml-2 h-4 w-4"
                            /></Button
                          >
                        </TableHead>
                        <TableHead>Generator ID</TableHead>
                        <TableHead>PGen</TableHead>
                        <TableHead>QGen</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {#each generatorPowers as gp}
                        <TableRow>
                          <TableCell>{gp.busNumber}</TableCell>
                          <TableCell>{gp.genId}</TableCell>
                          <TableCell>{formatFloat(gp.pGen)}</TableCell>
                          <TableCell>{formatFloat(gp.qGen)}</TableCell>
                        </TableRow>
                      {/each}
                    </TableBody>
                  </Table>
                {/if}
              </AccordionContent>
            </AccordionItem>
            <AccordionItem value="voltage_angle">
              <AccordionTrigger>BUS PHASE ANGLES AND VOLTAGES</AccordionTrigger>
              <AccordionContent>
                {#if !submitted}
                  No design submitted.
                {:else if !resolved}
                  Calculating results...
                {:else}
                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead>
                          <Button variant="ghost"
                            >Bus Number <ArrowUpDown
                              class="ml-2 h-4 w-4"
                            /></Button
                          >
                        </TableHead>
                        <TableHead>Phase Angle</TableHead>
                        <TableHead>Voltage Magnitude</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {#each busVoltagesAndPhaseAngles as va}
                        <TableRow>
                          <TableCell>{va.busNumber}</TableCell>
                          <TableCell>{formatFloat(va.phaseAngle)}</TableCell>
                          <TableCell>{formatFloat(va.voltageMagnitude)}</TableCell
                          >
                        </TableRow>
                      {/each}
                    </TableBody>
                  </Table>
                {/if}
              </AccordionContent>
            </AccordionItem>
          </Accordion>
          -->

<!--
          </Tabs.Content>
          <Tabs.Content value="dynsim">
            {#if ready}
              <Output className="w-full" />
            {:else}
              {dynsimText}
            {/if}
          </Tabs.Content>
        </Tabs.Root>
      </section>
    </div>
-->
  </main>
</div>
