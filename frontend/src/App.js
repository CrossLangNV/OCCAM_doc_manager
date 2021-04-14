import {Switch, Route, Redirect, NavLink, Link} from 'react-router-dom'
import DocumentList from "./containers/DocumentList";
import Document from "./containers/Document";
import {Navbar} from "react-bootstrap";

function App() {
    return (
        <div className="App">
            <nav>
                <NavLink to={"/document/"}>Search by doc id</NavLink>
            </nav>
            <Switch>
                <Route path={"/"} exact component={DocumentList}/>
                <Route path={"/document/:documentId"} exact component={Document}/>
                <Redirect to={"/"} />
            </Switch>
        </div>
    );
}

export default App;
