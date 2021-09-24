import {DocumentActionTypes} from "../constants/document-action-types";
import axios from "axios";
import {baseUrl} from "../constants/axiosConf";

export const GetDocumentList = (rows, page, query, website) => async dispatch => {
    try {

        const config = {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem("access")}`
            }
        }

        dispatch({
            type: DocumentActionTypes.DOCUMENT_LIST_LOADING,
            query: query
        });

        if (website === undefined) {
            website = ""
        }

        const offset = (page * rows) - rows;
        const res = await axios.get(`${baseUrl}/documents/api/documents?rows=${rows}&offset=${offset}&query=${query}&website=${website}`, config)

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

        const config = {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem("access")}`
            }
        }

        const res = await axios.get(`${baseUrl}/documents/api/document/${id}`, config)

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

        const config = {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem("access")}`
            }
        }

        await axios.delete(`${baseUrl}/documents/api/document/${id}`, config)
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

        const config = {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem("access")}`
            }
        }

        await axios.delete(`${baseUrl}/documents/api/documents/${id}/ocr`, config)
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

export const PublishDocument = (id) => async dispatch => {
    try {
        dispatch({
            type: DocumentActionTypes.DOCUMENT_PUBLISH_LOADING
        });

        const config = {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem("access")}`
            }
        }

        await axios.post(`${baseUrl}/documents/api/publish?document=${id}`, {document: id}, config)
            .then((res) => {
                dispatch({
                    type: DocumentActionTypes.DOCUMENT_PUBLISH_SUCCESS,
                    documentId: id,
                    payload: res.data
                });
                console.log("res: ", res)
                console.log("res.data: ", res.data)
            })
    } catch (e) {
        console.log(e)
        dispatch({
            type: DocumentActionTypes.DOCUMENT_PUBLISH_FAIL,
            payload: e
        });
    }
}

export const TranslateAllPages = (documentId, targetLanguage, useTM, user) => async dispatch => {
    try {
        dispatch({
            type: DocumentActionTypes.DOCUMENT_TRANSLATE_ALL_PAGES_LOADING
        });

        const config = {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem("access")}`
            }
        }

        await axios.post(`${baseUrl}/documents/api/translate_all`,
            {documentId, targetLanguage, useTM, user},
            config)
            .then((res) => {
                dispatch({
                    type: DocumentActionTypes.DOCUMENT_TRANSLATE_ALL_PAGES_SUCCESS,
                    payload: res.data
                });
            })
    } catch (e) {
        console.log(e)
        dispatch({
            type: DocumentActionTypes.DOCUMENT_TRANSLATE_ALL_PAGES_FAIL,
            payload: e
        });
    }
}
