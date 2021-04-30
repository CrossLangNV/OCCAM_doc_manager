import axios from "axios";
import {OverlayActionTypes} from "../constants/overlay-action-types";
import {UiActionTypes} from "../constants/ui-action-types";
import {hw} from "../constants/leafletFunctions";
import Leaflet from "leaflet";

export const ModifyDocumentQuery = (query) => async dispatch => {
    dispatch({
        type: UiActionTypes.UI_DOCUMENT_QUERY_MODIFY,
        payload: query
    });
}

export const ModifySelectedPage = (query) => async dispatch => {
    dispatch({
        type: UiActionTypes.UI_DOCUMENT_SELECTED_PAGE_MODIFY,
        payload: query
    });
}


export const GetLeafletMarkers = (geojson) => async dispatch => {
    dispatch({
        type: UiActionTypes.UI_GET_LEAFLET_MARKERS_LOADING
    });

    const leafletMarkers = []

    const res = axios.get(geojson).then((res) => {

        for (const c of res.data.features) {
            let marker;

            const bounds = c.geometry.coordinates.map(hw);

            marker = Leaflet.polygon(bounds, {
                className: 'polygon',
                weight: 1,
                color: '#ff7800',
            })

            leafletMarkers.push({marker: marker, bounds: bounds})
        }

    })


    dispatch({
        type: UiActionTypes.UI_GET_LEAFLET_MARKERS_SUCCESS,
        payload: leafletMarkers
    });
}
