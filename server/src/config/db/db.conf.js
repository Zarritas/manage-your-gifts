import { Sequelize } from "sequelize";
import { setupModels } from "#models/index.js";
import "dotenv/config";

const db = new Sequelize(
  process.env.DB_NAME,
  process.env.DB_USER,
  process.env.DB_PASSWORD,
  {
    host: process.env.DB_HOST || "localhost",
    dialect: "postgres",
    logging: false,
    pool: {
      max: 5,
      min: 0,
      acquire: 30000,
      idle: 10000,
    },
  }
);
setupModels(db);
db.sync({ alter: true })
  .then(() => {
    console.log("Database & tables created!");
  })
  .catch((error) => {
    console.error("Unable to create database or tables : ", error);
  });

export default db;
