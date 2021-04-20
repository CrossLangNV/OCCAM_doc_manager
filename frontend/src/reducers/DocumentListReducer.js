import {DocumentActionTypes} from "../constants/document-action-types";

const DefaultState = {
    loading: false,
    data: [],
    errorMsg: "",
    count: 0,
    rows: 0,

};

const DocumentListReducer = (state = DefaultState, action) => {
    switch (action.type) {
        case DocumentActionTypes.DOCUMENT_LIST_LOADING:
            return {
                ...state,
                loading: true,
                errorMsg: "",
                count: 0,
                rows: 0
            }
        case DocumentActionTypes.DOCUMENT_LIST_FAIL:
            return {
                ...state,
                loading: false,
                errorMsg: "Unable to fetch document",
                count: 0,
                rows: 0
            }
        case DocumentActionTypes.DOCUMENT_LIST_SUCCESS:
            return {
                ...state,
                loading: false,
                data: action.payload.results,
                errorMsg: "",
                count: action.payload.count,
                rows: action.rows

            }
        case DocumentActionTypes.DOCUMENT_DELETE_SUCCESS:

            const newState = state.data.filter(document =>
                document.id !== action.payload.id
            )

            return {
                data: newState,
                loading: false,
                errorMsg: "",
                count: state.count-1,
                rows: state.rows
            }
        default:
            return state
    }
}

export default DocumentListReducer
