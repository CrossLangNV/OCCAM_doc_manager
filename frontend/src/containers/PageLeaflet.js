import React, {useRef, useState} from 'react';
import {ImageOverlay, MapContainer, Polygon, Tooltip, useMap} from 'react-leaflet'
import {CRS} from "leaflet/dist/leaflet-src.esm";
import {hw} from "../constants/leafletFunctions";
import {Dropdown} from "primereact/dropdown";
import {Col} from "react-bootstrap";
import axios from "axios";

const PageLeaflet = (props) => {
    const page = props.selectedPage
    const file = page.file
    // const leafletMarkers = props.leafletMarkers

    const [overlay, setOverlay] = useState("");
    const [geojson, setGeojson] = useState("");
    const [language, setLanguage] = useState("");
    const [leafletMarkers, setLeafletMarkers] = useState([])

    React.useEffect(() => {
        if (page.page_overlay.length > 0) {
            const overlay = page.page_overlay[page.page_overlay.length - 1]
            const geojson = overlay.overlay_geojson[overlay.overlay_geojson.length -1]

            setOverlay(overlay)
            setGeojson(geojson)

            if (geojson) {
                setLanguage(overlay.source_lang)
                getLeafletMarkers(geojson)
            }
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

        console.log(features)

    }

    const fetchGeojson = async (file) => {
        return axios.get(file)
    }


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

    // TODO Fix me
    const setPageLanguage = (value) => {
        setLanguage(value)

        let geojsons = overlay.overlay_geojson

        geojsons = geojsons.filter(geojson =>
            geojson.lang.toLowerCase() === value.toLowerCase()
        )
        console.log(geojsons)

        setOverlay(overlay)
        setGeojson(geojsons)

        getLeafletMarkers(geojsons[geojsons.length - 1])
    }

    return (
        <>
            <Col>
                <Dropdown
                    md={7}
                    value={language.toUpperCase()}
                    options={languageSelectItems}
                    onChange={(e) => setPageLanguage(e.value)}
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
