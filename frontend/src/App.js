import {Route, Switch, useHistory, useLocation} from 'react-router-dom'
import DocumentList from "./containers/document/DocumentList";
import Document from "./containers/document/Document";
import Header from "./containers/Header";
import DocumentAdd from "./containers/document/DocumentAdd";
import 'primeflex/primeflex.css';
import 'primereact/resources/themes/saga-blue/theme.css';
import 'primereact/resources/primereact.min.css';
import 'primeicons/primeicons.css'
import {Button} from "primereact/button";
import ActivityLogs from "./containers/ActivityLogs";
import GoogleLoginPage from "./containers/GoogleLoginPage";
import PrivateRoute from "./containers/PrivateRoute";
import {useEffect} from "react";
import {load_user} from "./actions/authActions";
import {useDispatch} from "react-redux";
import {ScrollTop} from "primereact/scrolltop";
import Footer from "./containers/Footer";
import Settings from './containers/Settings';

function App() {
    const location = useLocation();
    let history = useHistory();

    const dispatch = useDispatch();
    useEffect(() => {
        dispatch(load_user())
    })

    const NO_BACK_BUTTON = ["/", "/login"]

    return (
        <div className="App">
            <Header/>
            <div className="space">
                <div className="container-fluid">
                    {(!NO_BACK_BUTTON.includes(location.pathname) &&
                        <>
                            <Button onClick={() => history.goBack()} className='margin-bottom'>Back</Button>
                        </>
                    )}
                    <Switch>
                        <PrivateRoute path={"/"} exact component={DocumentList}/>
                        <PrivateRoute path={"/document/:documentId"} exact component={Document}/>
                        <PrivateRoute path={"/document-add"} exact component={DocumentAdd}/>
                        <PrivateRoute path={"/activity"} exact component={ActivityLogs}/>
                        <PrivateRoute path={"/settings"} exact component={Settings}/>
                        <Route path={"/login"} exact component={GoogleLoginPage}/>
                    </Switch>
                </div>
            </div>
            <Footer />
            <ScrollTop />
        </div>
    );
}

export default App;
