import { UserService } from "#services/index.js";
import { GenericController } from "#controllers/index.js";
import { db } from "#config/index.js";

export default class UserController extends GenericController {
  constructor() {
    super(new UserService(db.models));
  }
}
