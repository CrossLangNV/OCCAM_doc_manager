import {combineReducers} from "redux";
import DocumentListReducer from "./DocumentListReducer";
import DocumentMultipleReducer from "./DocumentMultipleReducer";
import PageListReducer from "./PageListReducer";

const RootReducer = combineReducers({
    documentList: DocumentListReducer,
    document: DocumentMultipleReducer,
    pageList: PageListReducer,
});

export default RootReducer
