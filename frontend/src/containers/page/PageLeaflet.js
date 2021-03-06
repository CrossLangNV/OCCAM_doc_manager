import React, {useRef, useState} from 'react';
import {ImageOverlay, MapContainer, Polygon, Tooltip, useMap} from 'react-leaflet'
import {CRS} from "leaflet/dist/leaflet-src.esm";
import {hw} from "../../constants/leafletFunctions";
import {Col, Row} from "react-bootstrap";
import axios from "axios";
import _ from 'lodash';
import {TabMenu} from "primereact/tabmenu";
import PageMetadata from "./PageMetadata";
import PageHistory from "./PageHistory";
import PagePlainText from "./PagePlainText";
import Tour from "reactour";
import {useDispatch, useSelector} from "react-redux";
import {ChangeTutorialState, CloseTutorial, load_user} from "../../actions/authActions";
import {Button} from "primereact/button";
import {useTranslation} from "react-i18next";

const PageLeaflet = (props) => {
    const page = props.selectedPage
    const file = page.file

    // UI Elements
    const [overlay, setOverlay] = useState("");
    const [language, setLanguage] = useState("ORIGINAL");
    const [selectableLanguages, setSelectableLanguages] = useState([]);
    const [leafletMarkers, setLeafletMarkers] = useState([])
    const [activeView, setActiveView] = useState(0);
    const [textViewSidebar, setTextViewSidebar] = useState(false);
    const [activeLanguageIndex, setActiveLanguageIndex] = useState(0);
    const [plainText, setPlainText] = useState("");
    const {t} = useTranslation();

    // Redux
    const auth = useSelector(state => state.auth);
    const dispatch = useDispatch()

    const viewOptions = [
        {label: t("page-leaflet.Page View"), icon: ''},
        {label: t("page-leaflet.Text View"), icon: ''},
        {label: t("page-leaflet.Metadata"), icon: ''},
        {label: t("page-leaflet.History"), icon: ''},
    ];

    const languageSelectItems = [
        {label: t("translated-languages.original"), value: 'ORIGINAL'},
        {label: t("translated-languages.english"), value: 'EN'},
        {label: t("translated-languages.dutch"), value: 'NL'},
        {label: t("translated-languages.french"), value: 'FR'},
        {label: t("translated-languages.german"), value: 'DE'},
        {label: t("translated-languages.czech"), value: 'CS'},
    ];

    React.useEffect(() => {
        dispatch(load_user())
        if (page.page_overlay.length > 0) {
            const latestOverlay = page.page_overlay[page.page_overlay.length - 1]

            setOverlay(latestOverlay)

            setPageLanguage(latestOverlay, "ORIGINAL")
        }
    }, [])


    const getLeafletMarkers = (geojson) => {
        const leafletMarkersArr = []

        fetchGeojson(geojson.file).then((res) => {
            for (const c of res.data.features) {
                const bounds = c.geometry.coordinates.map(hw);
                const popupMessage = c.properties.name

                leafletMarkersArr.push({popupMessage: popupMessage, bounds: bounds})
            }
            setLeafletMarkers(leafletMarkersArr)
        })
    }

    const getPlainText = (geojson) => {
        const textArr = []
        fetchGeojson(geojson.file).then((res) => {
            for (const c of res.data.features) {
                textArr.push(c.properties.name)

            }

            const text = textArr.join("\r\n")

            setPlainText(text)

        })
    }

    const getProcessedLanguages = (geojsons) => {
        // Create a Set to make sure duplicate translations of a language are in the list
        let availableLanguagesSet = new Set()

        if (!_.isEmpty(geojsons)) {
            geojsons.forEach(geo => {
                availableLanguagesSet.add(geo.lang.toUpperCase())
            })
        }

        // Make a list from the Set, works easier
        let availableLanguages = [...availableLanguagesSet]

        // Take all the possible languages and filter out the items that are not present
        let result = languageSelectItems.filter(item => availableLanguages.includes(item.value))

        // Make sure the first selection in the UI is "Original"
        result = [{label: 'Original', value: 'ORIGINAL'}, ...result]

        // Store the object for the UI
        setSelectableLanguages(result)
    }

    const fetchGeojson = async (f) => {
        return axios.get(f)
    }


    // Calculate center and image bounds
    const mapRef = useRef(null);
    const center = hw([0, 0], null);
    const width = page.image_width;
    const height = page.image_height;
    const imageBounds = [center, hw(height, width)];


    // Resize the map to fit with the image
    function ResizeComponent() {
        const map = useMap()
        map.fitBounds(imageBounds)
        return null
    }

    const setPageLanguage = (overlay, language) => {
        setLanguage(language)

        let geojsons = overlay.overlay_geojson

        // Get processed languages
        getProcessedLanguages(geojsons)

        if (language === "ORIGINAL") {
            geojsons = geojsons.filter(geojson =>
                geojson.original === true
            )
        } else {
            geojsons = geojsons.filter(geojson =>
                geojson.lang.toUpperCase() === language.toUpperCase()
            )
        }

        setOverlay(overlay)

        // Get the leaflet popup markers
        getLeafletMarkers(geojsons[geojsons.length - 1])

        // Get the plain text
        getPlainText(geojsons[geojsons.length - 1])
    }

    function LeafletMarkers({ leafletMarkers }) {
        const map = useMap();

        return (
            leafletMarkers.map((marker, id) => {
                return <Polygon
                    key={id}
                    positions={marker.bounds}
                    eventHandlers={{
                        click: () => {
                            map.setView(
                                [
                                    marker.bounds[0].lat,
                                    marker.bounds[0].lng
                                ],
                                3
                            );
                        }
                    }}
                >

                    <Tooltip className="occ-leaflet-tooltip" direction="bottom" offset={[0, 20]}
                             opacity={1}>{marker.popupMessage}</Tooltip>
                </Polygon>
            })
        )
    }

    const steps = [
        {
            selector: '.document-step-four',
            content: () => (
                <div>
                    <h3>{t("page-leaflet.Page View")}</h3>
                    <p>{t("page-leaflet.In this interactive view your selected page will be presented")}</p>

                    <p>{t("page-leaflet.When the layout analysis has completed, you can see blue boxes around the text in the page")}</p>
                    <p>
                        {t("page-leaflet.By hovering these boxes, a popup will appear which contains the plain text that has been recognized by the OCR")}
                    </p>
                    <p>{t("page-leaflet.By clicking on these, it will automatically zoom in to your text")}</p>
                    <p>{t("page-leaflet.You can zoom in or out with your scroll wheel, and drag the screen to move in your page")}</p>
                </div>
            )
        },
        {
            selector: '.document-step-five',
            content: () => (
                <div>
                    <h3>{t("page-leaflet.View switch")}</h3>
                    <p>{t("page-leaflet.You can click on the tabs to change the view and see other kinds of information about your page")}</p>
                    <ul>
                        <li>
                            <b>{t("page-leaflet.Page View")}:</b> {t("page-leaflet.interactive view of your page")}
                        </li>
                        <li>
                            <b>{t("page-leaflet.Text View")}</b> {t("page-leaflet.Text view of your page. Only works after layout analysis")}.
                        </li>
                        <li>
                            <b>{t("page-leaflet.Metadata")}: </b> {t("page-leaflet.Metadata of your page from the document classifier")}
                        </li>
                        <li>
                            <b>{t("page-leaflet.History")}: </b> {t("page-leaflet.History of actions done on your page")}
                        </li>
                    </ul>
                </div>
            )
        },
        {
            selector: '.document-step-six',
            content: () => (
                <div>
                    <h3>{t("page-leaflet.Language Switch")}</h3>
                    <p>{t("page-leaflet.Switch between the available languages of your page")}</p>
                    <p>{t("page-leaflet.If the desired language is not present, use the context menu to translate your page")}</p>
                    <br/>
                    <Button label={t("tour.complete")} onClick={() => {
                        dispatch(ChangeTutorialState(auth.user, true))
                    }}/>
                </div>
            )
        },
    ]

    return (
        <>
            <Tour
                steps={steps}
                isOpen={!auth.hasCompletedTutorial}
                onRequestClose={() => dispatch(CloseTutorial())}
            />

            <Row className="justify-content-between">
                <Col md="auto">
                    <TabMenu className="document-step-five" model={viewOptions} activeIndex={activeView}
                             onTabChange={(e) => {
                                 setActiveView(e.index);
                             }}/>
                </Col>

                <Col md="auto" className="margin-bottom">
                    <TabMenu className="document-step-six" model={selectableLanguages} activeIndex={activeLanguageIndex}
                             onTabChange={(e) => {
                                 setActiveLanguageIndex(e.index)
                                 setPageLanguage(overlay, e.value.value);
                             }}/>
                </Col>
            </Row>

            {(activeView === 0 &&

                <Row className="justify-content-between">
                    <Col md={11}/>
                    <Col md={"auto"}>
                        <Button icon={textViewSidebar ? "pi pi-angle-double-right" : "pi pi-angle-double-left"}
                                onClick={() => setTextViewSidebar(!textViewSidebar)}
                                className="p-mr-2 p-button-secondary"/>
                    </Col>
                </Row>
            )}


            {/* Leaflet Page View */}
            {((activeView === 0 && textViewSidebar === false) &&
                <>
                    <MapContainer center={[0, 0]} scrollWheelZoom={true} crs={CRS.Simple}>

                        <ImageOverlay
                            ref={mapRef}
                            url={file}
                            bounds={imageBounds}
                            opacity={1}
                            zIndex={10}
                        />

                        <ResizeComponent/>

                        <LeafletMarkers leafletMarkers={leafletMarkers}/>
                    </MapContainer>
                </>
            )}

            {/* Leaflet Page View SPLIT VIEW */}
            {((activeView === 0 && textViewSidebar === true) &&
                <Row>
                    <Col md={8}>
                        <MapContainer center={[0, 0]} scrollWheelZoom={true} crs={CRS.Simple}>

                            <ImageOverlay
                                ref={mapRef}
                                url={file}
                                bounds={imageBounds}
                                opacity={1}
                                zIndex={10}
                            />

                            <ResizeComponent/>

                            <LeafletMarkers leafletMarkers={leafletMarkers}/>
                        </MapContainer>
                    </Col>

                    <Col md={4}>
                        {/* SIDEBAR: Plain Text View */}
                        {(textViewSidebar &&
                            <div className="occ-plaintext white-space margin-top">
                                <PagePlainText content={plainText}/>
                            </div>
                        )}
                    </Col>

                </Row>
            )}

            {/* Plain Text View */}
            {(activeView === 1 &&
                <div className="occ-plaintext white-space margin-top">
                    <PagePlainText content={plainText}/>
                </div>
            )}

            {/* Metadata View*/}
            {(activeView === 2 &&
                <div className="occ-plaintext white-space margin-top">
                    <PageMetadata page={page}/>
                </div>
            )}

            {/* History View*/}
            {(activeView === 3 &&
                <div className="occ-plaintext white-space margin-top">
                    <PageHistory pageId={page.id}/>
                </div>
            )}
        </>
    )
}

export default PageLeaflet;
