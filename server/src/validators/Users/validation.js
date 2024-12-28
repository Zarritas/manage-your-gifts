import { body } from "express-validator";
import { utils } from "#validators/index.js";

const create = [
  body("username").isString().withMessage(utils.invalid_username),
  body("email").isEmail().withMessage(utils.invalid_email),
  body("password").matches(utils.regex).withMessage(utils.invalid_password),
];

const update = [
  body("username").optional().isString().withMessage(utils.invalid_username),
  body("email").optional().isEmail().withMessage(utils.invalid_email),
  body("password")
    .optional()
    .matches(utils.regex)
    .withMessage(utils.invalid_password),
];

export default { create, update };
