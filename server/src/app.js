import cors from "cors";
import pkg from "body-parser";
import { setupRouterApi } from "#routes/index.js";
import "dotenv/config";
import { errorHandler } from "#middleware/index.js";

import express from "express";
const app = express();

import { setupConfig } from "#config/index.js";
setupConfig(app);

app
  .use(cors())
  .use(pkg.json())
  .use(pkg.urlencoded({ extended: true }));

setupRouterApi(app);

app.use(errorHandler);

export default app;
