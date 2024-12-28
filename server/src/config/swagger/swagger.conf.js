import { serve, setup } from "swagger-ui-express";
import { readFileSync } from "fs";
import { parse } from "yaml";

const file = readFileSync(`${process.cwd()}/docs/swagger.yaml`, "utf8");

const swaggerDocsOptions = parse(file);

const swaggerDocs = (app) => {
  app.use("/api-docs", serve, setup(swaggerDocsOptions));
};

export default swaggerDocs;
