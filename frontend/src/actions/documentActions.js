import {DocumentActionTypes} from "../constants/document-action-types";
import {axiosApi} from "../constants/axiosConf";

export const GetDocumentList = (rows, page, query) => async dispatch => {
    try {

        dispatch({
            type: DocumentActionTypes.DOCUMENT_LIST_LOADING,
            query: query
        });

        const offset = (page * rows) - rows;
        let url = `/documents/api/documents?rows=${rows}&offset=${offset}&query=${query}`
        const res = await axiosApi
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

        const res = await axiosApi.get(`/documents/api/document/${id}`)

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
    try {
        dispatch({
            type: DocumentActionTypes.DOCUMENT_DELETE_LOADING
        });

        await axiosApi.delete(`/documents/api/document/${id}`)
            .then((res) => {
                dispatch({
                    type: DocumentActionTypes.DOCUMENT_DELETE_SUCCESS,
                    payload: {id}
                })
            })
    } catch (e) {
        dispatch({
            type: DocumentActionTypes.DOCUMENT_DELETE_FAIL
        });
    }

}

export const ProcessOcrDocument = (id) => async dispatch => {
    try {
        dispatch({
            type: DocumentActionTypes.DOCUMENT_OCR_LOADING
        });

        await axiosApi.delete(`documents/api/documents/${id}/ocr`)
            .then((res) => {
                dispatch({
                    type: DocumentActionTypes.DOCUMENT_OCR_SUCCESS,
                    payload: {id}
                })
            })
    } catch (e) {
        dispatch({
            type: DocumentActionTypes.DOCUMENT_OCR_FAIL
        });
    }
}

