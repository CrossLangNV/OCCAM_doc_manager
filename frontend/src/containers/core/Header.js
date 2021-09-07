import React from 'react';
import {Button, Form, FormControl, Nav, Navbar} from "react-bootstrap";

import {Link, useLocation} from "react-router-dom";
import {useDispatch, useSelector} from "react-redux";
import {ModifyDocumentQuery} from "../../actions/uiActions";
import {GetDocumentList} from "../../actions/documentActions";
import {ProgressSpinner} from "primereact/progressspinner";
import {Logout} from "../../actions/authActions";
import {useTranslation} from "react-i18next";

const Header = () => {
    const location = useLocation();
    const dispatch = useDispatch();
    const {t} = useTranslation();

    // Redux
    const pageList = useSelector(state => state.pageList);
    const documentList = useSelector(state => state.documentList);
    const activityList = useSelector(state => state.activityLogsList);
    const auth = useSelector(state => state.auth);
    const uiStates = useSelector(state => state.uiStates);

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

            {(location.pathname !== "/login") &&
                <Nav className="mr-auto">
                    <Nav.Link as={Link} to="/">{t("nav.documents")}</Nav.Link>
                    <Nav.Link as={Link} to="/activity">{t("nav.activity-logs")}</Nav.Link>
                    <Nav.Link as={Link} to="/help">{t("nav.help")}</Nav.Link>
                    <Nav.Link as={Link} to="/settings">{t("nav.settings")}</Nav.Link>

                    {/* Loading spinner */}
                    {(reduxIsLoading()) && (
                        <ProgressSpinner style={{width: '50px', height: '40px'}} strokeWidth="8" fill="#343a40"
                                         animationDuration=".5s"/>
                    )}
                </Nav>
            }


            {/*{location.pathname === "/" &&*/}
            {/*    <Form inline>*/}
            {/*        <FormControl*/}
            {/*            type="text"*/}
            {/*            placeholder={t("nav.search-document")}*/}
            {/*            className="mr-sm-2"*/}
            {/*            value={uiStates.documentQuery}*/}
            {/*            onChange={(e) => {*/}
            {/*                searchDocuments(e.target.value)*/}
            {/*            }}*/}
            {/*            onKeyPress={(e) => {*/}
            {/*                if (e.key === "Enter") {*/}
            {/*                    e.preventDefault()*/}
            {/*                    searchDocuments(e.target.value)*/}
            {/*                }*/}
            {/*            }}*/}
            {/*        />*/}
            {/*        <Button variant="outline-info">{t("nav.search")}</Button>*/}
            {/*    </Form>*/}
            {/*}*/}

            {location.pathname !== "/login" &&
            <Nav>
                {(auth.isAuthenticated) && (
                    <Nav.Link>{auth.user}</Nav.Link>
                )}

                <Nav.Link as={Link} to="/login" onClick={() => dispatch(Logout())}>{t("nav.logout")}</Nav.Link>

            </Nav>
            }
        </Navbar>
    );
};

export default Header;
