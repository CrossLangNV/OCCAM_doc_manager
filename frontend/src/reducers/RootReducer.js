import {combineReducers} from "redux";
import DocumentListReducer from "./DocumentListReducer";
import DocumentMultipleReducer from "./DocumentMultipleReducer";
import PageListReducer from "./PageListReducer";
import OverlayListReducer from "./OverlayReducer";

const RootReducer = combineReducers({
    documentList: DocumentListReducer,
    document: DocumentMultipleReducer,
    pageList: PageListReducer,
    overlayList: OverlayListReducer,
});

export default RootReducer
