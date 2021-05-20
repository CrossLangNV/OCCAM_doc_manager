import axios from 'axios'
import {AuthActionTypes} from "../constants/auth-action-types";

export const GoogleAuthenticate = (accessToken, email) => async dispatch => {
    try {
        dispatch({
            type: AuthActionTypes.GOOGLE_AUTH_LOADING
        });

        await axios.post(`http://localhost:8000/auth/convert-token`,
            {
                grant_type: "convert_token",
                client_id: "kw1n5yIOASh5JUAMk1Vb4SIfDpUsO0QcvMZTqIJl", // REACT_DJANGO_CLIENT_ID
                client_secret: "Rt2fMrYufDxGFnGaIIQnJvdwa5P9WibwuwYUMaalfRR2pb2W4It4n3jMxuRzs4OpolLFmWUklUflwKIm1VTIJfoPcCUVQzBnREmBZG43NepHBfXoY9V3G2e7h2gAgNeI", // REACT_DJANGO_CLIENT_SECRET
                backend: "google-oauth2",
                token: accessToken,
                email: email,
            })
            .then((res) => {
                dispatch({
                    type: AuthActionTypes.GOOGLE_AUTH_SUCCESS,
                    payload: res.data
                })
            })
    } catch (e) {
        dispatch({
            type: AuthActionTypes.GOOGLE_AUTH_FAIL
        });
    }
};
