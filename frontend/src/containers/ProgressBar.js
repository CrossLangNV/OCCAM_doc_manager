import React from 'react';
import {Steps} from "primereact/steps";
import {useHistory} from "react-router-dom";
import {useTranslation} from "react-i18next";

const ProgressBar = (props) => {
    const activeStep = props.activeStep - 1; // -1 because javascript starts with 0
    const documentId = props.documentId; // -1 because javascript starts with 0
    let history = useHistory();
    const {t} = useTranslation();

    const steps = [
        {
            label: t("progress.Document Information"),
            command: (event) => {
                if (documentId !== undefined) {
                    history.push('/document-edit/' + documentId)
                }
            }
        },
        {
            label: t("progress.Upload Pages"),
            command: (event) => {
                if (documentId !== undefined) {
                    history.push('/document/' + documentId + "/add-pages")
                }
            }
        },
        {
            label: t("progress.Layout Analysis"),
            command: (event) => {
                if (documentId !== undefined) {
                    history.push(`/document-edit/${documentId}/layout_model`)
                }
            }
        },
        {
            label: t("progress.Results"),
            command: (event) => {
                if (documentId !== undefined) {
                    history.push('/document/' + documentId)
                }
            }
        },
        {
            label: t("progress.Publish"),
            command: (event) => {
                if (documentId !== undefined) {
                    history.push('/publish/' + documentId)
                }
            }
        }
    ];

    const goToStep = (index) => {

    }



    return (
        <div className='container-fluid'>
            <Steps model={steps} activeIndex={activeStep} onSelect={(e) => goToStep(e.index)} readOnly={false} />
        </div>
    );
};

export default ProgressBar;
