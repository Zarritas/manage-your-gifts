import GenericService from "#services/generic.service.js";
import { db } from "#config/index.js";
const models = db.models;

export default class GiftService extends GenericService {
  constructor() {
    super(models.Gift);
  }
}
