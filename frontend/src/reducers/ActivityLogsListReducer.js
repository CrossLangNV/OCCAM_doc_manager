import {ActivityLogsActionTypes} from "../constants/activity-logs-action-types";

const DefaultState = {
    loading: false,
    data: [],
    errorMsg: "",
    count: 0,
    rows: 0,
};

const ActivityListReducer = (state = DefaultState, action) => {
    switch (action.type) {
        case ActivityLogsActionTypes.ACTIVITY_LOGS_LIST_LOADING:
            return {
                ...state,
                loading: true,
                errorMsg: "",
                count: 0,
                rows: 0
            }
        case ActivityLogsActionTypes.ACTIVITY_LOGS_LIST_FAIL:
            return {
                ...state,
                loading: false,
                errorMsg: "Unable to fetch activity logs",
                count: 0,
                rows: 0
            }
        case ActivityLogsActionTypes.ACTIVITY_LOGS_LIST_SUCCESS:
            return {
                ...state,
                loading: false,
                data: action.payload.results,
                errorMsg: "",
                count: action.payload.count,
                rows: action.rows
            }
        default:
            return state
    }
}

export default ActivityListReducer
