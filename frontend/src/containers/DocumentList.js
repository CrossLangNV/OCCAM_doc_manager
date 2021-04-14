import {useDispatch, useSelector} from "react-redux";
import _ from 'lodash';
import {GetDocumentList} from "../actions/documentActions";
import React from "react";
import {Link} from "react-router-dom";

const DocumentList = () => {
    const dispatch = useDispatch();
    const documentList = useSelector(state => state.documentList);

    React.useEffect(() => {
        fetchDocuments(5, 1);
    }, []);

    const fetchDocuments = (rows, page) => {
        dispatch(GetDocumentList(rows, page))
    }

    const showData = () => {
        if (!_.isEmpty(documentList.data)) {
            return (
                <div className={'list-wrapper'}>
                    {documentList.data.map(item => {
                        return <div key={item.id}>
                            <p>{item.name}</p>
                            <p>{item.content}</p>
                            <Link to={`/document/${item.id}`}>View details</Link>
                        </div>
                    })}
                </div>
            )
        }

        if (documentList.loading) {
            return <p>loading...</p>
        }

        if (documentList.errorMsg !== "") {
            return <p> {documentList.errorMsg} </p>
        }

        return <p>Unable to get data</p>
    }
    return (
        <div>
            {showData()}
        </div>
    )
}

export default DocumentList
