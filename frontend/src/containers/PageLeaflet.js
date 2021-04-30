import React, {useRef} from 'react';
import {ImageOverlay, MapContainer, Polygon, Tooltip, useMap} from 'react-leaflet'
import {CRS} from "leaflet/dist/leaflet-src.esm";
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

    return (
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
                return <Polygon key={id} positions={marker.bounds}>
                    <Tooltip sticky>{marker.popupMessage}</Tooltip>
                </Polygon>
            })}
        </MapContainer>
    )
};

export default PageLeaflet;
