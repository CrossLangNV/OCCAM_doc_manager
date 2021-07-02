import React, {useRef, useState} from 'react';
import {ImageOverlay, MapContainer, Polygon, Tooltip, useMap} from 'react-leaflet'
import {CRS} from "leaflet/dist/leaflet-src.esm";
import {hw} from "../../constants/leafletFunctions";
import {Col, Row} from "react-bootstrap";
import axios from "axios";
import {languageSelectItems} from "../../constants/language-selections"
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

                    <Tooltip className="occ-leaflet-tooltip" sticky>{marker.popupMessage}</Tooltip>
                </Polygon>
            })
        )
    }

    const steps = [
        {
            selector: '.document-step-four',
            content: () => (
                <div>
                    <h3>Page View</h3>
                    <p>In this interactive view your selected page will be presented.</p>

                    <p>When the layout analysis has completed, you can see blue boxes around the text in the page.</p>
                    <p>By hovering these boxes, a popup will appear which contains the plain text that has been
                        recognized by the OCR. </p>
                    <p>By clicking on these, it will automatically zoom in to your text. </p>
                    <p>You can zoom in or out with your scroll wheel, and drag the screen to move in your page. </p>
                </div>
            )
        },
        {
            selector: '.document-step-five',
            content: () => (
                <div>
                    <h3>View switch</h3>
                    <p>You can click on the tabs to change the view and see other kinds of information about your
                        page.</p>
                    <ul>
                        <li>
                            <b>Page View:</b> interactive view of your page.
                        </li>
                        <li>
                            <b>Text View: </b> Text view of your page. Only works after layout analysis.
                        </li>
                        <li>
                            <b>Metadata: </b> Metadata of your page from the document classifier.
                        </li>
                        <li>
                            <b>History: </b> History of actions done on your page.
                        </li>
                    </ul>
                </div>
            )
        },
        {
            selector: '.document-step-six',
            content: () => (
                <div>
                    <h3>Language Switch</h3>
                    <p>Switch between the available languages of your page. </p>
                    <p>If the desired language is not present, use the context menu to translate your page. </p>
                    <br/>
                    <Button label="Don't show me again" onClick={() => {
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
                <Col md={4}>
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

            {/* Leaflet Page View */}
            {(activeView === 0 &&

                <MapContainer center={[0, 0]} scrollWheelZoom={true} crs={CRS.Simple}>

                    <ImageOverlay
                        ref={mapRef}
                        url={file}
                        bounds={imageBounds}
                        opacity={1}
                        zIndex={10}
                    />

                    <ResizeComponent/>

                    <LeafletMarkers leafletMarkers={leafletMarkers} />

                </MapContainer>
            )}

            {/* Plain Text View */}
            {(activeView === 1 &&
                <div className="occ-plaintext white-space margin-top">
                    <PagePlainText content={plainText} />
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
