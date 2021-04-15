import {DocumentActionTypes} from "../constants/document-action-types";

const DefaultState = {
    loading: false,
    data: [],
    errorMsg: "",
    count: 0

};

const DocumentListReducer = (state = DefaultState, action) => {
    switch (action.type) {
        case DocumentActionTypes.DOCUMENT_LIST_LOADING:
            return {
                ...state,
                loading: true,
                errorMsg: "",
                count: 0
            }
        case DocumentActionTypes.DOCUMENT_LIST_FAIL:
            return {
                ...state,
                loading: false,
                errorMsg: "Unable to fetch document",
                count: 0
            }
        case DocumentActionTypes.DOCUMENT_LIST_SUCCESS:
            return {
                ...state,
                loading: false,
                data: action.payload.results,
                errorMsg: "",
                count: action.payload.count

            }

        default:
            return state
    }
}

export default DocumentListReducer
