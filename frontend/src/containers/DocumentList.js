import {useDispatch, useSelector} from "react-redux";
import _ from 'lodash';
import {GetDocumentList} from "../actions/documentActions";
import React from "react";
import {Link} from "react-router-dom";
import {Button, Table} from "react-bootstrap";
import ReactPagiate from "react-paginate"
import {Skeleton} from "primereact/skeleton";

const DocumentList = () => {
    const dispatch = useDispatch();
    const documentList = useSelector(state => state.documentList);

    React.useEffect(() => {
        fetchDocuments(5, 1);
    }, []);

    const fetchDocuments = (rows, page) => {
        dispatch(GetDocumentList(rows, page))
    }

    const loadTableRows = () => {
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
            return <tr>
                <td>{documentList.errorMsg}</td>
            </tr>
        }
    }
    return (
        <div>
            <Button as={Link} to="/document-add">Add new document</Button>
            <br/><br/>

            <Table striped borderless hover>
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
                    {loadTableRows()}
                </tbody>
            </Table>

            {/* Pagination for the table */}
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
