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
import Tour from "reactour";
import {ChangeTutorialState, CloseTutorial} from "../../actions/authActions";
import DocumentPreview from "./DocumentPreview";
import {useTranslation} from "react-i18next";


const DocumentList = () => {
    const dispatch = useDispatch();
    let history = useHistory();
    const {t} = useTranslation();

    // Redux states
    const documentList = useSelector(state => state.documentList);
    const uiStates = useSelector(state => state.uiStates);
    const auth = useSelector(state => state.auth)

    React.useEffect(() => {
        fetchDocuments(5, 1, uiStates.documentQuery);
    }, []);

    const fetchDocuments = (rows, page, query) => {
        dispatch(GetDocumentList(rows, page, query))
    }

    const confirmDeleteDoc = (event) => {
        confirmPopup({
            target: event.currentTarget,
            message: t("document-list.Are you sure you want to delete this document and all its pages?"),
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
                            <td className='w-10'>
                                <DocumentPreview document={item} />
                            </td>
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

    const steps = [
        {
            content: () => (
                <div>
                    <h3>Welcome</h3>
                    <p>Let's take a quick tour on how to use the application.</p>
                    <br/>
                    <Button label="Skip product tour" onClick={() => {
                        dispatch(ChangeTutorialState(auth.user, true))
                    }}/>
                </div>

            )
        },
        {
            selector: '.doc-list-step-two',
            content: () => (
                <div>
                    <h3>Document List</h3>
                    <p>This is a table with all your documents.</p>
                    <p>At the first glance, it should look pretty empty...</p>
                    <p>When you created documents, you can always navigate to them by clicking on the titles.</p>
                    <p>The table is paginated, and a search button in the header allows you to search for documents.</p>
                </div>
            )
        },
        {
            selector: '.doc-list-step-three',
            content: () => (
                <div>
                    <h3>Add new document</h3>
                    <p>By pressing this button you can create a new document.</p>
                </div>
            )
        }
    ]

    return (
        <div className="doc-list-step-two">
            <Tour
                steps={steps}
                isOpen={!auth.hasCompletedTutorial}
                onRequestClose={() => dispatch(CloseTutorial())} />


            <Button onClick={() => history.push("/document-add")}
                    label={t("document-list.New document")}
                    icon="pi pi-plus"
                    className="doc-list-step-three"
            />
            <br/>
            <Row className="justify-content-between">
                <Col/>
                <Col md="mr-auto">
                    <p className="occ-table-result-count">{t("document-list.Document(s) found:")} {documentList.count}</p>
                </Col>
            </Row>
            <Table striped borderless hover>
                <thead>
                <tr>
                    <th width="2rem">{t("ui.preview")}</th>
                    <th>{t("ui.title")}</th>
                    <th>{t("ui.state")}</th>
                    <th>{t("ui.created-at")}</th>
                    <th>{t("ui.actions")}</th>
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
