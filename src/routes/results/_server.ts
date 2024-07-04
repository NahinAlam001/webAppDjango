import type { RequestHandler } from "./$types";
import { json } from "@sveltejs/kit";
import { exec as legacyExec } from "node:child_process";
import { promisify } from "node:util";
import { readFile } from "fs/promises";

const STATIC_ROOT = "./static";
const scriptFilePath = `convert.py`;
const flowsFilePath = "/home/cpslab/.node-red/flows.json";
// const basePath = `/home/cpslab/Downloads/testbed_backend/cmake-build/core`;
const basePath = `/home/cpslab/GridPACK/src/build/applications/dynamic_simulation_full_y`;
const inputPath = `${basePath}/input.xml`;
// const outPathPF = `/home/cpslab/Downloads/testbed_backend/cmake-build/core/simulationoutput.json`;
const outPathDS = `${basePath}/gen_watch.csv`;
// const pfPath = `/home/cpslab/Downloads/testbed_backend/cmake-build/core/simulation`;
const dsPath = `${basePath}/dsf.x`;

const cmdGenRAW = `python3 ${scriptFilePath} ${flowsFilePath}`;
// const cmd2 = `dsf_json.x ${inputPath}`;
const cmdPf = `${dsPath} ${inputPath}`;
// const cmdDS = `${dsPath} ${inputPath}`;
const cmdDS = `cd ${basePath} && ./dsf.x input.xml`;

const exec = promisify(legacyExec);

export const GET: RequestHandler = async () => {
  // console.log(cmdGenRAW);
  // const r1 = await exec(cmdGenRAW);
  // console.log(`stdout1: ${r1.stdout}`)
  // console.log(`stderr1: ${r1.stderr}`)

  // const r2 = await exec(cmd2);
  // console.log(`stdout2: ${r2.stdout}`)
  // console.log(`stderr2: ${r2.stderr}`)

  const r2 = await exec(cmdDS);
  console.log(`stdout2: ${r2.stdout}`);
  console.log(`stderr2: ${r2.stderr}`);

  // const jsonModule = await import(outPathPF, { assert: { type: "json" } });
  // return json(jsonModule.default);
  const fileOut = await readFile(outPathDS, "utf8");
  // console.log(`Output JSON: ${fileOut}`);
  // return json(await JSON.parse(fileOut));
  // return json(fileOut);
  return json({
    pf: r2.stdout,
    ds: fileOut,
  });
};
