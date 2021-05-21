import {Route, Switch, useHistory, useLocation} from 'react-router-dom'
import DocumentList from "./containers/DocumentList";
import Document from "./containers/Document";
import Header from "./containers/Header";
import DocumentAdd from "./containers/DocumentAdd";
import 'primeflex/primeflex.css';
import 'primereact/resources/themes/saga-blue/theme.css';
import 'primereact/resources/primereact.min.css';
import 'primeicons/primeicons.css'
import {Button} from "primereact/button";
import ActivityLogs from "./containers/ActivityLogs";
import GoogleLoginPage from "./containers/GoogleLoginPage";
import PrivateRoute from "./containers/PrivateRoute";

function App() {
    const location = useLocation();
    let history = useHistory();

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
                        <Route path={"/login"} exact component={GoogleLoginPage}/>
                    </Switch>
                </div>
            </div>
        </div>
    );
}

export default App;
