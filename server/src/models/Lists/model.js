import { Model } from "sequelize";
import { generateConfig } from "#models/common/index.js";

import { constants } from "#models/Lists/index.js";

class List extends Model {
  static config(sequelize) {
    return generateConfig(
      sequelize,
      constants.LISTS_TABLE,
      constants.LISTS_MODEL,
      true
    );
  }

  static associate(models) {
    this.belongsTo(models.User, { required: true, foreignKey: "userId" });
    this.belongsTo(models.ListType, {
      required: true,
      foreignKey: "listTypeId",
    });
    this.hasMany(models.Gift, { foreignKey: "listId" });
  }
}

export default List;
