import { body } from "express-validator";
import { utils } from "#validators/index.js";

const create = [
  body("name")
    .isLength({ min: utils.name_min_length })
    .withMessage(utils.invalid_name_length)
    .notEmpty()
    .withMessage(utils.invalid_name),
];

const update = [
  body("name")
    .optional()
    .isLength({ min: utils.name_min_length })
    .withMessage(utils.invalid_name_length)
    .notEmpty()
    .withMessage(utils.invalid_name),
];

export default { create, update };
