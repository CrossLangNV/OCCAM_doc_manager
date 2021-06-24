import React from 'react';
import {useSelector} from "react-redux";
import {Route} from "react-router-dom";
import { Redirect } from 'react-router-dom';


const PrivateRoute = ({ component: Component, ...rest }) => {
    const auth = useSelector(state => state.auth);
    const isAuthenticated = auth.isAuthenticated

    return (
        <Route
            {...rest}
            render={props =>
                isAuthenticated ? (
                    <Component {...props} />
                ) : (
                    <Redirect to={{ pathname: '/login', state: { from: props.location } }} />
                )
            }
        />
    );
};

export default PrivateRoute;
