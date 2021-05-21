import React, {useRef} from 'react';
import GoogleLogin from "react-google-login";
import {useDispatch} from "react-redux";
import {GoogleAuthenticate} from "../actions/authActions";
import {useHistory} from "react-router-dom";

const GoogleLoginPage = () => {
    const dispatch = useDispatch();
    const history = useHistory();
    const toast = useRef(null);


    const responseGoogle = async (response) => {
        try {
            await dispatch(GoogleAuthenticate(response.accessToken, response.profileObj.email))
            history.push("/")
        } catch (e) {
            console.log(e.message)
        }
    }

    const onFailureMessage = () => {
        toast.current.show({severity: 'danger', summary: 'Failed', detail: 'Google authentication failed'});
    }

    return (
        <div>
            <h5>Login with Google</h5>
            <GoogleLogin
                clientId="929639281599-8ufjqdo3t0plli2iql1710pkg27fth0l.apps.googleusercontent.com"
                onSuccess={responseGoogle}
                onFailure={onFailureMessage}
            />
        </div>
    );
};

export default GoogleLoginPage;
