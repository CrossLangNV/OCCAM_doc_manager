import {AuthActionTypes} from "../constants/auth-action-types";

const DefaultState = {
    loading: false,
    data: {},
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
            return {
                ...state,
                loading: false,
                data: action.payload,
                errorMsg: "",
            }
        default:
            return state
    }
}

export default AuthReducer
