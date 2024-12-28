import { body } from "express-validator";
import { utils } from "#validators/index.js";

const create = [
  body("name")
    .isLength({ min: utils.name_min_length })
    .withMessage(utils.invalid_name_length)
    .notEmpty()
    .withMessage(utils.invalid_name),
  body("description")
    .optional()
    .isString()
    .withMessage(utils.invalid_description),
  body("price").optional().isFloat({ min: 0 }).withMessage(utils.invalid_price),
  body("urls")
    .optional()
    .isArray()
    .withMessage(utils.invalid_urls)
    .custom((value) => value.every((url) => utils.regex.test(url)))
    .withMessage(utils.invalid_each_url),
  body("image").optional().isString().withMessage(utils.invalid_image),
  body("listId").isUUID().withMessage(utils.invalid_list_id),
];

const update = [
  body("name")
    .optional()
    .isLength({ min: utils.name_min_length })
    .withMessage(utils.invalid_name_length)
    .notEmpty()
    .withMessage(utils.invalid_name),
  body("description")
    .optional()
    .isString()
    .withMessage(utils.invalid_description),
  body("price").optional().isFloat({ min: 0 }).withMessage(utils.invalid_price),
  body("urls")
    .optional()
    .isArray()
    .withMessage(utils.invalid_urls)
    .custom((value) => value.every((url) => utils.url_regex.test(url)))
    .withMessage(utils.invalid_each_url),
  body("image").optional().isString().withMessage(utils.invalid_image),
  body("listId").optional().isUUID().withMessage(utils.invalid_list_id),
];

export default { create, update };
