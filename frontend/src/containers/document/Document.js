import {useDispatch, useSelector} from "react-redux";
import {DeleteDocument, GetDocument, GetDocumentList, TranslateAllPages} from "../../actions/documentActions";
import React, {useRef, useState} from "react";
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
import {Dropdown} from "primereact/dropdown";
import {InputSwitch} from "primereact/inputswitch";
import {OverlayPanel} from "primereact/overlaypanel";
import {Toast} from "primereact/toast";

const Document = (props) => {
    const documentId = props.match.params.documentId

    const dispatch = useDispatch()
    let history = useHistory();
    const {t} = useTranslation();

    const toast = useRef(null);
    const translationSelectionOverlay = useRef(null);
    const [targetLanguage, setTargetLanguage] = useState("");
    const [checkedTM, setCheckedTM] = useState(true);


    // Redux states
    const documentState = useSelector(state => state.document)
    const auth = useSelector(state => state.auth);
    const uiStates = useSelector(state => state.uiStates);

    const languageSelectItems = [
        {label: t("translated-languages.english"), value: 'EN'},
        {label: t("translated-languages.dutch"), value: 'NL'},
        {label: t("translated-languages.french"), value: 'FR'},
        {label: t("translated-languages.german"), value: 'DE'},
        {label: t("translated-languages.czech"), value: 'CS'},
    ];


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


    const toggleTranslationMenu = (e) => {
        if (!_.isEmpty(documentState.data[documentId])) {
            const documentData = documentState.data[documentId]
            if (!_.isEmpty(documentData.document_page)) {
                // Toggle the menu
                translationSelectionOverlay.current.toggle(e);
            }
        } else {
            toast.current.show({severity: 'error', summary: t("ui.failed"), detail: t("page-list.Translation is not possible when no overlay is available. Upload an overlay or OCR the page")});
        }

    }


    const startTranslationForAllPages = (e) => {
        if (targetLanguage !== "ORIGINAL") {

            dispatch(TranslateAllPages(documentId, targetLanguage, checkedTM, auth.user));

            toast.current.show({
                severity: 'success',
                summary: t("ui.success"),
                detail: "Started translation for all the pages of your document."
            });

            translationSelectionOverlay.current.hide(e);
            dispatch(GetPageList(100, 1, documentId, checkedTM))
        } else {
            toast.current.show({severity: 'error', summary: t("ui.failed"), detail: t("page-list.Target language cannot be the same as the source language")});
        }

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
                                <>
                                    <Button
                                        onClick={() => confirmStartOcr(documentId)}
                                        label={t("ui.ocr")}
                                        icon="pi pi-play"
                                        className="p-button-primary margin-left"
                                        tooltip={t("document.Starts layout analysis for every page")}
                                        tooltipOptions={{position: 'bottom'}}
                                    />
                                    <Button
                                        onClick={() => toggleTranslationMenu(documentId)}
                                        label={t("page-list.Translate")}
                                        icon="pi pi-globe"
                                        className="p-button-primary margin-left"
                                        tooltip={t("document.Translates all pages to your selected language")}
                                        tooltipOptions={{position: 'bottom'}}
                                    />


                                </>




                            )}

                            <Button
                                onClick={() => confirmDeleteDoc(documentId)}
                                label={t("document.Delete document")}
                                icon="pi pi-trash"
                                className="p-button-danger margin-left"
                            />
                        </Col>
                    </Row>

                    <OverlayPanel ref={translationSelectionOverlay} showCloseIcon id="overlay_panel_translate_all"
                                  className={"occ-translate-all-pages-overlay"}>
                        <h6>{t("ui.Translate all pages")}</h6>
                        <Row>
                            <Col md={2}>
                                {t("page-list.To")}
                            </Col>
                            <Col>
                                <Dropdown
                                    md={7}
                                    value={targetLanguage}
                                    options={languageSelectItems}
                                    onChange={(e) => setTargetLanguage(e.value)}
                                    placeholder={t("page-list.Select a language")}
                                />
                            </Col>

                        </Row>
                        <br/>

                        <Row>
                            <Col>
                                <div className="p-field-checkbox">
                                    <InputSwitch inputId="useTM" checked={checkedTM} onChange={e => setCheckedTM(e.value)} />
                                    <label htmlFor="useTM">{t("page-list.Use translation memory")}</label>
                                </div>
                                {t("page-list.Click")} <a className="occ-link" onClick={() => history.push("/settings")} >{t("page-list.here")}</a> {t("page-list.to see translation memory configuration")}
                            </Col>
                        </Row>
                        <br/>

                        <Row>
                            <Col>
                                <Button onClick={(e) => startTranslationForAllPages(e)}
                                        label="Translate"
                                        icon="pi pi-check"
                                        style={{marginRight: '.25em'}}
                                        disabled={(targetLanguage.length === 0)}
                                />
                            </Col>

                        </Row>
                    </OverlayPanel>

                    <br/>

                        <div>
                            <PageList documentId={documentId} />

                            <br/><br/>
                        </div>
                    <Toast ref={toast} />
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
