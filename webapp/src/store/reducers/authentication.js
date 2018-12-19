import { AUTHENTICATE, LOGOUT } from '../actionTypes/ActionTypes';

export const initialAuthenticationState = {};

const authenticationReducer = (state = initialAuthenticationState, action) => {
  switch (action.type) {
    case AUTHENTICATE:
      return Object.assign({}, state, {
        email: action.email,
        password: action.password,
      });
    case LOGOUT:
      return Object.assign({}, state, {
        email: null,
        password: null,
      });
    default:
      return state;
  }
};


export { authenticationReducer };
