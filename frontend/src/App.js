import {Route, Switch, useHistory, useLocation} from 'react-router-dom'
import DocumentList from "./containers/document/DocumentList";
import Document from "./containers/document/Document";
import Header from "./containers/core/Header";
import DocumentAdd from "./containers/document/DocumentAdd";
import 'primeflex/primeflex.css';
import 'primereact/resources/themes/saga-blue/theme.css';
import 'primereact/resources/primereact.min.css';
import 'primeicons/primeicons.css'
import ActivityLogs from "./containers/ActivityLogs";
import GoogleLoginPage from "./containers/core/GoogleLoginPage";
import PrivateRoute from "./containers/core/PrivateRoute";
import React, {useEffect} from "react";
import {load_user} from "./actions/authActions";
import {useDispatch, useSelector} from "react-redux";
import {ScrollTop} from "primereact/scrolltop";
import Footer from "./containers/core/Footer";
import Settings from './containers/Settings';
import PageAdd from "./containers/page/PageAdd";
import DocumentLayoutAnalysis from "./containers/document/DocumentLayoutAnalysis";
import HelpComponent from "./containers/HelpComponent";
import DocumentPublish from "./containers/document/DocumentPublish";
import {GetWebsites} from "./actions/uiActions";
import Feedback from "feeder-react-feedback";
import "feeder-react-feedback/dist/feeder-react-feedback.css";

function App() {
    // Don't remove these unused location/history variables, otherwise react tour will only open after refreshing
    const location = useLocation();
    let history = useHistory();

    const dispatch = useDispatch();


    useEffect(() => {
        dispatch(load_user())
        dispatch(GetWebsites())
    }, [])

    const auth = useSelector(state => state.auth);


    return (
        <div className="App">
            <Header/>
            <div className="space">
                <div className="container-fluid">
                    <Switch>
                        <PrivateRoute path={"/"} exact component={DocumentList}/>
                        <PrivateRoute path={"/document/:documentId"} exact component={Document}/>
                        <PrivateRoute path={"/document/:documentId/add-pages"} exact component={PageAdd}/>
                        <PrivateRoute path={"/document-add"} exact component={DocumentAdd}/>
                        <PrivateRoute path={"/document-edit/:documentId"} exact component={DocumentAdd}/>
                        <PrivateRoute path={"/activity"} exact component={ActivityLogs}/>
                        <PrivateRoute path={"/settings"} exact component={Settings}/>
                        <PrivateRoute path={"/document-edit/:documentId/layout_model"} exact
                                      component={DocumentLayoutAnalysis}/>
                        <PrivateRoute path={"/help"} exact component={HelpComponent}/>
                        <PrivateRoute path={"/publish/:documentId"} exact component={DocumentPublish}/>
                        <Route path={"/login"} exact component={GoogleLoginPage}/>
                    </Switch>
                </div>
            </div>
            <Footer/>
            <ScrollTop/>
            <Feedback
                projectId={"614c89c976003e00042e592a"}
                tooltip={true}
                email={true}
                emailRequired={true}
                emailDefaultValue={auth.user}
                primaryColor={"#2196F3"}
            />
        </div>
    );
}

export default App;
