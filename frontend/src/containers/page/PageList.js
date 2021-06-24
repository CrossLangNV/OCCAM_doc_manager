import React, {useEffect, useRef, useState} from 'react';
import {Card} from "primereact/card";
import {Col, Image, Row} from "react-bootstrap";
import {useDispatch, useSelector} from "react-redux";
import {DeletePage, GetPageList, OcrPage, TranslatePage} from "../../actions/pageActions";
import {Button} from "primereact/button";
import {confirmPopup} from "primereact/confirmpopup";
import {Toast} from "primereact/toast";
import OverlayAdd from "../document/OverlayAdd";
import _ from 'lodash'
import PageLeaflet from "./PageLeaflet";
import {ModifySelectedPage} from "../../actions/uiActions";
import {OverlayPanel} from "primereact/overlaypanel";
import {languageSelectItems} from "../../constants/language-selections";
import {Dropdown} from "primereact/dropdown";
import LoadingSpinner from "../core/LoadingSpinner";
import {Dialog} from "primereact/dialog";
import {ScrollPanel} from "primereact/scrollpanel";
import DocumentState from "../document/DocumentState";
import {ContextMenu} from "primereact/contextmenu";
import NotSelectedMessage from "../NotSelectedMessage";
import {useHistory} from "react-router-dom";
import {InputSwitch} from "primereact/inputswitch";


