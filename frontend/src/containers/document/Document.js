import {useDispatch, useSelector} from "react-redux";
import {DeleteDocument, GetDocument, GetDocumentList} from "../../actions/documentActions";
import React from "react";
import _ from "lodash"
import {Button} from "primereact/button";
import {confirmPopup} from "primereact/confirmpopup";
import {Col, Row} from "react-bootstrap";
import {useHistory} from "react-router-dom";
import PageList from "../page/PageList";
import {ModifySelectedPage} from "../../actions/uiActions";
import {GetPageList, OcrPage, UpdatePageState} from "../../actions/pageActions";
import ProgressBar from "../ProgressBar";
import {useTranslation} from "react-i18next";

const Document = (props) => {
    const documentId = props.match.params.documentId
    const dispatch = useDispatch()
    let history = useHistory();
    const {t} = useTranslation();

    // Redux states
    const documentState = useSelector(state => state.document)
    const auth = useSelector(state => state.auth);
    const uiStates = useSelector(state => state.uiStates);


    React.useEffect(() => {
        dispatch(GetDocument(documentId))
        dispatch(ModifySelectedPage(""))
    }, [])

    const confirmDeleteDoc = (event) => {
        confirmPopup({
            target: event.currentTarget,
            message: t("document.Are you sure you want to delete this document?"),
            icon: 'pi pi-exclamation-triangle',
            accept: () => {
                dispatch(DeleteDocument(event))
                dispatch(GetDocumentList(5, 1, "", ""))
                history.push("/")
            }
        });
    }

    const confirmStartOcr = (event) => {
        confirmPopup({
            target: event.currentTarget,
            message: t("document.Do you want to start the OCR process for all the pages of this document?"),
            icon: 'pi pi-exclamation-triangle',
            accept: () => {
                // Make sure all recently uploaded pages are included
                dispatch(GetPageList(100, 1, documentId))

                if (!_.isEmpty(documentState.data[documentId])) {
                    const documentData = documentState.data[documentId]
                    if (!_.isEmpty(documentData.document_page)) {
                        documentData.document_page.forEach(page => {
                            dispatch(OcrPage(page.id, documentData.layout_analysis_model, auth.user))
                            dispatch(UpdatePageState(page.id))
                            dispatch(GetPageList(100, 1, documentId))
                        })

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
                        <Col md="auto" className="justify-content-between document-step-one">
                            <Button
                                onClick={() => dispatch(GetPageList(100, 1, documentId))}
                                label={t("ui.refresh")}
                                icon="pi pi-refresh"
                                className="p-button-primary margin-left"
                            />
                            {/* 100 is the id of "NO OCR"*/}
                            {(documentData.layout_analysis_model !== 100 && documentData.document_page.length > 0) && (
                                <Button
                                    onClick={() => confirmStartOcr(documentId)}
                                    label={t("document.OCR all pages")}
                                    icon="pi pi-play"
                                    className="p-button-primary margin-left"
                                    tooltip={t("document.Starts layout analysis for every page")}
                                    tooltipOptions={{position: 'bottom'}}
                                />
                            )}

                            <Button
                                onClick={() => confirmDeleteDoc(documentId)}
                                label={t("document.Delete document")}
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
            return <p>{t("ui.loading")}...</p>
        }

        if (documentState.errorMsg !== "") {
            return <p>{documentState.errorMsg}</p>
        }

        return <p>{t("document.Error fetching document")}</p>

    }

    return (
        <div>
            {showData()}
        </div>
    )
}
export default Document
