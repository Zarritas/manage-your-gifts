import { GiftService } from "#services/index.js";
import { GenericController } from "#controllers/index.js";
import { db } from "#config/index.js";

class GiftController extends GenericController {
  constructor() {
    super(new GiftService(db.models));
  }
}

export default GiftController;
