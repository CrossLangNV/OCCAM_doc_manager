import React, {useRef, useState} from 'react';
import {ImageOverlay, MapContainer, Polygon, Tooltip, useMap, useMapEvent, useMapEvents} from 'react-leaflet'
import {CRS} from "leaflet/dist/leaflet-src.esm";
import {hw} from "../constants/leafletFunctions";
import {Dropdown} from "primereact/dropdown";
import {Col} from "react-bootstrap";
import axios from "axios";
import {languageSelectItems} from "../constants/language-selections"
import _ from 'lodash';

const PageLeaflet = (props) => {
    const page = props.selectedPage
    const file = page.file

    const [overlay, setOverlay] = useState("");
    const [language, setLanguage] = useState("ORIGINAL");
    const [selectableLanguages, setSelectableLanguages] = useState([]);
    const [leafletMarkers, setLeafletMarkers] = useState([])

    React.useEffect(() => {
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

        getLeafletMarkers(geojsons[geojsons.length - 1])
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


    return (
        <>
            <Col>
                View in language
                <Dropdown
                    md={7}
                    value={language.toUpperCase()}
                    options={selectableLanguages}
                    onChange={(e) => setPageLanguage(overlay, e.value)}
                    placeholder="Select a language"
                />
            </Col>

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
        </>
    )
}

export default PageLeaflet;
