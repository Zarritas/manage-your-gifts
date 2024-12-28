import { ListService } from "#services/index.js";
import { GenericController } from "#controllers/index.js";
import { db } from "#config/index.js";

export default class ListController extends GenericController {
  constructor() {
    super(new ListService(db.models));
  }

  // Metodos especificos de Lists
}
