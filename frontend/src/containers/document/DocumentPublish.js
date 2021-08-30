import React from 'react';
import ProgressBar from "../ProgressBar";
import {Col, Row} from "react-bootstrap";
import {useTranslation} from "react-i18next";
import {Button} from "primereact/button";
import {baseUrl} from "../../constants/axiosConf";
import {useDispatch, useSelector} from "react-redux";
import {GetDocument} from "../../actions/documentActions";
import {ModifySelectedPage} from "../../actions/uiActions";
import _ from "lodash";

const DocumentPublish = (props) => {
    const documentId = props.match.params.documentId;
    const dispatch = useDispatch();
    const {t} = useTranslation();

    // Redux states
    const pageList = useSelector(state => state.pageList);
    const uiStates = useSelector(state => state.uiStates);
    const auth = useSelector(state => state.auth);
    const documentState = useSelector(state => state.document);

    React.useEffect(() => {
        dispatch(GetDocument(documentId))
        dispatch(ModifySelectedPage(""))
    }, [])

    // UI
    const linkStyle = {
        color: 'inherit',
        textDecoration: 'inherit'
    };

    const showData = () => {
        if (!_.isEmpty(documentState.data[documentId])) {

            const documentData = documentState.data[documentId];

            return (
                <>
                    <Row className="justify-content-between">
                        <Col md={3}>
                            <h2>{documentData.name}</h2>
                        </Col>
                        <Col md={9}>
                            <ProgressBar activeStep={5} documentId={documentId}/>
                        </Col>
                    </Row>

                    <Row className="margin-top">
                        <Col>
                            <h3>{t("publish.Metadata")}</h3>
                        </Col>
                    </Row>

                    <Row>
                        <Col>
                            <Button>
                                <a style={linkStyle}
                                   href={`${baseUrl}/documents/api/export/metadata?document=${documentId}`}>{t("publish.Download")}</a>
                            </Button>
                        </Col>
                    </Row>
                </>
            );
        }
        if (documentState.loading) {
            return <p>{t("ui.loading")}...</p>
        }

        if (documentState.errorMsg !== "") {
            return <p>{documentState.errorMsg}</p>
        }

        return <p>{t("document.Error fetching document")}</p>
    }

    return (
        <div>
            {showData()}
        </div>
    )
};

export default DocumentPublish;
