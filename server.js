import { createServer } from "http";
import { config as dotenvConfig } from "dotenv";
import express from "express";
import nodeRed from "node-red";
import { handler as svelteKitHandler } from "./build/handler.js";

// Load .env file contents into `process.env`.
dotenvConfig();

/**
 * The Express app used by both SvelteKit and Node-RED
 * @type {import("express").Express}
 */
const app = express();

/**
 * The HTTP server used by both SvelteKit and Node-RED
 * @type {import("http").Server}
 */
const server = createServer(app);

const settings = {
  flowFile: process.env.FLOWS_FILENAME || "flows.json",
  httpAdminRoot: "/red",
  userDir: "./static/node-red",
  functionGlobalContext: {},
};

// Initialise the runtime with a server and settings
nodeRed.init(server, settings);

// Serve the editor UI from /red
app.use(settings.httpAdminRoot, nodeRed.httpAdmin);

// Let SvelteKit handle everything else, including serving prerendered pages and static assets
app.use(svelteKitHandler);

/// The port to serve the Node-RED editor on
const PORT = Number(process.env.PORT) || 3000;

server.listen(PORT, () => {
  console.log(`Listening for the Node-RED editor on port ${PORT}.`);
});

// Start the Node-RED runtime.
await nodeRed.start();
