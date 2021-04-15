import {Switch, Route, Redirect, NavLink, Link} from 'react-router-dom'
import DocumentList from "./containers/DocumentList";
import Document from "./containers/Document";
import {Button, Navbar} from "react-bootstrap";
import Header from "./containers/Header";

function App() {
    return (
        <div className="App">
            <Header />
            <div className="space">
                <div className="container-fluid">

                    <Switch>
                        <Route path={"/"} exact component={DocumentList}/>
                        <Route path={"/document/:documentId"} exact component={Document}/>
                    </Switch>
                </div>
            </div>


        </div>
    );
}

export default App;
