import { AUTHENTICATE, LOGOUT } from '../actionTypes/ActionTypes';

export const initialAuthenticationState = {};

const authenticationReducer = (state = initialAuthenticationState, action) => {
  switch (action.type) {
    case AUTHENTICATE:
      return Object.assign({}, state, {
        token: action.token,
      });
    case LOGOUT:
      return Object.assign({}, state, {
        token: null,
      });
    default:
      return state;
  }
};


export { authenticationReducer };
