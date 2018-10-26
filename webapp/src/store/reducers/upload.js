import uploadActions from './../actionTypes/upload'

const initialState = {
    pending: false,
    file: null
}

export default function uploadReducer(state = initialState, action) {
    switch(action.type) {
        case uploadActions.UPLOAD:
            return {
                ...state,
                pending: true,
                file: action.file
            }
        case uploadActions.SUCCESS:
            return {
                ...state,
                pending: false
            }
        case uploadActions.FAILURE:
            return {
                ...state,
                pending: false
            }
        default:
            return state;
    }
}