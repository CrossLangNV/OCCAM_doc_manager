import React, {useRef, useState} from 'react';
import {Card} from "primereact/card";
import {Col, Image, Row} from "react-bootstrap";
import {useDispatch, useSelector} from "react-redux";
import {DeletePage, GetPageList, OcrPage} from "../actions/pageActions";
import {Button} from "primereact/button";
import {confirmPopup} from "primereact/confirmpopup";
import {Toast} from "primereact/toast";
import OverlayAdd from "./OverlayAdd";
import _ from 'lodash'
import {Skeleton} from "primereact/skeleton";
import PageLeaflet from "./PageLeaflet";
import {GetLeafletMarkers, ModifySelectedPage} from "../actions/uiActions";
import axios from "axios";
import {hw} from "../constants/leafletFunctions";
import Leaflet from "leaflet";


const PageList = (props) => {
    const documentId = props.documentId;
    const dispatch = useDispatch()
    const toast = useRef(null);

    const pageList = useSelector(state => state.pageList);
    const uiStates = useSelector(state => state.uiStates);
    const [leafletMarkers, setLeafletMarkers] = useState([])

    React.useEffect(() => {
        dispatch(GetPageList(100, 1, documentId))
    }, [])

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

    const selectPage = async (page) => {
        dispatch(ModifySelectedPage(page))

        const overlay = page.page_overlay[page.page_overlay.length - 1]
        const geojson = overlay.geojson

        // dispatch(GetLeafletMarkers(geojson))

        const leafletMarkersArr = []
        const res = await axios.get(geojson).then((res) => {

            for (const c of res.data.features) {
                let marker;

                const bounds = c.geometry.coordinates.map(hw);

                marker = Leaflet.polygon(bounds, {
                    className: 'polygon',
                    weight: 1,
                    color: '#ff7800',
                })

                leafletMarkersArr.push({marker: marker, bounds: bounds})
            }
            setLeafletMarkers(leafletMarkersArr)

        })


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
                                />
                            </Col>


                            {(!_.isEmpty(page.page_overlay) &&
                                <>
                                    <Col>
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

                                    </Col>
                                </>
                            )}

                            <Col>
                                <Button
                                    onClick={() => startOcrForPage(page.id)}
                                    label=""
                                    icon="pi pi-play"
                                    className="p-button-primary"
                                    tooltip="Run OCR"
                                    tooltipOptions={{position: 'bottom'}}
                                />
                            </Col>
                        </Row>
                    </Card>
                })}
                <Toast ref={toast} />


            </Row>

            <div className='space' />

            <Row>
                {uiStates.selectedPage !== "" && (
                    <PageLeaflet selectedPage={uiStates.selectedPage} leafletMarkers={leafletMarkers}/>
                )}
            </Row>
        </>


    );
};

export default PageList;
