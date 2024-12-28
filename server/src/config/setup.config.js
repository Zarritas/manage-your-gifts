import { db, swaggerDocs, constants } from "#config/index.js";

export default function setupConfig(app) {
  global.constants = constants;
  swaggerDocs(app);
  db;
}
