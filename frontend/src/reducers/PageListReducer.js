import {PageActionTypes} from "../constants/page-action-types";
import {OverlayActionTypes} from "../constants/overlay-action-types";

const DefaultState = {
    loading: false,
    data: [],
    errorMsg: "",
    count: 0,
    rows: 0,
}

const PageListReducer = (state = DefaultState, action) => {
    switch (action.type) {
        case PageActionTypes.PAGE_LIST_LOADING:
            return {
                ...state,
                loading: true,
                errorMsg: "",
                count: 0,
                rows: 0
            }
        case PageActionTypes.PAGE_LIST_FAIL:
            return {
                ...state,
                loading: false,
                errorMsg: "Unable to fetch page",
                count: 0,
                rows: 0
            }
        case PageActionTypes.PAGE_LIST_SUCCESS:
            return {
                ...state,
                loading: false,
                data: action.payload.results,
                errorMsg: "",
                count: action.payload.count,
                rows: action.rows

            }
        case PageActionTypes.PAGE_DELETE_SUCCESS:

            const newState = state.data.filter(page =>
                page.id !== action.payload.id
            )

            return {
                data: newState,
                loading: false,
                errorMsg: "",
                count: state.count-1,
                rows: state.rows
            }

        case PageActionTypes.PAGE_ADD_SUCCESS:
            return {
                ...state,
                data: [...state.data, action.payload],
                loading: false,
                errorMsg: "",
                count: state.count+1,
                rows: state.rows
            }

        case OverlayActionTypes.OVERLAY_ADD_SUCCESS:

            return {
                ...state,
                data: state.data.map(
                    (page, i) => page.id === action.pageId ? {...page, page_overlay: [action.payload]}
                        : page
                ),
                loading: false,
                errorMsg: "",
                count: state.count,
                rows: state.rows
            }

        default:
            return state

    }
};

export default PageListReducer;
