import { body } from "express-validator";
import { utils } from "#validators/index.js";

const create = [
  body("listTypeId").isInt().withMessage(utils.invalid_list_type_id),
  body("userId").isUUID().withMessage(utils.invalid_user_id),
  body("name")
    .isLength({ min: utils.name_min_length })
    .withMessage(utils.invalid_name_length)
    .notEmpty()
    .withMessage(utils.invalid_name),
];

const update = [
  body("listTypeId").optional().isInt().withMessage(utils.invalid_list_type_id),
  body("userId").optional().isUUID().withMessage(utils.invalid_user_id),
  body("name")
    .optional()
    .isLength({ min: utils.name_min_length })
    .withMessage(utils.invalid_name_length)
    .notEmpty()
    .withMessage(utils.invalid_name),
];

export default { create, update };
