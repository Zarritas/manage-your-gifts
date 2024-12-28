import "#utils/banner.js";
import "dotenv/config";
import logger from "morgan";
import { app } from "#src/index.js";
app.use(logger("dev"));

import { createServer } from "http";
const server = createServer(app);

import { constants } from "#config/index.js";
global.constants = constants;

const PORT = process.env.PORT || constants.HTTP_STATUS.INTERNAL_SERVER_ERROR;

server.listen(PORT, () => {
  console.log(`Server runing on http://localhost:${PORT}`);
});

export default server;
