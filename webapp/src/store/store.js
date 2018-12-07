import {applyMiddleware, compose, createStore} from 'redux';
import {combineReducers} from 'redux';
import uploadReducer from './reducers/upload';
import authenticationReducer from './reducers/authentication';
import usersReducer from './reducers/users';
// import thunk from 'redux-thunk';
import throttle from 'lodash/throttle';
import {loadState, saveState} from './cookie_store';

const middlewares = [];

const combinedReducers = combineReducers({
    uploadReducer,
    authenticationReducer,
    usersReducer
});

export default function configureStore(initialState) {
  const createdStore = createStore(combinedReducers, initialState,
    compose(applyMiddleware(...middlewares)));
  return createdStore;
}

const store = configureStore(loadState());

store.subscribe(throttle(() => {
  saveState({
    authenticationReducer: store.getState().authenticationReducer
  });
}, 1000));

export {store};