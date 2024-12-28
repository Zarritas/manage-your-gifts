import { DataTypes } from "sequelize";

const ListTypeSchema = {
  id: {
    allowNull: false,
    autoIncrement: true,
    primaryKey: true,
    type: DataTypes.INTEGER,
  },
  name: {
    allowNull: false,
    field: "name",
    type: DataTypes.STRING,
  },
};

export default ListTypeSchema;
