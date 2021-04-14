import {combineReducers} from "redux";
import DocumentListReducer from "./DocumentListReducer";
import DocumentMultipleReducer from "./DocumentMultipleReducer";

const RootReducer = combineReducers({
    documentList: DocumentListReducer,
    document: DocumentMultipleReducer
});

export default RootReducer
