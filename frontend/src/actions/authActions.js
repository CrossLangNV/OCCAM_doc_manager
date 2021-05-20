import axios from 'axios'
import {AuthActionTypes} from "../constants/auth-action-types";

export const GoogleAuthenticate = (state, code) => async dispatch => {
    if (state && code && !localStorage.getItem('access')) {
        const config = {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        };

        const details = {
            'state': state,
            'code': code
        };

        const formBody = Object.keys(details).map(key => encodeURIComponent(key) + '=' + encodeURIComponent(details[key])).join('&');

        try {
            // const res = await axios.post(`${process.env.REACT_APP_API_URL}/auth/o/google-oauth2/?${formBody}`, config);
            const res = await axios.post(`http://localhost:8000/auth/o/google-oauth2/?${formBody}`, config);

            dispatch({
                type: AuthActionTypes.GOOGLE_AUTH_SUCCESS,
                payload: res.data
            });

            dispatch(load_user());
        } catch (err) {
            dispatch({
                type: AuthActionTypes.GOOGLE_AUTH_FAIL
            });
        }
    }
};
