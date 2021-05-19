import {Switch, Route, Redirect, NavLink, Link, useHistory, useLocation} from 'react-router-dom'
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

function App() {
    let history = useHistory();
    const location = useLocation()

    return (
        <div className="App">
            <Header />
            <div className="space">
                <div className="container-fluid">
                    {(location.pathname !== "/" &&
                            <>
                                <Button onClick={() => history.goBack()} className='margin-bottom'>Back</Button>
                            </>

                    )}
                    <Switch>
                        <Route path={"/"} exact component={DocumentList}/>
                        <Route path={"/document/:documentId"} exact component={Document}/>
                        <Route path={"/document-add"} exact component={DocumentAdd}/>
                        <Route path={"/activity"} exact component={ActivityLogs}/>
                    </Switch>
                </div>
            </div>

            <div className="space"></div>

        </div>
    );
}

export default App;
