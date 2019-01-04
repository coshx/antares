import * as ActionTypes from '../actionTypes/ActionTypes';

export const authenticationAction = (token) => ({
  type: ActionTypes.AUTHENTICATE,
  token,
});

export const logoutAction = () => ({
  type: ActionTypes.LOGOUT,
});
