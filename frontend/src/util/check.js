import { UnexpectedResponseStatusError } from '@/util/error';

const throwUnexpectedResponseError = async (expectedStatus, response) => {
  let message = '';
  try {
    const body = await response.json();
    message = body.message || body.error.message;
  } catch (error) {
    message = `Expected status "${expectedStatus}", but got "${response.status} ${response.statusText}"`;
  }
  throw new UnexpectedResponseStatusError(response, message);
};

const checkResponseStatus = async (expectedStatus, response) => {
  if (response.status !== expectedStatus) {
    await throwUnexpectedResponseError(expectedStatus, response);
    return false;
  }
  return true;
};

export { checkResponseStatus };
