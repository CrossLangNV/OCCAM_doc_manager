import {UiActionTypes} from "../constants/ui-action-types";


const DefaultState = {
    documentQuery: "",
    selectedPage: "",
    layout_engines: [],
    selected_layout_engine: "",
    language: "en",
    showDemoContent: false,
    selectedWebsite: "",
    websites: [],
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
        case UiActionTypes.UI_DOCUMENT_SELECTED_ENGINE_MODIFY:
            return {
                ...state,
                selected_layout_engine: action.payload
            }
        case UiActionTypes.UI_DOCUMENT_LAYOUT_ENGINES_SUCCESS:
            return {
                ...state,
                layout_engines: action.payload,
                selected_layout_engine: action.payload.filter(p => {
                    return p.selected
                })
            }
        case UiActionTypes.UI_LANGUAGE_MODIFY:
            return {
                ...state,
                language: action.payload
            }
        case UiActionTypes.UI_SHOW_DEMO_CONTENT_MODIFY:
            return {
                ...state,
                showDemoContent: action.payload
            }
        case UiActionTypes.UI_WEBSITES_SELECTED_MODIFY:
            return {
                ...state,
                selectedWebsite: action.payload
            }

        case UiActionTypes.UI_WEBSITES_LIST_SUCCESS:
            return {
                ...state,
                websites: action.payload
            }
        default:
            return state
    }
}

export default UiReducer
