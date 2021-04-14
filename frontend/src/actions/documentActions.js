import axios from 'axios'

export const GetDocumentList = (rows, page) => async dispatch => {
    try {

        dispatch({
            type: 'DOCUMENT_LIST_LOADING'
        });

        const offset = (page * rows) - rows;
        const res = await axios.get(`http://localhost:8000/documents/api/documents/?rows=${rows}&offset=${offset}`)

        dispatch({
            type: 'DOCUMENT_LIST_SUCCESS',
            payload: res.data
        });
    } catch (e) {
        dispatch({
            type: 'DOCUMENT_LIST_FAIL'
        });
    }
}

export const GetDocument = (id) => async dispatch => {
    try {

        dispatch({
            type: 'DOCUMENT_MULTIPLE_LOADING'
        });

        const res = await axios.get(`http://localhost:8000/documents/api/documents/${id}`)

        dispatch({
            type: 'DOCUMENT_MULTIPLE_SUCCESS',
            payload: res.data,
            documentId: id
        });
    } catch (e) {
        dispatch({
            type: 'DOCUMENT_MULTIPLE_FAIL'
        });
    }
}
