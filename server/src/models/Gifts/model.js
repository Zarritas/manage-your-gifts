import { Model } from "sequelize";
import { generateConfig } from "#models/common/index.js";

import { constants } from "#models/Gifts/index.js";

class Gift extends Model {
  static config(sequelize) {
    return generateConfig(
      sequelize,
      constants.GIFTS_TABLE,
      constants.GIFTS_MODEL,
      true
    );
  }
  static associate(models) {
    this.belongsTo(models.List, { required: true, foreignKey: "listId" });
  }
}

export default Gift;
