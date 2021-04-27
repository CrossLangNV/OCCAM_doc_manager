import {combineReducers} from "redux";
import DocumentListReducer from "./DocumentListReducer";
import DocumentMultipleReducer from "./DocumentMultipleReducer";
import PageListReducer from "./PageListReducer";
import UiReducer from "./uiReducer";

const RootReducer = combineReducers({
    documentList: DocumentListReducer,
    document: DocumentMultipleReducer,
    pageList: PageListReducer,
    uiStates: UiReducer,
    // overlayList: OverlayListReducer,
});

export default RootReducer
