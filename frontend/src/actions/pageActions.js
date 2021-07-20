import {PageActionTypes} from "../constants/page-action-types";
import axios from "axios";
import {baseUrl} from "../constants/axiosConf";

export const GetPageList = (rows, page, doc_id) => async dispatch => {
    try {

        dispatch({
            type: PageActionTypes.PAGE_LIST_LOADING
        });

        const config = {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem("access")}`
            },
            params: {document: doc_id}
        }

        const offset = (page * rows) - rows;
        const res = await axios.get(`${baseUrl}/documents/api/pages?rows=${rows}&offset=${offset}`,
            config)

        dispatch({
            type: PageActionTypes.PAGE_LIST_SUCCESS,
            payload: res.data,
            rows: rows
        });
    } catch (e) {
        dispatch({
            type: PageActionTypes.PAGE_LIST_FAIL
        });
    }
}

export const GetPage = (id) => async dispatch => {
    try {

        dispatch({
            type: PageActionTypes.PAGE_MULTIPLE_LOADING
        });

        const config = {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem("access")}`
            }
        }

        const res = await axios.get(`${baseUrl}/documents/api/page/${id}`, config)

        dispatch({
            type: PageActionTypes.PAGE_MULTIPLE_SUCCESS,
            payload: res.data,
            pageId: id
        });
    } catch (e) {
        dispatch({
            type: PageActionTypes.PAGE_MULTIPLE_FAIL
        });
    }
}

export const DeletePage = (id) => async dispatch => {
    try {
        dispatch({
            type: PageActionTypes.PAGE_DELETE_LOADING
        });

        const config = {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem("access")}`
            }
        }

        await axios.delete(`${baseUrl}/documents/api/page/${id}`, config)
            .then((res) => {
                dispatch({
                    type: PageActionTypes.PAGE_DELETE_SUCCESS,
                    payload: {id}
                })
            })
    } catch (e) {
        dispatch({
            type: PageActionTypes.PAGE_DELETE_FAIL
        });
    }
}

export const AddPage = (documentId, files) => async dispatch => {
    try {
        dispatch({
            type: PageActionTypes.PAGE_ADD_LOADING
        });

        files.forEach(file => {
            const formData = new FormData();
            formData.append("document", documentId)
            formData.append("file", file)

            const config = {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem("access")}`,
                    'Content-Type': `multipart/form-data; boundary=${formData._boundary}`,
                }
            }

            axios.post(`${baseUrl}/documents/api/pages`, formData, config
            ).then((res) => {
                dispatch({
                    type: PageActionTypes.PAGE_ADD_SUCCESS,
                    payload: res.data
                })
            });
        })
    } catch (e) {
        dispatch({
            type: PageActionTypes.PAGE_ADD_FAIL
        });
    }
}

export const OcrPage = (id, engine_pk, user) => async dispatch => {
    try {
        dispatch({
            type: PageActionTypes.PAGE_OCR_LOADING
        });

        const config = {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem("access")}`
            }
        }

        await axios.post(`${baseUrl}/documents/api/pages/launch_ocr`,
            {
                page: id,
                engine_pk: engine_pk,
                user: user
            }, config)
            .then((res) => {
                dispatch({
                    type: PageActionTypes.PAGE_OCR_SUCCESS,
                    payload: {id}
                })
            })
    } catch (e) {
        dispatch({
            type: PageActionTypes.PAGE_OCR_FAIL
        });
    }
}

export const TranslatePage = (id, target, useTM, user) => async dispatch => {
    try {
        dispatch({
            type: PageActionTypes.PAGE_TRANSLATION_LOADING
        });

        const config = {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem("access")}`
            }
        }

        await axios.post(`${baseUrl}/documents/api/pages/translate`,
            {
                overlay: id,
                target: target.toUpperCase(),
                user: user,
                useTM: useTM
            }, config)
            .then((res) => {
                dispatch({
                    type: PageActionTypes.PAGE_TRANSLATION_SUCCESS,
                    payload: {id}
                })
            })
    } catch (e) {
        dispatch({
            type: PageActionTypes.PAGE_TRANSLATION_FAIL
        });
    }
}

export const UpdatePageState = (pageId) => async dispatch => {
    try {
        dispatch({
            type: PageActionTypes.PAGE_UPDATE_STATE_LOADING
        });

        const config = {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem("access")}`
            }
        }

        const res = await axios.get(`${baseUrl}/activitylogs/api/activitylogs?rows=5&offset=0&page=${pageId}&overlay=&type=&&onlyLatest=false`, config)
            .then((res) => {
                dispatch({
                    type: PageActionTypes.PAGE_UPDATE_STATE_SUCCESS,
                    pageId: pageId,
                    payload: res.data
                });
            })
    } catch (e) {
        dispatch({
            type: PageActionTypes.PAGE_UPDATE_STATE_FAILED,
            errorMsg: e
        });
    }


}
