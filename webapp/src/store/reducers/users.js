import { SIGN_IN_USER_BEGIN, SIGN_IN_USER_SUCCESS, SIGN_IN_USER_FAILURE } from '../actionTypes/ActionTypes';

export const initialState = {
  loading: false,
  error: null,
};

const usersReducer = (state = initialState, action) => {
  switch (action.type) {
    case SIGN_IN_USER_BEGIN:
      return {
        ...state,
        loading: true,
        error: null,
      };

    case SIGN_IN_USER_SUCCESS:
      return {
        ...state,
        loading: false,
      };

    case SIGN_IN_USER_FAILURE:
      return {
        ...state,
        loading: false,
        error: action.payload.error,
      };

    default:
      return state;
  }
};

export { usersReducer };
