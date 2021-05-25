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
                access: accessToken,
                refresh: refreshToken,
                isAuthenticated: true,
                errorMsg: "",
            }

        case AuthActionTypes.GET_USER_SUCCESS:
            return {
                ...state,
                user: action.payload.email,
                isAuthenticated: true
            }

        case AuthActionTypes.GET_USER_FAIL:
            return {
                ...state,
                user: null
            }
        case AuthActionTypes.LOGOUT:
            localStorage.removeItem('access');
            localStorage.removeItem('refresh');
            return {
                ...state,
                access: null,
                refresh: null,
                isAuthenticated: false,
                user: null
            }
        default:
            return state
    }
}

export default AuthReducer
