import React from 'react';
import ProgressBar from "../ProgressBar";
import {Col, Row} from "react-bootstrap";

const DocumentPublish = (props) => {
    const documentId = props.match.params.documentId

    return (
        <>
            <Row>
                <ProgressBar activeStep={5} documentId={documentId}/>
            </Row>

            <Row className="margin-top">
                <Col>
                    <h3>Publish</h3>
                </Col>
            </Row>
        </>
    );
};

export default DocumentPublish;
