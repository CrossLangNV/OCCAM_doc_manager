import {useDispatch, useSelector} from "react-redux";
import {DeleteDocument, GetDocument} from "../actions/documentActions";
import React from "react";
import _ from "lodash"
import {Button} from "primereact/button";
import {confirmPopup} from "primereact/confirmpopup";
import {Col, Row} from "react-bootstrap";
import {useHistory} from "react-router-dom";
import Moment from "react-moment";
import PageAdd from "./PageAdd";
import PageList from "./PageList";
import DocumentState from "./DocumentState";
import {ModifySelectedPage} from "../actions/uiActions";
import {GetPageList, OcrPage} from "../actions/pageActions";

const Document = (props) => {
    const documentId = props.match.params.documentId

    const dispatch = useDispatch()
    const documentState = useSelector(state => state.document)

    let history = useHistory();

    React.useEffect(() => {
        dispatch(GetDocument(documentId))
        dispatch(ModifySelectedPage(""))
    }, [])

    const confirmDeleteDoc = (event) => {
        confirmPopup({
            target: event.currentTarget,
            message: 'Are you sure you want to delete this document?',
            icon: 'pi pi-exclamation-triangle',
            accept: () => {
                dispatch(DeleteDocument(event))
                history.push("/")
            },
        });
    }

    const confirmStartOcr = (event) => {
        confirmPopup({
            target: event.currentTarget,
            message: 'Do you want to start the OCR process for all the pages of this document?',
            icon: 'pi pi-exclamation-triangle',
            accept: () => {
                if (!_.isEmpty(documentState.data[documentId])) {
                    const documentData = documentState.data[documentId]
                    if (!_.isEmpty(documentData.document_page)) {
                        documentData.document_page.forEach(page => {
                            dispatch(OcrPage(page.id))
                        })
                        dispatch(GetPageList(100, 1, documentId))
                    }
                }
            },
        });
    }

    const showData = () => {
        if (!_.isEmpty(documentState.data[documentId])) {

            const documentData = documentState.data[documentId]
            return (
                <div>
                    <Row>
                        <Col sm={11}>
                            <h1>{documentData.name}</h1>
                        </Col>
                        <Col>
                            <Button
                                onClick={() => dispatch(GetPageList(100, 1, documentId))}
                                label=""
                                icon="pi pi-refresh"
                                className="p-button-primary margin-left"
                                tooltip="Refresh"
                                tooltipOptions={{position: 'bottom'}}
                            />
                            <Button
                                onClick={() => confirmStartOcr(documentId)}
                                label=""
                                icon="pi pi-play"
                                className="p-button-primary margin-left"
                                tooltip="Run OCR"
                                tooltipOptions={{position: 'bottom'}}
                            />
                            <Button
                                onClick={() => confirmDeleteDoc(documentId)}
                                label=""
                                icon="pi pi-trash"
                                className="p-button-danger margin-left"
                                tooltip="Delete document"
                                tooltipOptions={{position: 'bottom'}}
                            />
                        </Col>
                    </Row>

                    <p>
                        <b>Content: </b> {documentData.content}
                    </p>
                    <p>
                        <b className="margin-right">State:</b>
                        <DocumentState state={documentData.state} />
                    </p>
                    <p>
                        <b>Created at:</b>
                        <Moment format="DD/MM/YYYY H:mm" date={documentData.created_at} />
                    </p>

                    <br/>

                        <div>
                            <h5>Pages</h5>
                            {_.isEmpty(documentData.document_page) && (
                                <p>No pages are uploaded yet.</p>
                            )}

                            <PageList documentId={documentId} />

                            <br/><br/>
                        </div>


                    <h5>Upload pages</h5>
                    <PageAdd documentId={documentId} />

                </div>
            )
        }

        if (documentState.loading) {
            return <p>Loading...</p>
        }

        if (documentState.errorMsg !== "") {
            return <p>{documentState.errorMsg}</p>
        }

        return <p>Error fetching document</p>

    }

    return (
        <div>
            {showData()}
        </div>
    )
}
export default Document
