import {AuthActionTypes} from "../constants/auth-action-types";
import axios from "axios";
import {baseUrl} from "../constants/axiosConf";

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
                type: AuthActionTypes.GET_USER_FAIL
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

        const baseUrl = window._env_.REACT_APP_API_URL

        await axios.post(`/auth/convert-token`,
            {
                grant_type: "convert_token",
                client_id: window._env_.REACT_DJANGO_CLIENT_ID, // REACT_DJANGO_CLIENT_ID
                client_secret: window._env_.REACT_DJANGO_CLIENT_SECRET, // REACT_DJANGO_CLIENT_SECRET
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

export const CheckAuthenticated = () => async dispatch => {
    if (localStorage.getItem('access')) {

    }
}
