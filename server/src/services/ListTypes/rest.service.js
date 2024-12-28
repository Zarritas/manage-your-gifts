import GenericService from "#services/generic.service.js";
import { db } from "#config/index.js";
const models = db.models;

export default class ListTypeService extends GenericService {
  constructor() {
    super(models.ListType);
  }
}
