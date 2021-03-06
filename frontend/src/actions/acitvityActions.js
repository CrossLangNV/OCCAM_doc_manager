import {ActivityLogsActionTypes} from "../constants/activity-logs-action-types";
import axios from "axios";
import {baseUrl} from "../constants/axiosConf";

// page is the page from the pagination - pageId from the Page object
export const GetActivityList = (rows, page, pageId, overlayId, type, onlyLatest) => async dispatch => {
    try {

        const config = {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem("access")}`
            }
        }

        dispatch({
            type: ActivityLogsActionTypes.ACTIVITY_LOGS_LIST_LOADING
        });

        const offset = (page * rows) - rows;
        const res = await axios.get(`${baseUrl}/activitylogs/api/activitylogs?rows=${rows}&offset=${offset}&page=${pageId}&overlay=${overlayId}&type=${type}&onlyLatest=${onlyLatest}`,
            config)

        dispatch({
            type: ActivityLogsActionTypes.ACTIVITY_LOGS_LIST_SUCCESS,
            payload: res.data,
            rows: rows
        });
    } catch (e) {
        dispatch({
            type: ActivityLogsActionTypes.ACTIVITY_LOGS_LIST_FAIL
        });
    }
}

