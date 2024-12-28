import { asyncHandler } from "#middleware/index.js";

export default class GenericController {
  constructor(service) {
    this.service = service;
  }

  create = asyncHandler(async (req, res) => {
    const params = req.params;
    const body = req.body;
    const response = await this.service.create({ data: body, params });
    res.json({ success: true, data: response });
  });

  get = asyncHandler(async (req, res) => {
    const params = req.params;
    const { page, limit, attributes } = req.query;
    const response = await this.service.find({
      params,
      page: parseInt(page, 10) || 1,
      limit: parseInt(limit, 10) || 10,
      attributes: attributes ? attributes.split(",") : [],
    });
    res.json(response);
  });

  getByName = asyncHandler(async (req, res) => {
    const params = req.params;
    const { attributes } = req.query;

    const response = await this.service.findOne({
      where: params,
      attributes: attributes ? attributes.split(",") : [],
    });
    res.json(response);
  });

  update = asyncHandler(async (req, res) => {
    const params = req.params;
    const response = await this.service.update({ params, data: req.body });
    res.json(response);
  });

  _delete = asyncHandler(async (req, res) => {
    const { id } = req.params;
    const response = await this.service.delete({ id });
    res.json(response);
  });
}
