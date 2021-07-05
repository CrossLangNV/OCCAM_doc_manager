import React from 'react';
import ProgressBar from "../ProgressBar";
import {Col, Row} from "react-bootstrap";
import {useTranslation} from "react-i18next";

const DocumentPublish = (props) => {
    const documentId = props.match.params.documentId
    const {t} = useTranslation();

    return (
        <>
            <Row>
                <ProgressBar activeStep={5} documentId={documentId}/>
            </Row>

            <Row className="margin-top">
                <Col>
                    <h3>{t("ui.publish")}</h3>
                </Col>
            </Row>
        </>
    );
};

export default DocumentPublish;
