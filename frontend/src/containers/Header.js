import React from 'react';
import {Button, Form, FormControl, Nav, Navbar, NavLink} from "react-bootstrap";

import {Link} from "react-router-dom";

const Header = () => {
    return (
            <Navbar bg="dark" variant="dark">
                <Navbar.Brand as={Link} to="/">OCCAM</Navbar.Brand>
                <Nav className="mr-auto">
                    <Nav.Link as={Link} to="/">Documents</Nav.Link>
                    <Nav.Link as={Link} to="/history">Job history</Nav.Link>
                    <Nav.Link as={Link} to="/help">Help</Nav.Link>
                </Nav>
                <Form inline>
                    <FormControl type="text" placeholder="Search document" className="mr-sm-2" />
                    <Button variant="outline-info">Search</Button>
                </Form>
            </Navbar>
    );
};

export default Header;
