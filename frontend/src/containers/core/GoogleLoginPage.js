import React, {useEffect, useRef} from 'react';
import GoogleLogin from "react-google-login";
import {useDispatch, useSelector} from "react-redux";
import {GoogleAuthenticate, load_user} from "../../actions/authActions";
import {useHistory} from "react-router-dom";
import {Toast} from "primereact/toast";
import {Card} from "primereact/card";
import {googleOauthKey} from "../../constants/axiosConf";
import {Col, Row} from "react-bootstrap";

const GoogleLoginPage = () => {
    const dispatch = useDispatch();
    const history = useHistory();
    const toast = useRef(null);

    const auth = useSelector(state => state.auth)

    useEffect(() => {
        if (auth.isAuthenticated) {
            history.push("/")
        }
    })

    const responseGoogle = async (response) => {
        try {
            await dispatch(GoogleAuthenticate(response.accessToken))
            history.push("/")
        } catch (e) {
            console.log(e.message)
        }
    }

    const onFailureMessage = () => {
        toast.current.show({severity: 'error', summary: 'Failed', detail: 'Google authentication failed'});
    }

    return (
        <div className="occ-login">
            <Row>
                <Col>
                    <img
                    alt="OCCAM"
                    src="/occam-logo.png"
                    width="100"
                    height="100"
                    className="d-inline-block"
                />
                    <span className="occ-branding-login">OCCAM</span>
                </Col>

            </Row>


            <Card className="occ-login-card">
                <h5>Sign in with Google</h5>
                <br/>
                <GoogleLogin
                    clientId={googleOauthKey}
                    onSuccess={responseGoogle}
                    onFailure={onFailureMessage}
                />
            </Card>

            <Toast ref={toast} />
        </div>
    );
};

export default GoogleLoginPage;
