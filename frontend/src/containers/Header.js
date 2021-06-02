import React from 'react';
import {Button, Container, Form, FormControl, Nav, Navbar} from "react-bootstrap";

import {Link, useLocation} from "react-router-dom";
import {useDispatch, useSelector} from "react-redux";
import {ModifyDocumentQuery} from "../actions/uiActions";
import {GetDocumentList} from "../actions/documentActions";
import {ProgressSpinner} from "primereact/progressspinner";
import {Logout} from "../actions/authActions";

const Header = () => {
    const location = useLocation();
    const dispatch = useDispatch();

    const uiStates = useSelector(state => state.uiStates);

    // For the loading spinner
    const pageList = useSelector(state => state.pageList);
    const documentList = useSelector(state => state.documentList);
    const activityList = useSelector(state => state.activityLogsList);
    const auth = useSelector(state => state.auth);

    const searchDocuments = async (query) => {
        dispatch(ModifyDocumentQuery(query))
        dispatch(GetDocumentList(5, 1, query))
    }

    const reduxIsLoading = () => {
        return pageList.loading || documentList.loading || activityList.loading
    }

    return (
        <Navbar bg="dark" variant="dark">

            <Navbar.Brand as={Link} to="/">
                <img
                    alt="OCCAM"
                    src="/occam-logo.png"
                    width="30"
                    height="30"
                    className="d-inline-block align-top"
                />{' '}
                OCCAM
            </Navbar.Brand>
            <Nav className="mr-auto">
                <Nav.Link as={Link} to="/">Documents</Nav.Link>
                <Nav.Link as={Link} to="/activity">Activity logs</Nav.Link>
                <Nav.Link as={Link} to="/help">Help</Nav.Link>

                {/* Loading spinner */}
                {(reduxIsLoading()) && (
                    <ProgressSpinner style={{width: '50px', height: '40px'}} strokeWidth="8" fill="#343a40"
                                     animationDuration=".5s"/>
                )}
            </Nav>


            {location.pathname === "/" &&
                <Form inline>
                    <FormControl
                        type="text"
                        placeholder="Search document"
                        className="mr-sm-2"
                        value={uiStates.documentQuery}
                        onChange={(e) => {
                            searchDocuments(e.target.value)
                        }}
                        onKeyPress={(e) => {
                            if (e.key === "Enter") {
                                e.preventDefault()
                                searchDocuments(e.target.value)
                            }
                        }}
                    />
                    <Button variant="outline-info">Search</Button>
                </Form>
            }

            {location.pathname !== "/login" &&
            <Nav>
                {(auth.isAuthenticated) && (
                    <Nav.Link>{auth.user}</Nav.Link>
                )}

                <Nav.Link as={Link} to="/login" onClick={() => dispatch(Logout())}>Logout</Nav.Link>
            </Nav>
            }
        </Navbar>
    );
};

export default Header;
