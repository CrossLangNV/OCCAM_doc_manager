import React, {useRef} from 'react';
import {ImageOverlay, MapContainer, Polygon, Tooltip, useMap} from 'react-leaflet'
import Leaflet from "leaflet";
import {CRS} from "leaflet/dist/leaflet-src.esm";
import axios from "axios";
import {hw} from "../constants/leafletFunctions";

const PageLeaflet = (props) => {
    const page = props.selectedPage
    const file = page.file
    const leafletMarkers = props.leafletMarkers

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

    function GetGeoJsonRectangles() {
        const map = useMap()

        const overlay = page.page_overlay[page.page_overlay.length - 1]
        const geojson = overlay.geojson

        axios.get(geojson).then((res) => {

            for (const c of res.data.features) {
                let marker;

                const bounds = c.geometry.coordinates.map(hw);
                // marker = Leaflet.polygon(bounds, {color: '#ff7800', weight: 1}).addTo(map);
                marker = Leaflet.polygon(bounds, {
                    className: 'polygon',
                    weight: 1,
                    color: '#ff7800',
                }).addTo(map);

                marker.bindTooltip(c.properties.name, {
                    // permanent: true,
                    direction: 'bottom'
                });
            }
        })

        return null

    }


    return (
        <MapContainer center={[0, 0]} zoom={3} scrollWheelZoom={false} crs={CRS.Simple}>

            <ImageOverlay
                ref={mapRef}
                url={file}
                bounds={imageBounds}
                opacity={1}
                zIndex={10}
            />

            <ResizeComponent/>

            {/*<GetGeoJsonRectangles/>*/}

            {leafletMarkers.map((marker, id) => {
                return <Polygon key={id} positions={marker.bounds}>
                    <Tooltip sticky>{marker.popupMessage}</Tooltip>
                </Polygon>
            })}
        </MapContainer>
    )
};

export default PageLeaflet;
