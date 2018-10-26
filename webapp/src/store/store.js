import {createStore} from 'redux';
import {combineReducers} from 'redux';
import uploadReducer from './reducers/upload';

const combinedReducers = combineReducers({
    uploadReducer
});
const store = createStore(combinedReducers);

export default store;