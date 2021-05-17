import React, {useRef, useState} from 'react';
import {Card} from "primereact/card";
import {Col, Image, Row} from "react-bootstrap";
import {useDispatch, useSelector} from "react-redux";
import {DeletePage, GetPageList, OcrPage, TranslatePage} from "../actions/pageActions";
import {Button} from "primereact/button";
import {confirmPopup} from "primereact/confirmpopup";
import {Toast} from "primereact/toast";
import OverlayAdd from "./OverlayAdd";
import _ from 'lodash'
import {Skeleton} from "primereact/skeleton";
import PageLeaflet from "./PageLeaflet";
import {ModifySelectedPage} from "../actions/uiActions";
import {OverlayPanel} from "primereact/overlaypanel";
import {languageSelectItems} from "../constants/language-selections";
import {Dropdown} from "primereact/dropdown";


const PageList = (props) => {
    const documentId = props.documentId;
    const dispatch = useDispatch()
    const toast = useRef(null);

    const pageList = useSelector(state => state.pageList);
    const uiStates = useSelector(state => state.uiStates);

    const [targetLanguage, setTargetLanguage] = useState("");
    const [translationOverlayId, setTranslationOverlayId] = useState("");


    const [leafletMarkers, setLeafletMarkers] = useState([])

    React.useEffect(() => {
        dispatch(GetPageList(100, 1, documentId))
    }, [])

    const translationSelectionOverlay = useRef(null);

    const confirmDeletePage = (event) => {
        confirmPopup({
            target: event.currentTarget,
            message: 'Are you sure you want to delete this page?',
            icon: 'pi pi-exclamation-triangle',
            accept: () => {
                dispatch(DeletePage(event))
                toast.current.show({severity: 'success', summary: 'Success', detail: 'Page has been deleted'});
            },
        });
    }

    const startOcrForPage = (pageId) => {
        dispatch(OcrPage(pageId))
        toast.current.show({severity: 'success', summary: 'Success', detail: 'OCR started for page'});
    }

    const startTranslationForPage = () => {
        dispatch(TranslatePage(translationOverlayId, targetLanguage))
        toast.current.show({severity: 'success', summary: 'Success', detail: 'Translation task has been started for the selected page'});
    }

    const toggleTranslationMenu = (e, page) => {
        const overlay = page.page_overlay[page.page_overlay.length - 1].id
        setTranslationOverlayId(overlay)
        translationSelectionOverlay.current.toggle(e)
    }

    const selectPage = async (page) => {
        dispatch(ModifySelectedPage(page))

        // const overlay = page.page_overlay[page.page_overlay.length - 1]
        // const geojson = overlay.overlay_geojson[overlay.overlay_geojson.length -1]

    }

    return (
        <>
            <Row className='scroll-horizontally'>
                {pageList.loading && (
                    <Col>
                        <Skeleton width={'100%'} height={'380px'}></Skeleton>
                    </Col>
                )}

                {pageList.data.map(page => {
                    return <Card key={page.id} className='page-card'>
                        <Row>
                            <Col className="page-container">
                                <Image
                                    onClick={() => selectPage(page)}
                                    className={uiStates.selectedPage.id == page.id ?
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
                        <hr/>
                        <Row>
                            <Col md={7}>
                                <OverlayAdd
                                    pageId={page.id}
                                    label={!_.isEmpty(page.page_overlay) ? 'Replace overlay' : 'Upload overlay'}
                                />
                            </Col>


                            {(!_.isEmpty(page.page_overlay) &&
                                    <Button
                                        className="margin-left"
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

                        </Row>
                        <br/>

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
                                        <Button onClick={() => startTranslationForPage()}
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
