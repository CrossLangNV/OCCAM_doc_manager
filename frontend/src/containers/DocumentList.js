import {useDispatch, useSelector} from "react-redux";
import _ from 'lodash';
import {GetDocumentList} from "../actions/documentActions";
import React from "react";
import {Link} from "react-router-dom";
import {Button, Table} from "react-bootstrap";

const DocumentList = () => {
    const dispatch = useDispatch();
    const documentList = useSelector(state => state.documentList);

    React.useEffect(() => {
        fetchDocuments(5, 1);
    }, []);

    const fetchDocuments = (rows, page) => {
        dispatch(GetDocumentList(rows, page))
    }

    const renderDocumentsTable = () => {
        if (!_.isEmpty(documentList.data)) {
            return (
                <>
                    {documentList.data.map(item => {
                        return <tr key={item.id}>
                            <td></td>
                            <td><Link to={`/document/${item.id}`}>{item.name}</Link></td>
                            <td>{item.state}</td>
                            <td>{item.created_at}</td>
                            <td></td>
                        </tr>
                    })}
                </>
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
            <Button as={Link} to="/document-add">Add new document</Button>
            <br/><br/>
            <Table striped bordered hover>
                <thead>
                    <tr>
                        <th width="2rem">Preview</th>
                        <th>Title</th>
                        <th>State</th>
                        <th>Created at</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {renderDocumentsTable()}
                </tbody>
            </Table>


        </div>
    )
}

export default DocumentList
