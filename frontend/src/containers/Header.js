import React from 'react';
import {Button, Form, FormControl, Nav, Navbar} from "react-bootstrap";

import {Link, useLocation} from "react-router-dom";
import {useDispatch, useSelector} from "react-redux";
import {ModifyDocumentQuery} from "../actions/uiActions";
import {GetDocumentList} from "../actions/documentActions";

const Header = () => {
    const location = useLocation()
    const dispatch = useDispatch();

    const uiStates = useSelector(state => state.uiStates);

    const searchDocuments = async (query) => {
        dispatch(ModifyDocumentQuery(query))
        dispatch(GetDocumentList(5, 1, query))
    }

    return (
            <Navbar bg="dark" variant="dark">
                <Navbar.Brand as={Link} to="/">OCCAM</Navbar.Brand>
                <Nav className="mr-auto">
                    <Nav.Link as={Link} to="/">Documents</Nav.Link>
                    <Nav.Link as={Link} to="/history">Job history</Nav.Link>
                    <Nav.Link as={Link} to="/help">Help</Nav.Link>
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
            </Navbar>
    );
};

export default Header;
