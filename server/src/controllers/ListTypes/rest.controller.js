import { ListTypeService } from "#services/index.js";
import { GenericController } from "#controllers/index.js";
import { db } from "#config/index.js";

export default class ListTypeController extends GenericController {
  constructor() {
    super(new ListTypeService(db.models));
  }
}
