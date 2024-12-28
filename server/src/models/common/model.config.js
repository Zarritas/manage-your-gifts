const generateConfig = (sequelize, tableName, modelName, timestamps) => ({
  sequelize,
  tableName,
  modelName,
  timestamps,
});

export default generateConfig;
