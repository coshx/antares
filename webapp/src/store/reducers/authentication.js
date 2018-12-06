import { AUTHENTICATE, LOGOUT } from '../actionTypes/ActionTypes';

export const initialAuthenticationState = {};

export const authenticationReducer = (state = initialAuthenticationState, action) => {
  switch (action.type) {
    case AUTHENTICATE:
      return Object.assign({}, state, {
        username: action.username,
        token: action.token
      });
    case LOGOUT:
      return Object.assign({}, state, {
        username: null,
        token: null
      });
    default:
      return state;
  }
}


export default authenticationReducer;