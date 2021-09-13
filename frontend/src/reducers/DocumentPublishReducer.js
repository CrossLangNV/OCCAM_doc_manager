import {DocumentActionTypes} from "../constants/document-action-types";

const DefaultState = {
    loading: false,
    data: {},
    errorMsg: ""
};

const DocumentPublishReducer = (state = DefaultState, action) => {
    switch (action.type) {
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
                errorMsg: "Unable to publish document"
            }
        case DocumentActionTypes.DOCUMENT_PUBLISH_SUCCESS:
            return {
                ...state,
                loading: false,
                errorMsg: "",
                data: action.payload
            }
        default:
            return state
    }
}

export default DocumentPublishReducer
