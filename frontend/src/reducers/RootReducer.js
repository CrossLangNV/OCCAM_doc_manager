import {combineReducers} from "redux";
import DocumentListReducer from "./DocumentListReducer";
import DocumentMultipleReducer from "./DocumentMultipleReducer";
import PageListReducer from "./PageListReducer";
import UiReducer from "./uiReducer";
import ActivityListReducer from "./ActivityLogsListReducer";
import AuthReducer from "./AuthReducer";
import TmStatsReducer from "./TmStatsReducer";

const RootReducer = combineReducers({
    documentList: DocumentListReducer,
    document: DocumentMultipleReducer,
    pageList: PageListReducer,
    uiStates: UiReducer,
    activityLogsList: ActivityListReducer,
    tmStats: TmStatsReducer,
    auth: AuthReducer,
});

export default RootReducer
