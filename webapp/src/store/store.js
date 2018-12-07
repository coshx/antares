import {createStore} from 'redux';
import {combineReducers} from 'redux';
import uploadReducer from './reducers/upload';
import authenticationReducer from './reducers/authentication';
import usersReducer from './reducers/users';

const combinedReducers = combineReducers({
    uploadReducer,
    authenticationReducer,
    usersReducer
});
const store = createStore(combinedReducers);

export default store;