// eslint-disable-next-line max-classes-per-file
class UnexpectedResponseStatusError extends Error {
  constructor(response, ...args) {
    super(...args);
    this.response = response;
  }
}
class ConnectionRefusedError extends Error {}
class HTTPConflictError extends Error {} // Occurs on 409 Error

class AuthorizationError extends Error {}

export {
    UnexpectedResponseStatusError,
    ConnectionRefusedError,
    HTTPConflictError,
    AuthorizationError,
};

