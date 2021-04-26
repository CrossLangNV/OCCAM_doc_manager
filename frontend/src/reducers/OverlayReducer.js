import React from 'react';
import {OverlayActionTypes} from "../constants/overlay-action-types";

const DefaultState = {
    loading: false,
    data: [],
    errorMsg: "",
    count: 0,
    rows: 0,
}

const OverlayListReducer = (state = DefaultState, action) => {
    switch (action.type) {
        case OverlayActionTypes.OVERLAY_LIST_LOADING:
            return {
                ...state,
                loading: true,
                errorMsg: "",
                count: 0,
                rows: 0
            }
        case OverlayActionTypes.OVERLAY_LIST_FAIL:
            return {
                ...state,
                loading: false,
                errorMsg: "Unable to fetch overlay",
                count: 0,
                rows: 0
            }
        case OverlayActionTypes.OVERLAY_LIST_SUCCESS:
            return {
                ...state,
                loading: false,
                data: action.payload.results,
                errorMsg: "",
                count: action.payload.count,
                rows: action.rows

            }
        case OverlayActionTypes.OVERLAY_DELETE_SUCCESS:

            const newState = state.data.filter(overlay =>
                overlay.id !== action.payload.id
            )

            return {
                data: newState,
                loading: false,
                errorMsg: "",
                count: state.count-1,
                rows: state.rows
            }

        case OverlayActionTypes.OVERLAY_ADD_SUCCESS:
            return {
                ...state,
                data: [...state.data, action.payload],
                loading: false,
                errorMsg: "",
                count: state.count+1,
                rows: state.rows
            }
        default:
            return state

    }
};

export default OverlayListReducer;
