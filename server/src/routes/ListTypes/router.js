import express from "express";
import { validateData } from "#middleware/index.js";
import { ListTypeController } from "#controllers/index.js";
import { ValidationListTypes } from "#validators/index.js";

const controller = new ListTypeController();

const router = express.Router();

router
  .get("/", controller.get)
  .get("/:id", controller.getByName)
  .post("/", ValidationListTypes.create, validateData, controller.create)
  .put("/:id", ValidationListTypes.update, validateData, controller.update)
  .delete("/:id", controller._delete);

export default router;
