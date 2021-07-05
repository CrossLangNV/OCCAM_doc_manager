import React, {useEffect, useRef, useState} from 'react';
import {FileUpload} from "primereact/fileupload";
import {useDispatch, useSelector} from "react-redux";
import {AddPage} from "../../actions/pageActions";
import {Toast} from "primereact/toast";
import ProgressBar from "../ProgressBar";
import {Col, Row} from "react-bootstrap";
import {Button} from "primereact/button";
import {useHistory} from "react-router-dom";
import Tour from "reactour";
import {ChangeTutorialState, CloseTutorial} from "../../actions/authActions";
import {useTranslation} from "react-i18next";

const PageAdd = (props) => {
    const dispatch = useDispatch();
    const ACCEPTED_FILE_TYPES = "image/*"
    const documentId = props.match.params.documentId
    const toast = useRef(null);
    const history = useHistory();
    const {t} = useTranslation();

    const auth = useSelector(state => state.auth);

    const pagesUploader = async (event) => {
        const files = event.files

        if (files) {
            dispatch(AddPage(documentId, files))
            toast.current.show({severity: 'info', summary: 'Success', detail: t("page-add.Page(s) have been uploaded")});
        }
    }

    const emptyTemplate = () => {
        return (
            <div className="p-d-flex p-ai-center p-dir-col">
                <i className="pi pi-image p-mt-3 p-p-5" style={{
                    'fontSize': '5em',
                    borderRadius: '50%',
                    backgroundColor: 'var(--surface-b)',
                    color: 'var(--surface-d)'
                }}/>
                <span style={{'fontSize': '1.2em', color: 'var(--text-color-secondary)'}} className="p-my-5">{t("page-add.Drag and drop image(s) here")}</span>
            </div>
        )
    }

    const nextStep = () => {
        history.push(`/document-edit/${documentId}/layout_model`)
    }

    const steps = [
        {
            selector: '.upload-pages-step-one',
            content: () => (
                <div>
                    <h3>Upload pages</h3>
                    <p>Press the <Button label="Choose" icon="pi pi-plus"/> button to select images or PDF files
                        that you wish to add to your document. </p>
                    <p>All pages in a PDF file will automatically be converted to images.</p>
                    <p>Documents will automatically be uploaded once you selected them from your system.</p>
                    <br/>
                    <Button label={t("tour.skip")} onClick={() => {
                        dispatch(ChangeTutorialState(auth.user, true))
                    }}/>
                </div>
            )
        },
        {
            selector: '.upload-pages-step-two',
            content: () => (
                <div>
                    <h3>Next</h3>
                    <p>When you have selected all your pages, you can press this button to proceed to the next step.</p>
                </div>
            )
        },
    ]



    return (
        <Col>
            <Tour
                steps={steps}
                isOpen={!auth.hasCompletedTutorial}
                onRequestClose={() => dispatch(CloseTutorial())}
            />

            <Row>
                <ProgressBar activeStep={2} documentId={documentId}/>
            </Row>

            <FileUpload
                name="demo[]"
                url="./upload"
                multiple
                accept={ACCEPTED_FILE_TYPES}
                maxFileSize={10000000}
                customUpload
                uploadHandler={pagesUploader}
                emptyTemplate={emptyTemplate}
                className="margin-top upload-pages-step-one"
                auto={true}
            />
            <Toast ref={toast} />

            <Row className="margin-top">
                <Col md={6} />
                <Col md="auto">
                    <Button className="upload-pages-step-two" onClick={nextStep} label="Next"/>
                </Col>
            </Row>
        </Col>

    );
};

export default PageAdd;
