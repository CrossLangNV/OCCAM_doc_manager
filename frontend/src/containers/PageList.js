import React, {useEffect, useRef, useState} from 'react';
import {Card} from "primereact/card";
import {Col, Image, Row} from "react-bootstrap";
import {useDispatch, useSelector} from "react-redux";
import {DeletePage, GetPageList, OcrPage, TranslatePage} from "../actions/pageActions";
import {Button} from "primereact/button";
import {confirmPopup} from "primereact/confirmpopup";
import {Toast} from "primereact/toast";
import OverlayAdd from "./OverlayAdd";
import _ from 'lodash'
import PageLeaflet from "./PageLeaflet";
import {ModifySelectedPage} from "../actions/uiActions";
import {OverlayPanel} from "primereact/overlaypanel";
import {languageSelectItems} from "../constants/language-selections";
import {Dropdown} from "primereact/dropdown";
import LoadingSpinner from "./LoadingSpinner";
import {Dialog} from "primereact/dialog";
import PageHistory from "./PageHistory";


const PageList = (props) => {
    const documentId = props.documentId;
    const dispatch = useDispatch();
    const toast = useRef(null);

    // Redux states
    const pageList = useSelector(state => state.pageList);
    const uiStates = useSelector(state => state.uiStates);
    const auth = useSelector(state => state.auth);

    // UI Elements
    const [targetLanguage, setTargetLanguage] = useState("");
    const [translationOverlayId, setTranslationOverlayId] = useState("");
    const [displayPageHistory, setDisplayPageHistory] = useState(false);
    const [pageHistoryId, setPageHistoryId] = useState("");

    // Load pages initially
    useEffect(() => {
        dispatch(GetPageList(100, 1, documentId));
    }, [])

    // Refresh the pages every 5 seconds
    // TODO Fix Leaflet zoom is also being reset with this
    // useEffect(() => {
    //     const timer = setTimeout(
    //         () => dispatch(GetPageList(100, 1, documentId)),
    //         5000
    //     );
    //     return () => clearTimeout(timer);
    // })

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
        toast.current.show({severity: 'success', summary: 'Success', detail: 'OCR started for page'});
        dispatch(GetPageList(100, 1, documentId))
    }

    const startTranslationForPage = (e) => {
        dispatch(TranslatePage(translationOverlayId, targetLanguage, auth.user));
        toast.current.show({
            severity: 'success',
            summary: 'Success',
            detail: 'Translation task has been started for the selected page'
        });
        translationSelectionOverlay.current.hide(e);
        dispatch(GetPageList(100, 1, documentId))
    }

    const toggleTranslationMenu = (e, page) => {
        const overlay = page.page_overlay[page.page_overlay.length - 1].id

        // Set states so the UI knows which overlay is selected, and which page is selecting for the loading animation
        setTranslationOverlayId(overlay);

        // Toggle the menu
        translationSelectionOverlay.current.toggle(e);
    }

    const toggleHistoryMenu = (e, page) => {
        setPageHistoryId(page.id)
        // Toggle the menu
        setDisplayPageHistory(true)
    }

    const selectPage = async (page) => {
        dispatch(ModifySelectedPage(page))
    }

    return (
        <>
            <Row className='scroll-horizontally'>

                {pageList.data.map(page => {
                    return <Card key={page.id} className='page-card'>
                        <Row>
                            <Col className="page-container">
                                <Image
                                    onClick={() => selectPage(page)}
                                    className={uiStates.selectedPage.id === page.id ?
                                        'page-card-img selectedPage' : 'page-card-img'}
                                    src={page.file}
                                />
                            </Col>
                        </Row>
                        <Row>
                            <Col>
                                <Button
                                    onClick={() => confirmDeletePage(page.id)}
                                    label=""
                                    icon="pi pi-trash"
                                    className="p-button-danger"
                                    tooltip="Delete page"
                                    tooltipOptions={{position: 'bottom'}}
                                />
                                <Button
                                    className="margin-left"
                                    label=""
                                    icon="pi pi-search-plus"
                                    onClick={(e) => {
                                        e.preventDefault();
                                        window.open(page.file, '_blank');
                                    }}
                                    tooltip="View full size page"
                                    tooltipOptions={{position: 'bottom'}}
                                />
                            </Col>
                        </Row>
                        <br/>

                        <Row className="justify-content-between">
                            <Col md={7}>
                                <OverlayAdd
                                    pageId={page.id}
                                    label={!_.isEmpty(page.page_overlay) ? 'Replace overlay' : 'Upload overlay'}
                                />
                            </Col>
                            <Col md="auto">
                                {(!_.isEmpty(page.page_overlay) &&
                                    <Button
                                        className="margin-right"
                                        label=""
                                        icon="pi pi-eye"
                                        onClick={(e) => {
                                            e.preventDefault();
                                            window.open(page.page_overlay[page.page_overlay.length - 1].file, '_blank');
                                        }}
                                        tooltip="View overlay"
                                        tooltipOptions={{position: 'bottom'}}
                                    />
                                )}
                            </Col>
                        </Row>
                        <hr/>

                        <Row>
                            <Col>
                                <Button
                                    onClick={() => startOcrForPage(page.id)}
                                    label=""
                                    icon="pi pi-play"
                                    className="p-button-primary"
                                    tooltip="Run OCR"
                                    tooltipOptions={{position: 'bottom'}}
                                />
                                {(!_.isEmpty(page.page_overlay) &&
                                    <Button
                                        onClick={(e) => toggleTranslationMenu(e, page)}
                                        label=""
                                        icon="pi pi-globe"
                                        className="p-button-primary margin-left"
                                        tooltip="Translate page"
                                        tooltipOptions={{position: 'bottom'}}
                                    />
                                )}
                                <Button
                                    onClick={(e) => toggleHistoryMenu(e, page)}
                                    label=""
                                    icon="pi pi-info-circle"
                                    className="p-button-primary margin-left"
                                    tooltip="Show history"
                                    tooltipOptions={{position: 'bottom'}}
                                />

                                <Row>
                                    <Col>
                                        <br/>

                                        {/* Translation state - Translations are done on the Overlay object*/}
                                        {(!_.isEmpty(page.latest_overlay_state) &&
                                            <>
                                                Latest translation state: {page.latest_overlay_state[0].state}

                                                {((page.latest_overlay_state[0].state === "Processing") &&
                                                    <LoadingSpinner/>
                                                )}
                                            </>
                                        )}

                                        {/* OCR state - OCR task is done on the Page object*/}
                                        {(!_.isEmpty(page.latest_page_state) &&
                                            <>
                                                <br/>
                                                Latest OCR state: {page.latest_page_state[0].state}

                                                {((page.latest_page_state[0].state === "Processing") &&
                                                    <LoadingSpinner/>
                                                )}
                                            </>
                                        )}
                                    </Col>
                                </Row>
                            </Col>
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
                                        <Button onClick={(e) => startTranslationForPage(e)}
                                                label="Translate"
                                                icon="pi pi-check"
                                                style={{marginRight: '.25em'}}
                                                disabled={(targetLanguage.length === 0)}
                                        />
                                    </Col>

                                </Row>


                            </OverlayPanel>

                            <Dialog header="Page history" visible={displayPageHistory} style={{width: '50vw'}}
                                    onHide={() => setDisplayPageHistory(false)}>
                                <PageHistory pageId={pageHistoryId}/>
                            </Dialog>

                        </Row>
                    </Card>
                })}
                <Toast ref={toast} />


            </Row>

            <div className='space' />

            {uiStates.selectedPage !== "" && (
                <PageLeaflet
                    key={uiStates.selectedPage.id}
                    selectedPage={uiStates.selectedPage}
                    // leafletMarkers={leafletMarkers}
                />
            )}
        </>


    );
};

export default PageList;
