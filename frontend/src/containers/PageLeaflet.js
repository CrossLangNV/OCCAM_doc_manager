import React, {useRef} from 'react';
import {MapContainer, TileLayer, Marker, Popup, ImageOverlay, useMap} from 'react-leaflet'
import {useSelector} from "react-redux";
import Leaflet from "leaflet";
import {CRS} from "leaflet/dist/leaflet-src.esm";

const PageLeaflet = (props) => {
    const scale = .1; // TODO Change scale later

    const uiStates = useSelector(state => state.uiStates);

    const page = uiStates.selectedPage
    const file = uiStates.selectedPage.file

    const mapRef = useRef(null);

    const hw = (h, w) => {
        if (Leaflet.Util.isArray(h)) {    // When doing xy([x, y]);
            return hw(h[0], h[1]);
        }
        // let height go from top to bottom
        return Leaflet.latLng(-h * scale, w * scale);  // When doing xy(x, y);
    }


    const center = hw([0, 0], null);
    const width = page.image_width;
    const height = page.image_height;

    console.log(width)
    console.log(height)


    const imageBounds = [center, hw(height, width)];

    function ResizeComponent() {
        const map = useMap()
        map.fitBounds(imageBounds)
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

            <ResizeComponent />

        </MapContainer>
    )
};

export default PageLeaflet;
