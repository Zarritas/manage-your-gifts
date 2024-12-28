import express from "express";
import { validateData } from "#middleware/index.js";
import { ListController } from "#controllers/index.js";
import { ValidationLists } from "#validators/index.js";
import { Gifts } from "#routes/index.js";

const controller = new ListController();

const router = express.Router({ mergeParams: true });

router
  .get("/", controller.get)
  .get("/:id", controller.getByName)
  .post("/", ValidationLists.create, validateData, controller.create)
  .put("/:id", ValidationLists.update, validateData, controller.update)
  .delete("/:id", controller._delete)
  .use("/:listId/gifts", Gifts);

export default router;
