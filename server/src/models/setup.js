import { ListTypes, Users, Gifts, Lists } from "#models/index.js";

const setupModels = (sequelize) => {
  setupInit(sequelize);
  setupAssociations(sequelize);
};

function setupInit(sequelize) {
  ListTypes.Model.init(ListTypes.Schema, ListTypes.Model.config(sequelize));
  Lists.Model.init(Lists.Schema, Lists.Model.config(sequelize));
  Gifts.Model.init(Gifts.Schema, Gifts.Model.config(sequelize));
  Users.Model.init(Users.Schema, Users.Model.config(sequelize));
}

function setupAssociations(sequelize) {
  Users.Model.associate(sequelize.models);
  Lists.Model.associate(sequelize.models);
  Gifts.Model.associate(sequelize.models);
  ListTypes.Model.associate(sequelize.models);
}

export default setupModels;
