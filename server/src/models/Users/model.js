import { Model } from "sequelize";
import { generateConfig } from "#models/common/index.js";

import { constants } from "#models/Users/index.js";

class User extends Model {
  static config(sequelize) {
    return generateConfig(
      sequelize,
      constants.USERS_TABLE,
      constants.USERS_MODEL,
      true
    );
  }

  static associate(models) {
    this.hasMany(models.List, { foreignKey: "userId" });
  }
}

export default User;
