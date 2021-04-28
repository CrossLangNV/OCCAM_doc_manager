import React from 'react';
import {MapContainer, TileLayer, Marker, Popup, ImageOverlay} from 'react-leaflet'
import {useSelector} from "react-redux";

const PageLeaflet = (props) => {

    const position = [51.505, -0.09]

    // const page = props.page
    // const file = props.file



    const uiStates = useSelector(state => state.uiStates);

    const page = uiStates.selectedPage
    const file = uiStates.selectedPage.file


    console.log(page)
    console.log(file)

    return (
        // <MapContainer center={[0, 0]} zoom={13}>
        //
        // </MapContainer>
        <MapContainer center={[70, 50]} zoom={3} scrollWheelZoom={false}>
            <Marker position={[100, -0.09]}>
                <Popup>
                    A pretty CSS3 popup. <br /> Easily customizable.
                </Popup>
            </Marker>
            <ImageOverlay
                    url={file}
                    bounds={[
                        [100, 0],
                        [-35, 100],
                    ]}
                    opacity={1}
                    zIndex={10}
                />
        </MapContainer>
    );
};

export default PageLeaflet;
