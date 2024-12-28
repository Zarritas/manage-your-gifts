// TODO: Mirar que cambios hay que hacer

export default {
  HTTP_STATUS: {
    OK: 200,
    CREATED: 201,
    NO_CONTENT: 204,
    BAD_REQUEST: 400,
    UNAUTHORIZED: 401,
    FORBIDDEN: 403,
    NOT_FOUND: 404,
    INTERNAL_SERVER_ERROR: 500,
  },
  ERROR: {
    MODEL_NOT_FOUND: (model) => `${model} not found`,
    GETTING_MODEL: (model) => `Error getting ${model}`,
    CREATING_MODEL: (model) => `Error creating ${model}`,
    UPDATING_MODEL: (model) => `Error updating ${model}`,
    DELETING_MODEL: (model) => `Error deleting ${model}`,
    INVALID_INPUT: "Invalid input provided",
    SOMETHING_WENT_WRONG: "Something went wrong",
    DATA_SENT: "Error in data sent",
    INVALID_CREDENTIALS: "Invalid credentials",
    ALREADY_EXISTS: (model) => `${model} not found`,
    UNAUTHORIZED: "Unauthorized",
    CONNECTION: (service) => `Unable to connect to the ${service}`,
  },
  SUCCESS: {
    CREATED: (model) => `${model} has been created successfully`,
    UPDATED: (model) => `${model} has been updated successfully`,
    DELETED: (model) => `${model} has been deleted successfully`,
    INITIAL: "Welcome to the API",
    CONNECTION: "Connection has been established successfully.",
  },
};
