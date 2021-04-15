import {useDispatch, useSelector} from "react-redux";
import _ from 'lodash';
import {GetDocumentList} from "../actions/documentActions";
import React from "react";
import {Link} from "react-router-dom";
import {Button, Pagination, Table} from "react-bootstrap";
import ReactPagiate from "react-paginate"

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
        if (documentList.loading) {
            return <p>loading...</p>
        }

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

            {!_.isEmpty(documentList.data) && (
                <ReactPagiate
                    pageCount={Math.ceil(documentList.count / documentList.rows)}
                    pageRangeDisplayed={2}
                    pageMarginDisplayed={1}
                    onPageChange={(data) => fetchDocuments(documentList.rows, data.selected + 1)}
                    containerClassName={"pagination"}
                    activeClassName={'active'}
                    breakClassName={'page-item'}
                />
            )}
        </div>
    )
};

export default DocumentList
