import * as ActionTypes from '../actionTypes/ActionTypes';

export const authenticationAction = (token, username) => ({
  type: ActionTypes.AUTHENTICATE,
  token,
  username
});

export const logoutAction = () => ({
  type: ActionTypes.LOGOUT
});

const handlers = {
    signInUser: {
      begin: ActionTypes.SIGN_IN_USER_BEGIN,
      success: ActionTypes.SIGN_IN_USER_SUCCESS,
      failure: ActionTypes.SIGN_IN_USER_FAILURE
    }
};
  
export function signInUser(email) {
    //TODO: Call API
    //return callAPI(handlers.signInUser, Helpers.signInUser, [email]);
}
  