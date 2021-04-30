import {UiActionTypes} from "../constants/ui-action-types";


const DefaultState = {
    documentQuery: "",
    selectedPage: ""
};

const UiReducer = (state = DefaultState, action) => {
    switch (action.type) {
        case UiActionTypes.UI_DOCUMENT_QUERY_MODIFY:
            return {
                ...state,
                documentQuery: action.payload
            }
        case UiActionTypes.UI_DOCUMENT_SELECTED_PAGE_MODIFY:
            return {
                ...state,
                selectedPage: action.payload
            }
        default:
            return state
    }
}

export default UiReducer
