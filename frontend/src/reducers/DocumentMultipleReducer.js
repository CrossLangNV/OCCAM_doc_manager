import {DocumentActionTypes} from "../constants/document-action-types";

const DefaultState = {
    loading: false,
    data: {},
    errorMsg: ""
};

const DocumentMultipleReducer = (state = DefaultState, action) => {
    switch (action.type) {
        case DocumentActionTypes.DOCUMENT_MULTIPLE_LOADING:
            return {
                ...state,
                loading: true,
                errorMsg: ""
            }
        case DocumentActionTypes.DOCUMENT_MULTIPLE_FAIL:
            return {
                ...state,
                loading: false,
                errorMsg: "Unable to find document"
            }
        case DocumentActionTypes.DOCUMENT_MULTIPLE_SUCCESS:
            return {
                ...state,
                loading: false,
                errorMsg: "",
                data: {
                    ...state.data,
                    [action.documentId]: action.payload
                }
            }
        case DocumentActionTypes.DOCUMENT_PUBLISH_LOADING:
            return {
                ...state,
                loading: true,
                errorMsg: ""
            }
        case DocumentActionTypes.DOCUMENT_PUBLISH_FAIL:
            return {
                ...state,
                loading: false,
                errorMsg: action.payload,
            }
        case DocumentActionTypes.DOCUMENT_PUBLISH_SUCCESS:
            return {
                data: {
                    ...state.data,
                    [action.documentId]: action.payload
                }
            }
        default:
            return state
    }
}

export default DocumentMultipleReducer
