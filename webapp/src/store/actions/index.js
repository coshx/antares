import * as ActionTypes from '../actionTypes/ActionTypes';

export const authenticationAction = (email, token) => ({
  type: ActionTypes.AUTHENTICATE,
  email,
  token,
});

export const logoutAction = () => ({
  type: ActionTypes.LOGOUT,
});