const PageList = (props) => {
    const documentId = props.documentId;
    const dispatch = useDispatch();
    const toast = useRef(null);
    const history = useHistory();

    // Redux states
    const pageList = useSelector(state => state.pageList);
    const uiStates = useSelector(state => state.uiStates);
    const auth = useSelector(state => state.auth);

    // UI Elements
    const [targetLanguage, setTargetLanguage] = useState("");
    const [translationOverlayId, setTranslationOverlayId] = useState("");
    const [translationOverlaySourceLang, setTranslationOverlaySourceLang] = useState("");
    const [contextMenuPage, setContextMenuPage] = useState("");
    const [displayUploadOverlayDialog, setDisplayUploadOverlayDialog] = useState(false);
    const [checkedTM, setCheckedTM] = useState(false);


    const cm = useRef(null);

    // Load pages initially
    useEffect(() => {
        dispatch(GetPageList(100, 1, documentId));
    }, [])

    const translationSelectionOverlay = useRef(null);

    const confirmDeletePage = (event) => {
        confirmPopup({
            target: event.currentTarget,
            message: 'Are you sure you want to delete this page?',
            icon: 'pi pi-exclamation-triangle',
            accept: () => {
                dispatch(DeletePage(event));
                toast.current.show({severity: 'success', summary: 'Success', detail: 'Page has been deleted'});
            },
        });
    }

    const startOcrForPage = (pageId) => {
        dispatch(OcrPage(pageId, auth.user));
        toast.current.show({
            severity: 'success',
            summary: 'Success',
            detail: 'OCR task has been started for the selected page'
        });
        dispatch(GetPageList(100, 1, documentId))
    }

    const startTranslationForPage = (e) => {
        if (translationOverlaySourceLang !== targetLanguage && targetLanguage !== "ORIGINAL") {
            dispatch(TranslatePage(translationOverlayId, targetLanguage, auth.user));
            toast.current.show({
                severity: 'success',
                summary: 'Success',
                detail: 'Translation task has been started for the selected page'
            });
            translationSelectionOverlay.current.hide(e);
            dispatch(GetPageList(100, 1, documentId, checkedTM))
        } else {
            toast.current.show({severity: 'error', summary: 'Failed', detail: 'Target language cannot be the same as the source language'});
        }

    }

    const toggleTranslationMenu = (e, page) => {
        if (!_.isEmpty(page.page_overlay)) {
            const overlay = page.page_overlay[page.page_overlay.length - 1].id

            // Set states so the UI knows which overlay is selected, and which page is selecting for the loading animation
            setTranslationOverlayId(overlay);
            setTranslationOverlaySourceLang(page.page_overlay[page.page_overlay.length - 1].source_lang)

            // Toggle the menu
            translationSelectionOverlay.current.toggle(e);
        } else {
            toast.current.show({severity: 'error', summary: 'Failed', detail: 'Translation is not possible when no overlay is available. Upload an overlay or OCR the page.'});
        }

    }

    const selectPage = async (page) => {
        dispatch(ModifySelectedPage(page))
    }

    const openContextMenu = (e, page) => {
        setContextMenuPage(page)
        cm.current.show(e)
    }

    const downloadOverlay = (e, page) => {
        if (!_.isEmpty(page.page_overlay)) {
            e.preventDefault();
            window.open(page.page_overlay[page.page_overlay.length - 1].file, '_blank');
        } else {
            toast.current.show({severity: 'error', summary: 'Failed', detail: 'No overlay available. Upload an overlay or OCR the page first.'});
        }

    }

    const contextMenuItems = [
        {
            label: 'Start OCR',
            icon: 'pi pi-play',
            command: () => startOcrForPage(contextMenuPage.id)
        },
        {
            label: 'Translate...',
            icon: 'pi pi-globe',
            command: (event) => toggleTranslationMenu(event.originalEvent, contextMenuPage)
        },
        {
            label: 'Upload overlay...',
            icon: 'pi pi-upload',
            command: () => setDisplayUploadOverlayDialog(true)
        },
        {
            label: 'View page overlay',
            icon: 'pi pi-fw pi-file',
            command: (event) => downloadOverlay(event.originalEvent, contextMenuPage)
        },
        {
            label: 'View full-size page',
            icon: 'pi pi-fw pi-file',
            command: () => window.open(contextMenuPage.file, '_blank')
        },
        {
            separator:true
        },
        {
            label: 'Delete page',
            icon: 'pi pi-trash',
            command: () => confirmDeletePage(contextMenuPage.id)
        },
    ]

    return (
        <>
            <h5>Pages ({pageList.count})</h5>
            <br/>
            <Row>
                <Col md={3}>
                    {!_.isEmpty(pageList.data) && (
                        <ScrollPanel className="occ-scrollbar occ-ui-pages-list-scrollable">
                            {pageList.data.map(page => {
                                return <Card key={page.id} className='page-card'>
                                    <Row>
                                        <Col>
                                            <Image
                                                onClick={() => selectPage(page)}
                                                className={uiStates.selectedPage.id === page.id ?
                                                    'page-card-img selectedPage' : 'page-card-img'}
                                                src={page.file}
                                            />
                                            <Button
                                                className="occ-context-menu-button p-button-rounded p-button-secondary"
                                                label=""
                                                icon="pi pi-ellipsis-h"
                                                onClick={(e) => openContextMenu(e, page)}
                                            />
                                            <ContextMenu model={contextMenuItems} ref={cm}/>
                                        </Col>
                                    </Row>

                                    <hr/>

                                    <Row>
                                        <Col>
                                            <Row>
                                                <Col>
                                                    <br/>

                                                    {/* OCR state - OCR task is done on the Page object*/}
                                                    <Row>
                                                        <Col md={5}>
                                                            OCR:
                                                        </Col>

                                                        <Col md="auto">
                                                            <DocumentState state={page.latest_ocr_state.state}/>

                                                            {((page.latest_ocr_state.state === "Processing") &&
                                                                <LoadingSpinner/>
                                                            )}
                                                        </Col>

                                                    </Row>

                                                    {/*Translation state - Translations are done on the Overlay object*/}
                                                    {(!_.isEmpty(page.latest_translation_state) &&
                                                        <Row className="margin-top-lesser">
                                                            <Col md={5}>
                                                                Latest translation:
                                                            </Col>
                                                            <Col md="auto">
                                                                <DocumentState state={page.latest_translation_state[0].state} />

                                                                {((page.latest_translation_state[0].state === "Processing") &&
                                                                    <LoadingSpinner/>
                                                                )}
                                                            </Col>
                                                        </Row>
                                                    )}


                                                </Col>
                                            </Row>
                                        </Col>

                                        {/* Translation Overlay Panel */}
                                        <OverlayPanel ref={translationSelectionOverlay} showCloseIcon id="overlay_panel" style={{width: '450px'}} className="overlaypanel-demo">
                                            <h6>Translate page</h6>
                                            <Row>
                                                <Col md={2}>
                                                    To
                                                </Col>
                                                <Col>
                                                    <Dropdown
                                                        md={7}
                                                        value={targetLanguage}
                                                        options={languageSelectItems}
                                                        onChange={(e) => setTargetLanguage(e.value)}
                                                        placeholder="Select a language"
                                                    />
                                                </Col>

                                            </Row>
                                            <br/>

                                            <Row>
                                                <Col>
                                                    <div className="p-field-checkbox">
                                                        <InputSwitch inputId="useTM" checked={checkedTM} onChange={e => setCheckedTM(e.value)} />
                                                        <label htmlFor="useTM">Use translation memory</label>
                                                    </div>
                                                    Click <a className="occ-link" onClick={() => history.push("/settings")} >here</a> to see translation memory configuration.
                                                </Col>
                                            </Row>
                                            <br/>

                                            <Row>
                                                <Col>
                                                    <Button onClick={(e) => startTranslationForPage(e)}
                                                            label="Translate"
                                                            icon="pi pi-check"
                                                            style={{marginRight: '.25em'}}
                                                            disabled={(targetLanguage.length === 0)}
                                                    />
                                                </Col>

                                            </Row>
                                        </OverlayPanel>
                                    </Row>
                                </Card>
                            })}


                        </ScrollPanel>
                    )}

                    <NotSelectedMessage context={pageList.data} message="No pages are uploaded yet." />

                </Col>

                {!_.isEmpty(pageList.data) && (
                    <Col>

                        {/* Leaflet.js View */}
                        {uiStates.selectedPage !== "" && (
                            <Card className="occ-ui-leaflet-container">
                                <PageLeaflet
                                    key={uiStates.selectedPage.id}
                                    selectedPage={uiStates.selectedPage}
                                />
                            </Card>
                        )}

                        {/* No page selected message */}
                        <NotSelectedMessage context={uiStates.selectedPage} message="No page selected" />

                    </Col>
                )}
            </Row>

            <Dialog visible={displayUploadOverlayDialog} onHide={() => setDisplayUploadOverlayDialog(false)}>
                    <OverlayAdd
                        pageId={contextMenuPage.id}
                        label={!_.isEmpty(contextMenuPage.page_overlay) ? 'Replace overlay' : 'Upload overlay'}
                    />

            </Dialog>

            <Toast ref={toast} />
        </>

    );
};

export default PageList;
