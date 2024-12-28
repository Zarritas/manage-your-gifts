import { Model } from "sequelize";
import { generateConfig } from "#models/common/index.js";
import { constants } from "#models/ListTypes/index.js";

class ListType extends Model {
  static config(sequelize) {
    return generateConfig(
      sequelize,
      constants.LIST_TYPES_TABLE,
      constants.LIST_TYPE_MODEL,
      true
    );
  }

  static associate(models) {
    this.hasMany(models.List, { foreignKey: "listTypeId" });
  }
}

export default ListType;
