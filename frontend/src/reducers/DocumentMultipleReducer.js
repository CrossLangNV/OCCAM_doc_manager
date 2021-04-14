const DefaultState = {
    loading: false,
    data: {},
    errorMsg: ""
};

const DocumentMultipleReducer = (state = DefaultState, action) => {
    switch (action.type) {
        case 'DOCUMENT_MULTIPLE_LOADING':
            return {
                ...state,
                loading: true,
                errorMsg: ""
            }
        case 'DOCUMENT_MULTIPLE_FAIL':
            return {
                ...state,
                loading: false,
                errorMsg: "Unable to find document"
            }
        case 'DOCUMENT_MULTIPLE_SUCCESS':
            return {
                ...state,
                loading: false,
                errorMsg: "",
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
