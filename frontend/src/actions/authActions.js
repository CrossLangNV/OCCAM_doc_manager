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

        await axios.post(`${baseUrl}/auth/convert-token`,
            {
                grant_type: "convert_token",
                client_id: "kw1n5yIOASh5JUAMk1Vb4SIfDpUsO0QcvMZTqIJl", // REACT_DJANGO_CLIENT_ID
                client_secret: "Rt2fMrYufDxGFnGaIIQnJvdwa5P9WibwuwYUMaalfRR2pb2W4It4n3jMxuRzs4OpolLFmWUklUflwKIm1VTIJfoPcCUVQzBnREmBZG43NepHBfXoY9V3G2e7h2gAgNeI", // REACT_DJANGO_CLIENT_SECRET
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
