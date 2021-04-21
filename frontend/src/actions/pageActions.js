import axios from 'axios'
import {PageActionTypes} from "../constants/page-action-types";

export const GetPageList = (rows, page, doc_id) => async dispatch => {
    try {

        dispatch({
            type: PageActionTypes.PAGE_LIST_LOADING
        });

        const offset = (page * rows) - rows;
        const res = await axios.get(`http://localhost:8000/documents/api/pages?rows=${rows}&offset=${offset}`,
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

        const res = await axios.get(`http://localhost:8000/documents/api/pages/${id}`)

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
    dispatch({
        type: PageActionTypes.PAGE_DELETE_LOADING
    });

    const res = await axios.delete(`http://localhost:8000/documents/api/pages/${id}`)
        .then((res) => {
            dispatch({
                type: PageActionTypes.PAGE_DELETE_SUCCESS,
                payload: {id}
            })
        })
}
