import express from "express";
import { validateData } from "#middleware/index.js";
import { UserController } from "#controllers/index.js";
import { ValidationUsers } from "#validators/index.js";
import { Lists } from "#routes/index.js";

const controller = new UserController();

const router = express.Router();

router
  .get("/", controller.get)
  .get("/:id", controller.getByName)
  .post("/", ValidationUsers.create, validateData, controller.create)
  .put("/:id", ValidationUsers.update, validateData, controller.update)
  .delete("/:id", controller._delete)
  .use("/:userId/lists", Lists);

export default router;
