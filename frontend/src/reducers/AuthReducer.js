import {AuthActionTypes} from "../constants/auth-action-types";

const DefaultState = {
    loading: false,
    access: localStorage.getItem("access"),
    refresh: localStorage.getItem("refresh"),
    isAuthenticated: localStorage.getItem("isAuthenticated"),
    hasCompletedTutorial: false,
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
            localStorage.setItem("isAuthenticated", "true");

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
                isAuthenticated: true,
                hasCompletedTutorial: action.payload.has_completed,
            }

        case AuthActionTypes.GET_USER_FAIL:
            return {
                ...state,
                user: null
            }
        case AuthActionTypes.LOGOUT:
            localStorage.removeItem('access');
            localStorage.removeItem('refresh');
            localStorage.removeItem('isAuthenticated');
            return {
                ...state,
                access: null,
                refresh: null,
                isAuthenticated: false,
                user: null
            }
        case AuthActionTypes.CHANGE_TUTORIAL_STATE_SUCCESS:
            return {
                ...state,
                hasCompletedTutorial: action.payload
            }
        default:
            return state
    }
}

export default AuthReducer
