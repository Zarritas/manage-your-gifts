import { DataTypes } from "sequelize";

const GiftSchema = {
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
  description: {
    allowNull: true,
    type: DataTypes.STRING,
  },
  price: {
    allowNull: true,
    precision: 2,
    defaultValue: 0.0,
    type: DataTypes.DOUBLE,
  },
  urls: {
    allowNull: true,
    type: DataTypes.ARRAY(DataTypes.STRING),
  },
  image: {
    allowNull: true,
    type: DataTypes.STRING,
  },
};

export default GiftSchema;
