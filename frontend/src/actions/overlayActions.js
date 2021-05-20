import axios from "axios";
import {OverlayActionTypes} from "../constants/overlay-action-types";

export const AddOverlay = (pageId, files) => async dispatch => {
    try {
        dispatch({
            type: OverlayActionTypes.OVERLAY_ADD_LOADING
        });

        files.forEach(file => {

            const formData = new FormData();
            formData.append("page", pageId)
            formData.append("file", file)

            axios.post(`http://localhost:8000/documents/api/overlays`, formData, {
                headers: {
                    'Content-Type': `multipart/form-data; boundary=${formData._boundary}`,
                }
            }).then((res) => {
                dispatch({
                    type: OverlayActionTypes.OVERLAY_ADD_SUCCESS,
                    pageId: pageId,
                    payload: res.data
                })
            });
        });
    } catch (e) {
        dispatch({
            type: OverlayActionTypes.OVERLAY_ADD_FAIL
        });
    }
}
