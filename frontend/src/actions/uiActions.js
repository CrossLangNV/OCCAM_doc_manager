import {UiActionTypes} from "../constants/ui-action-types";
import axios from "axios";
import {baseUrl} from "../constants/axiosConf";
import _ from "lodash";

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

export const ModifySelectedEngine = (engine) => async dispatch => {
    dispatch({
        type: UiActionTypes.UI_DOCUMENT_SELECTED_ENGINE_MODIFY,
        payload: engine
    });
}



export const GetLayoutEngines = (documentId) => async dispatch => {

    try {
        dispatch({
            type: UiActionTypes.UI_DOCUMENT_LAYOUT_ENGINES_LOADING,
        })

        const config = {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem("access")}`
            }
        }

        // Get available models/engines
        let models = []
        const res = await axios.get(`${baseUrl}/documents/api/layout_analysis_models`, config)

        res.data.forEach(model => {
            models.push({name: model.name, value: model.description, id: model.id, selected: false})
        })
        // models.push({name: 'None', value: 'None'})

        // Get current selected model if present
        if (documentId !== undefined) {
            await axios.get(`${baseUrl}/documents/api/document/${documentId}`, config).then((res) => {

                models.forEach((opt) => {
                    if (opt.id === res.data.layout_analysis_model) {

                        const index = _.findIndex(models, {id: opt.id})
                        models[index].selected = true
                    }
                })

            }).catch((err => {
                console.log(err)
            }))
        }


        dispatch({
            type: UiActionTypes.UI_DOCUMENT_LAYOUT_ENGINES_SUCCESS,
            payload: models
        })

    } catch (err) {
        dispatch({
            type: UiActionTypes.UI_DOCUMENT_LAYOUT_ENGINES_FAILED,
        })
    }

}
