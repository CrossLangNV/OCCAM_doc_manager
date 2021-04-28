import React, {useRef} from 'react';
import {MapContainer, TileLayer, Marker, Popup, ImageOverlay, useMap} from 'react-leaflet'
import {useSelector} from "react-redux";
import Leaflet from "leaflet";
import {CRS} from "leaflet/dist/leaflet-src.esm";
import axios from "axios";

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

    function GetGeoJsonRectangles() {
        const map = useMap()


        // const overlay = page.page_overlay[page.page_overlay.length - 1]
        const overlay = page.page_overlay[0]
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
                /*
                Add .openTooltip() to show all tooltips
                OR add {permanent: true} after name.
                https://gis.stackexchange.com/questions/59571/how-to-add-text-only-labels-on-leaflet-map-with-no-icon
                marker.bindTooltip(c.properties.name).openTooltip();
                marker.bindTooltip(c.properties.name);
                */

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

            <ResizeComponent />

            <GetGeoJsonRectangles />

        </MapContainer>
    )
};

export default PageLeaflet;
