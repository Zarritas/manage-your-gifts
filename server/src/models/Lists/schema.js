import { DataTypes } from "sequelize";

const ListSchema = {
  id: {
    allowNull: false,
    primaryKey: true,
    defaultValue: DataTypes.UUIDV4,
    type: DataTypes.UUID,
  },
  name: {
    allowNull: false,
    type: DataTypes.STRING,
  },
};

export default ListSchema;
