import {combineReducers} from "redux";
import DocumentListReducer from "./DocumentListReducer";
import DocumentMultipleReducer from "./DocumentMultipleReducer";
import PageListReducer from "./PageListReducer";
import UiReducer from "./uiReducer";
import ActivityListReducer from "./ActivityLogsListReducer";
import AuthReducer from "./AuthReducer";

const RootReducer = combineReducers({
    documentList: DocumentListReducer,
    document: DocumentMultipleReducer,
    pageList: PageListReducer,
    uiStates: UiReducer,
    activityLogsList: ActivityListReducer,
    auth: AuthReducer,
});

export default RootReducer
