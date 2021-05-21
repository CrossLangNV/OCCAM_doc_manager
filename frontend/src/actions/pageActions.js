import {PageActionTypes} from "../constants/page-action-types";
import {axiosApi} from "../constants/axiosConf";

export const GetPageList = (rows, page, doc_id) => async dispatch => {
    try {

        dispatch({
            type: PageActionTypes.PAGE_LIST_LOADING
        });

        const offset = (page * rows) - rows;
        const res = await axiosApi.get(`/documents/api/pages?rows=${rows}&offset=${offset}`,
            {params: {document: doc_id}})

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

        const res = await axiosApi.get(`/documents/api/page/${id}`)

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

        await axiosApi.delete(`/api/page/${id}`)
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

            axiosApi.post(`/documents/api/pages`, formData, {
                headers: {
                    'Content-Type': `multipart/form-data; boundary=${formData._boundary}`,
                }
            }).then((res) => {
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

export const OcrPage = (id) => async dispatch => {
    try {
        dispatch({
            type: PageActionTypes.PAGE_OCR_LOADING
        });

        await axiosApi.post(`/documents/api/pages/launch_ocr`,
            {
                page: id
            })
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

export const TranslatePage = (id, target) => async dispatch => {
    try {
        dispatch({
            type: PageActionTypes.PAGE_TRANSLATION_LOADING
        });

        await axiosApi.post(`/documents/api/pages/translate`,
            {
                overlay: id,
                target: target.toUpperCase()
            })
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
