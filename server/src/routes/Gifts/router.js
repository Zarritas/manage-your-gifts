import express from "express";
import { validateData } from "#middleware/index.js";
import { GiftController } from "#controllers/index.js";
import { ValidationGifts } from "#validators/index.js";

const controller = new GiftController();

const router = express.Router({ mergeParams: true });

router
  .get("/", controller.get)
  .get("/:id", controller.getByName)
  .post("/", ValidationGifts.create, validateData, controller.create)
  .put("/:id", ValidationGifts.update, validateData, controller.update)
  .delete("/:id", controller._delete);

export default router;
