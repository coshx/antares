import {
  applyMiddleware, compose, createStore, combineReducers,
} from 'redux';
import throttle from 'lodash/throttle';
import uploadReducer from './reducers/upload';
import { authenticationReducer } from './reducers/authentication';
import { usersReducer } from './reducers/users';
// import thunk from 'redux-thunk';
import { loadState, saveState } from './cookie_store';

const middlewares = [];

const combinedReducers = combineReducers({
  uploadReducer,
  authenticationReducer,
  usersReducer,
});

export function configureStore(initialState) {
  const createdStore = createStore(combinedReducers, initialState,
    compose(applyMiddleware(...middlewares)));
  return createdStore;
}

const store = configureStore(loadState());

store.subscribe(throttle(() => {
  saveState({
    authenticationReducer: store.getState().authenticationReducer,
  });
}, 1000));

export { store };
