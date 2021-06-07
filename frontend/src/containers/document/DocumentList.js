import {useDispatch, useSelector} from "react-redux";
import _ from 'lodash';
import {DeleteDocument, GetDocumentList} from "../../actions/documentActions";
import React from "react";
import {Link, useHistory} from "react-router-dom";
import {Col, Row, Table} from "react-bootstrap";
import ReactPagiate from "react-paginate"
import {Button} from "primereact/button";
import Moment from 'react-moment';
import {confirmPopup} from "primereact/confirmpopup";
import DocumentState from "./DocumentState";


const DocumentList = () => {
    const dispatch = useDispatch();
    const documentList = useSelector(state => state.documentList);
    const uiStates = useSelector(state => state.uiStates);
    let history = useHistory();

    React.useEffect(() => {
        fetchDocuments(5, 1, uiStates.documentQuery);
    }, []);

    const fetchDocuments = (rows, page, query) => {
        dispatch(GetDocumentList(rows, page, query))
    }

    const confirmDeleteDoc = (event) => {
        confirmPopup({
            target: event.currentTarget,
            message: 'Are you sure you want to proceed?',
            icon: 'pi pi-exclamation-triangle',
            accept: () => dispatch(DeleteDocument(event)),
        });
    }

    const loadTableRows = () => {
        if (!_.isEmpty(documentList.data)) {
            return (
                <>
                    {documentList.data.map(item => {
                        return <tr key={item.id}>
                            <td className='w-10'></td>
                            <td className='w-50'><Link to={`/document/${item.id}`}>{item.name}</Link></td>
                            <td>
                                <DocumentState state={item.state} />
                            </td>
                            <td className='w-10'>
                                <Moment format="DD/MM/YYYY H:mm" date={item.created_at} />
                            </td>
                            <td className='w-10'>
                                <Button
                                    onClick={() => confirmDeleteDoc(item.id)}
                                    label=""
                                    icon="pi pi-trash"
                                    className="p-button-danger"
                                />
                            </td>
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
            <Button onClick={() => history.push("/document-add")}
                    label="New document"
                    icon="pi pi-plus"
            />
            <br/>
            <Row className="justify-content-between">
                <Col/>
                <Col md="mr-auto">
                    <p className="occ-table-result-count">Document(s) found: {documentList.count}</p>
                </Col>
            </Row>
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
                    onPageChange={(data) => fetchDocuments(documentList.rows, data.selected + 1, uiStates.documentQuery)}
                    containerClassName={"pagination"}
                    activeClassName={'active'}
                    breakClassName={'page-item'}
                />
            )}
        </div>
    )
};

export default DocumentList
