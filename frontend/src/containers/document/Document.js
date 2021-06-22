import {useDispatch, useSelector} from "react-redux";
import {DeleteDocument, GetDocument, GetDocumentList} from "../../actions/documentActions";
import React from "react";
import _ from "lodash"
import {Button} from "primereact/button";
import {confirmPopup} from "primereact/confirmpopup";
import {Col, Row} from "react-bootstrap";
import {useHistory} from "react-router-dom";
import Moment from "react-moment";
import PageList from "../page/PageList";
import DocumentState from "./DocumentState";
import {ModifySelectedPage} from "../../actions/uiActions";
import {GetPageList, OcrPage} from "../../actions/pageActions";
import ProgressBar from "../ProgressBar";

const Document = (props) => {
    const documentId = props.match.params.documentId
    const dispatch = useDispatch()
    let history = useHistory();


    // Redux states
    const documentState = useSelector(state => state.document)
    const auth = useSelector(state => state.auth);

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
                dispatch(GetDocumentList(5, 1, ""))
                history.push("/")
            }
        });
    }

    const confirmStartOcr = (event) => {
        confirmPopup({
            target: event.currentTarget,
            message: 'Do you want to start the OCR process for all the pages of this document?',
            icon: 'pi pi-exclamation-triangle',
            accept: () => {
                // Make sure all recently uploaded pages are included
                dispatch(GetPageList(100, 1, documentId))

                if (!_.isEmpty(documentState.data[documentId])) {
                    const documentData = documentState.data[documentId]
                    if (!_.isEmpty(documentData.document_page)) {
                        documentData.document_page.forEach(page => {
                            dispatch(OcrPage(page.id, auth.user))
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
                    <Row className="justify-content-between">
                        <Col md={3}>
                            <h2>{documentData.name}</h2>
                        </Col>
                        <Col md={5}>
                            <ProgressBar activeStep={4} documentId={documentId}/>
                        </Col>
                        <Col md="auto">
                            <Button
                                onClick={() => dispatch(GetPageList(100, 1, documentId))}
                                label="Refresh"
                                icon="pi pi-refresh"
                                className="p-button-primary margin-left"
                            />
                            <Button
                                onClick={() => confirmStartOcr(documentId)}
                                label="OCR all pages"
                                icon="pi pi-play"
                                className="p-button-primary margin-left"
                                tooltip="Starts layout analysis for every page"
                                tooltipOptions={{position: 'bottom'}}
                            />
                            <Button
                                onClick={() => confirmDeleteDoc(documentId)}
                                label="Delete document"
                                icon="pi pi-trash"
                                className="p-button-danger margin-left"
                            />
                        </Col>
                    </Row>

                    <br/>

                        <div>
                            <PageList documentId={documentId} />

                            <br/><br/>
                        </div>
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
