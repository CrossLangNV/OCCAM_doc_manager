import {Route, Switch, useHistory, useLocation} from 'react-router-dom'
import DocumentList from "./containers/document/DocumentList";
import Document from "./containers/document/Document";
import Header from "./containers/core/Header";
import DocumentAdd from "./containers/document/DocumentAdd";
import 'primeflex/primeflex.css';
import 'primereact/resources/themes/saga-blue/theme.css';
import 'primereact/resources/primereact.min.css';
import 'primeicons/primeicons.css'
import {Button} from "primereact/button";
import ActivityLogs from "./containers/ActivityLogs";
import GoogleLoginPage from "./containers/core/GoogleLoginPage";
import PrivateRoute from "./containers/core/PrivateRoute";
import {useEffect} from "react";
import {load_user} from "./actions/authActions";
import {useDispatch} from "react-redux";
import {ScrollTop} from "primereact/scrolltop";
import Footer from "./containers/core/Footer";
import PageAdd from "./containers/page/PageAdd";
import DocumentLayoutAnalysis from "./containers/document/DocumentLayoutAnalysis";

function App() {
    const location = useLocation();
    let history = useHistory();

    const dispatch = useDispatch();
    useEffect(() => {
        dispatch(load_user())
    })

    const NO_BACK_BUTTON = ["/", "/login", "/document-add", "/document"]

    return (
        <div className="App">
            <Header/>
            <div className="space">
                <div className="container-fluid">
                    {/*{(!NO_BACK_BUTTON.includes(location.pathname) &&*/}
                    {/*    <>*/}
                    {/*        <Button onClick={() => history.goBack()} className='margin-bottom'>Back</Button>*/}
                    {/*    </>*/}
                    {/*)}*/}
                    <Switch>
                        <PrivateRoute path={"/"} exact component={DocumentList}/>
                        <PrivateRoute path={"/document/:documentId"} exact component={Document}/>
                        <PrivateRoute path={"/document/:documentId/add-pages"} exact component={PageAdd}/>
                        <PrivateRoute path={"/document-add"} exact component={DocumentAdd}/>
                        <PrivateRoute path={"/document-edit/:documentId"} exact component={DocumentAdd}/>
                        <PrivateRoute path={"/activity"} exact component={ActivityLogs}/>
                        <PrivateRoute path={"/document-edit/:documentId/layout_model"} exact component={DocumentLayoutAnalysis}/>
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
