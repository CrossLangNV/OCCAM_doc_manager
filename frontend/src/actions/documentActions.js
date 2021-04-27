import axios from 'axios'
import {DocumentActionTypes} from "../constants/document-action-types";

export const GetDocumentList = (rows, page, query) => async dispatch => {
    try {

        dispatch({
            type: DocumentActionTypes.DOCUMENT_LIST_LOADING,
            query: query
        });

        const offset = (page * rows) - rows;
        let url = `http://localhost:8000/documents/api/documents?rows=${rows}&offset=${offset}&query=${query}`
        const res = await axios
            .get(url)

        dispatch({
            type: DocumentActionTypes.DOCUMENT_LIST_SUCCESS,
            payload: res.data,
            rows: rows,
            query: query
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

        const res = await axios.get(`http://localhost:8000/documents/api/document/${id}`)

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

export const DeleteDocument = (id) => async dispatch => {
    dispatch({
        type: DocumentActionTypes.DOCUMENT_DELETE_LOADING
    });

    const res = await axios.delete(`http://localhost:8000/documents/api/document/${id}`)
        .then((res) => {
            dispatch({
                type: DocumentActionTypes.DOCUMENT_DELETE_SUCCESS,
                payload: {id}
            })
        })
}

export const ProcessOcrDocument = (id) => async dispatch => {
    dispatch({
        type: DocumentActionTypes.DOCUMENT_OCR_LOADING
    });

    const res = await axios.delete(`http://localhost:8000/documents/api/documents/${id}/ocr`)
        .then((res) => {
            dispatch({
                type: DocumentActionTypes.DOCUMENT_OCR_SUCCESS,
                payload: {id}
            })
        })
}

