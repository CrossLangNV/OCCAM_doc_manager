import React, {useRef, useState} from 'react';
import {ImageOverlay, MapContainer, Polygon, Tooltip, useMap} from 'react-leaflet'
import {CRS} from "leaflet/dist/leaflet-src.esm";
import {hw} from "../constants/leafletFunctions";
import {Dropdown} from "primereact/dropdown";
import {Col} from "react-bootstrap";
import axios from "axios";
import {languageSelectItems} from "../constants/language-selections"

const PageLeaflet = (props) => {
    const page = props.selectedPage
    const file = page.file
    // const leafletMarkers = props.leafletMarkers

    const [overlay, setOverlay] = useState("");
    const [language, setLanguage] = useState("ORIGINAL");
    const [leafletMarkers, setLeafletMarkers] = useState([])

    React.useEffect(() => {
        if (page.page_overlay.length > 0) {
            const latestOverlay = page.page_overlay[page.page_overlay.length - 1]

            setOverlay(latestOverlay)

            setPageLanguage(latestOverlay, "ORIGINAL")

            getProcessedLanguages()
        }
    }, [])


    const getLeafletMarkers = (geojson) => {
        const leafletMarkersArr = []

        const features = fetchGeojson(geojson.file).then((res) => {
            for (const c of res.data.features) {
                const bounds = c.geometry.coordinates.map(hw);
                const popupMessage = c.properties.name

                leafletMarkersArr.push({popupMessage: popupMessage, bounds: bounds})
            }
            setLeafletMarkers(leafletMarkersArr)
        })
    }

    // TODO CONTINUE THIS TOMORROW

    const getProcessedLanguages = () => {
        // let geojsons = overlay.overlay_geojson
        //
        // let availableLanguages = new Set()
        //
        // geojsons.forEach(geo => {
        //     availableLanguages.add(geo.lang)
        // })
        //
        // console.log(availableLanguages)

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

    // TODO Fix me
    const setPageLanguage = (overlay, language) => {
        setLanguage(language)

        let geojsons = overlay.overlay_geojson

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

    return (
        <>
            <Col>
                View in language
                <Dropdown
                    md={7}
                    value={language.toUpperCase()}
                    options={languageSelectItems}
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

                {leafletMarkers.map((marker, id) => {
                    return <Polygon
                        key={id}
                        positions={marker.bounds}
                    >
                        <Tooltip sticky>{marker.popupMessage}</Tooltip>
                    </Polygon>
                })}
            </MapContainer>
        </>
    )
}

export default PageLeaflet;
