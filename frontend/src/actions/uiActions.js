import axios from "axios";
import {OverlayActionTypes} from "../constants/overlay-action-types";
import {UiActionTypes} from "../constants/ui-action-types";

export const ModifyDocumentQuery = (query) => async dispatch => {
    dispatch({
        type: UiActionTypes.UI_DOCUMENT_QUERY_MODIFY,
        payload: query
    });
}

export const ModifySelectedPage = (query) => async dispatch => {
    dispatch({
        type: UiActionTypes.UI_DOCUMENT_SELECTED_PAGE_MODIFY,
        payload: query
    });
}
