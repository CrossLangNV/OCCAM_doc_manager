import axios from "axios";
import {baseUrl} from "../constants/axiosConf";
import { TmActionTypes } from "../constants/tm-action-types";


export const UploadTMX = (tmx) => async dispatch => {
    try {
        dispatch({
            type: TmActionTypes.TM_TMX_UPLOAD_LOADING
        });

        const formData = new FormData();
        formData.append("tmx", tmx);

        await axios.post(`${baseUrl}/documents/api/tmx/upload`, formData, {
            headers: {
                'Content-Type': `multipart/form-data; boundary=${formData._boundary}`,
            }
        }).then((res) => {
            dispatch({
                type: TmActionTypes.TM_TMX_UPLOAD_SUCCESS,
                payload: res.data
            })
        });
    } catch (e) {
        dispatch({
            type: TmActionTypes.TM_TMX_UPLOAD_FAIL
        });
    }
}

export const GetTmStats = () => async dispatch => {
    try {
        dispatch({
            type: TmActionTypes.TM_STATS_LOADING
        });

        const res = await axios.get(`${baseUrl}/documents/api/tm/stats`)

        dispatch({
            type: TmActionTypes.TM_STATS_SUCCESS,
            payload: res
        });
    } catch (e) {
        dispatch({
            type: TmActionTypes.TM_STATS_FAIL
        });
    }
}