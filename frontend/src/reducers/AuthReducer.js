import {AuthActionTypes} from "../constants/auth-action-types";

const DefaultState = {
    loading: false,
    access: localStorage.getItem("access"),
    refresh: localStorage.getItem("refresh"),
    isAuthenticated: false,
    user: "",
    errorMsg: "",
};

const AuthReducer = (state = DefaultState, action) => {
    switch (action.type) {
        case AuthActionTypes.GOOGLE_AUTH_LOADING:
            return {
                ...state,
                loading: true,
                errorMsg: "",
            }
        case AuthActionTypes.GOOGLE_AUTH_FAIL:
            return {
                ...state,
                loading: false,
                errorMsg: "Unable to authenticate to django",
            }
        case AuthActionTypes.GOOGLE_AUTH_SUCCESS:
            const accessToken = action.payload.access_token
            const refreshToken = action.payload.refresh_token

            localStorage.setItem("access", accessToken);
            localStorage.setItem("refresh", refreshToken);

            return {
                ...state,
                loading: false,
                isAuthenticated: true,
                access: accessToken,
                refresh: refreshToken,
                errorMsg: "",
                user: action.user
            }
        case AuthActionTypes.LOGOUT:
            localStorage.removeItem('access');
            localStorage.removeItem('refresh');
            return {
                ...state,
                access: null,
                refresh: null,
                isAuthenticated: null,
                user: null
            }
        default:
            return state
    }
}

export default AuthReducer
