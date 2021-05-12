import React, {useRef, useState} from 'react';
import {ImageOverlay, MapContainer, Polygon, Tooltip, useMap} from 'react-leaflet'
import {CRS} from "leaflet/dist/leaflet-src.esm";
import {hw} from "../constants/leafletFunctions";
import {Dropdown} from "primereact/dropdown";
import {Col} from "react-bootstrap";
import _ from 'lodash'

const PageLeaflet = (props) => {
    const page = props.selectedPage
    const file = page.file
    const leafletMarkers = props.leafletMarkers

    const [overlay, setOverlay] = useState("");
    const [geojson, setGeojson] = useState("");
    const [language, setLanguage] = useState("");

    React.useEffect(() => {
        if (!_.isEmpty(page.page_overlay.length)) {
            const overlay = page.page_overlay[page.page_overlay.length - 1]
            const geojson = overlay.overlay_geojson[overlay.overlay_geojson.length -1]

            setOverlay(overlay)
            setGeojson(geojson)
            if (geojson) {
                setLanguage(geojson.lang)
            }
        }
    }, [])


    // Calculate center and image bounds
    const mapRef = useRef(null);
    const center = hw([0, 0], null);
    const width = page.image_width;
    const height = page.image_height;
    const imageBounds = [center, hw(height, width)];

    const languageSelectItems = [
        {label: 'English', value: 'EN'},
        {label: 'Dutch', value: 'NL'},
        {label: 'French', value: 'FR'},
        {label: 'German', value: 'DE'},
        {label: 'Czech', value: 'CZ'},
    ];


    // Resize the map to fit with the image
    function ResizeComponent() {
        const map = useMap()
        map.fitBounds(imageBounds)
        return null
    }

    return (
        <>
            <Col>
                <Dropdown md={7} value={language} options={languageSelectItems} onChange={(e) => setLanguage(e.value)} placeholder="Select a language"/>
            </Col>

            <MapContainer center={[0, 0]} zoom={3} scrollWheelZoom={true} crs={CRS.Simple}>

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
