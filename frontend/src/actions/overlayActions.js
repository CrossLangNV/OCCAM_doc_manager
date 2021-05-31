import {OverlayActionTypes} from "../constants/overlay-action-types";
import axios from "axios";
import {baseUrl} from "../constants/axiosConf";

export const AddOverlay = (pageId, files) => async dispatch => {
    try {
        dispatch({
            type: OverlayActionTypes.OVERLAY_ADD_LOADING
        });

        files.forEach(file => {

            const formData = new FormData();
            formData.append("page", pageId)
            formData.append("file", file)
            formData.append("source_lang", "EN")

            axios.post(`${baseUrl}/documents/api/overlays`, formData, {
                headers: {
                    'Content-Type': `multipart/form-data; boundary=${formData._boundary}`,
                     'Authorization': `Bearer ${localStorage.getItem("access")}`
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
