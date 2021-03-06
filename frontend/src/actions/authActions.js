import {AuthActionTypes} from "../constants/auth-action-types";
import axios from "axios";
import {baseUrl, clientId, clientSecret} from "../constants/axiosConf";


export const load_user = () => async dispatch => {
    if (localStorage.getItem('access')) {
        const config = {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem("access")}`
            }
        }

        dispatch({
            type: AuthActionTypes.GET_USER_LOADING
        });

        try {
            const res = await axios.get(`${baseUrl}/auth/me`,
                config)

            dispatch({
                type: AuthActionTypes.GET_USER_SUCCESS,
                payload: res.data
            });
        } catch (err) {
            dispatch({
                type: AuthActionTypes.GET_USER_FAIL,
                payload: err
            });
        }
    } else {
        dispatch({
            type: AuthActionTypes.GET_USER_FAIL
        });
    }
}

export const GoogleAuthenticate = (accessToken) => async dispatch => {
    try {
        dispatch({
            type: AuthActionTypes.GOOGLE_AUTH_LOADING
        });

        await axios.post(`${baseUrl}/auth/convert-token`,
            {
                grant_type: "convert_token",
                client_id: clientId, // REACT_DJANGO_CLIENT_ID
                client_secret: clientSecret, // REACT_DJANGO_CLIENT_SECRET
                backend: "google-oauth2",
                token: accessToken
            })
            .then((res) => {
                dispatch({
                    type: AuthActionTypes.GOOGLE_AUTH_SUCCESS,
                    payload: res.data,
                });

                dispatch(load_user())
            })
    } catch (e) {
        dispatch({
            type: AuthActionTypes.GOOGLE_AUTH_FAIL
        });
    }
};

export const Logout = () => async dispatch => {
    dispatch({
        type: AuthActionTypes.LOGOUT
    });
}

export const ChangeTutorialState = (userId, value) => async dispatch => {

    dispatch({
        type: AuthActionTypes.CHANGE_TUTORIAL_STATE_LOADING
    })

    try {
        const config = {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem("access")}`
            }
        }

        await axios.post(`${baseUrl}/tutorial/api/usertutorials`,
            {
                "user": userId,
                "value": value
            },
            config)

        dispatch({
            type: AuthActionTypes.CHANGE_TUTORIAL_STATE_SUCCESS,
            payload: value
        })
    } catch (err) {
        dispatch({
            type: AuthActionTypes.CHANGE_TUTORIAL_STATE_FAILED,
        })
    }
}

export const CloseTutorial = () => async dispatch => {

    dispatch({
        type: AuthActionTypes.CHANGE_TUTORIAL_STATE_SUCCESS,
        payload: true
    })

}
