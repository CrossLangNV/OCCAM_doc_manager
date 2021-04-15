import {Switch, Route, Redirect, NavLink, Link} from 'react-router-dom'
import DocumentList from "./containers/DocumentList";
import Document from "./containers/Document";
import {Navbar} from "react-bootstrap";
import Header from "./containers/Header";

function App() {
    return (
        <div className="App">
            <Header />
            <Switch>
                <Route path={"/"} exact component={DocumentList}/>
                <Route path={"/document/:documentId"} exact component={Document}/>
            </Switch>
        </div>
    );
}

export default App;
