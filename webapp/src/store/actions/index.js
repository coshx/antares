import * as ActionTypes from '../actionTypes/ActionTypes';

export const authenticationAction = (email, password) => ({
  type: ActionTypes.AUTHENTICATE,
  email,
  password
});

export const logoutAction = () => ({
  type: ActionTypes.LOGOUT
});
