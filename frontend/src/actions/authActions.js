import {AuthActionTypes} from "../constants/auth-action-types";
import axios from "axios";
import {baseUrl} from "../constants/axiosConf";

export const GoogleAuthenticate = (accessToken, user) => async dispatch => {
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
                    user: user
                });
                // localStorage.setItem("access", res.data.access_token);
                // localStorage.setItem("refresh", res.data.refresh_token);
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
