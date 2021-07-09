import { TmActionTypes } from "../constants/tm-action-types";


const DefaultState = {
    loading: false,
    data: [],
    errorMsg: "",
};

const TmStatsReducer = (state = DefaultState, action) => {
    switch (action.type) {
        case TmActionTypes.TM_STATS_LOADING:
            return {
                ...state,
                loading: true,
                errorMsg: ""
            }
        case TmActionTypes.TM_STATS_FAIL:
            return {
                ...state,
                loading: false,
                errorMsg: "Unable to fetch TM stats"
            }
        case TmActionTypes.TM_STATS_SUCCESS:
            return {
                ...state,
                loading: false,
                data: action.payload.data,
                errorMsg: ""
            }
        default:
            return state
    }
}

export default TmStatsReducer
