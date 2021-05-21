import {ActivityLogsActionTypes} from "../constants/activity-logs-action-types";
import {axiosApi} from "../constants/axiosConf";

// page is the page from the pagination - pageId from the Page object
export const GetActivityList = (rows, page, pageId, overlayId) => async dispatch => {
    try {

        dispatch({
            type: ActivityLogsActionTypes.ACTIVITY_LOGS_LIST_LOADING
        });

        const offset = (page * rows) - rows;
        const res = await axiosApi.get(`/activitylogs/api/activitylogs?rows=${rows}&offset=${offset}&pageId=${pageId}&overlayId=${overlayId}`)

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

