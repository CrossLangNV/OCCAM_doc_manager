import axios from 'axios'
import {DocumentActionTypes} from "../constants/document-action-types";

export const GetDocumentList = (rows, page) => async dispatch => {
    try {

        dispatch({
            type: DocumentActionTypes.DOCUMENT_LIST_LOADING
        });

        const offset = (page * rows) - rows;
        const res = await axios.get(`http://localhost:8000/documents/api/documents/?rows=${rows}&offset=${offset}`)

        dispatch({
            type: DocumentActionTypes.DOCUMENT_LIST_SUCCESS,
            payload: res.data,
            rows: rows
        });
    } catch (e) {
        dispatch({
            type: DocumentActionTypes.DOCUMENT_LIST_FAIL
        });
    }
}

export const GetDocument = (id) => async dispatch => {
    try {

        dispatch({
            type: DocumentActionTypes.DOCUMENT_MULTIPLE_LOADING
        });

        const res = await axios.get(`http://localhost:8000/documents/api/documents/${id}`)

        dispatch({
            type: DocumentActionTypes.DOCUMENT_MULTIPLE_SUCCESS,
            payload: res.data,
            documentId: id
        });
    } catch (e) {
        dispatch({
            type: DocumentActionTypes.DOCUMENT_MULTIPLE_FAIL
        });
    }
}

export const AddDocument = (title, content) => async dispatch => {
    try {
        dispatch({
            type: DocumentActionTypes.DOCUMENT_ADD_LOADING
        });

        const res = await axios.post(`http://localhost:8000/documents/api/documents/`,
            {
                name: title,
                content: content,
                state: 'New'
            }).then((res) => {
                console.log(res);
        });

        dispatch({
            type: DocumentActionTypes.DOCUMENT_ADD_SUCCESS,
            payload: res.data,
            documentId: res.data.id
        });
    } catch (e) {
        dispatch({
            type: DocumentActionTypes.DOCUMENT_ADD_FAIL
        });
    }
}
