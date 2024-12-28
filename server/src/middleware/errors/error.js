const error = (err, req, res, next) => {
  console.error(err.stack);

  const status = err.status || constants.HTTP_STATUS.INTERNAL_SERVER_ERROR;
  const message = err.message || constants.ERROR.SOMETHING_WENT_WRONG;

  res.status(status).send({
    error: {
      message,
      details: err.details || null,
    },
  });
};

export default error;
