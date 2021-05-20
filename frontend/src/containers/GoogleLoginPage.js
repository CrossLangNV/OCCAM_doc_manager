import React from 'react';
import GoogleLogin from "react-google-login";
import {useDispatch} from "react-redux";
import {GoogleAuthenticate} from "../actions/authActions";

const GoogleLoginPage = () => {
    const dispatch = useDispatch();


    const responseGoogle = (response) => {
        console.log(response);
        console.log(response.accessToken);
        console.log(response.profileObj.email);

        dispatch(GoogleAuthenticate(response.accessToken, response.profileObj.email))

    }

    return (
        <div>
            <GoogleLogin
                clientId="929639281599-8ufjqdo3t0plli2iql1710pkg27fth0l.apps.googleusercontent.com"
                onSuccess={responseGoogle}
                isSignedIn={true}
            />
        </div>
    );
};

export default GoogleLoginPage;
