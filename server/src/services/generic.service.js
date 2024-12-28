export default class GenericService {
  constructor(model) {
    this.model = model;
  }

  async create({ data, params }) {
    const createData = { ...data, ...params };
    console.log("data", data, "params", params);
    console.error("createData", createData);
    const res = await this.model.create(createData);
    return res;
  }

  async find({ limit = 10, page = 1, attributes = [], params }) {
    console.log(
      "limit",
      limit,
      "page",
      page,
      "attributes",
      attributes,
      "params",
      params
    );
    const offset = (page - 1) * limit;

    if (limit < 1 || page < 1) return null;

    const { rows, count } = await this.model.findAndCountAll({
      where: params,
      limit,
      offset,
      attributes: attributes.length > 0 ? attributes : null,
    });

    return {
      data: rows,
      meta: {
        total: count,
        page,
        limit,
        totalPages: Math.ceil(count / limit),
      },
    };
  }

  async findOne({ attributes = [], params }) {
    console.log("attributes", attributes, "params", params);
    const res = await this.model.findOne({
      where: params,
      attributes: attributes.length > 0 ? attributes : null,
    });
    return res;
  }

  async update({ data, params }) {
    console.log("data", data, "params", params);
    const model = await this.model.findOne({ where: params });
    if (!model) return null;
    const res = await model.update(data);
    return res;
  }

  async delete({ params }) {
    console.log("params", params);
    const model = await this.model.findOne({ where: params });
    if (!model) return null;
    const res = await model.destroy();
    return "Deleted";
  }
}
