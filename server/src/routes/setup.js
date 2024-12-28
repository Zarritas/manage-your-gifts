import express from "express";
import { ListTypes, Gifts, Lists, Users } from "#routes/index.js";

export default function setupRouterApi(app) {
  const router = express.Router();

  app.use("/api", router);
  router
    .use("/listTypes", ListTypes)
    .use("/users", Users)
    .use("/lists", Lists)
    .use("/gifts", Gifts);
}
