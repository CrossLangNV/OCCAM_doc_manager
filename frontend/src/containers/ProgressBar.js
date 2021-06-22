import React, {useState} from 'react';
import {Steps} from "primereact/steps";
import {useHistory} from "react-router-dom";

const ProgressBar = (props) => {
    const activeStep = props.activeStep - 1; // -1 because javascript starts with 0
    const documentId = props.documentId; // -1 because javascript starts with 0
    let history = useHistory();

    const steps = [
        {
            label: 'Document Information',
            command: (event) => {
                if (documentId !== undefined) {
                    history.push('/document-edit/' + documentId)
                }
            }
        },
        {
            label: 'Upload Pages',
            command: (event) => {
                if (documentId !== undefined) {
                    history.push('/document/' + documentId + "/add-pages")
                }
            }
        },
        {
            label: 'Layout Analysis',
            command: (event) => {
                if (documentId !== undefined) {
                    history.push(`/document-edit/${documentId}/layout_model`)
                }
            }
        },
        {
            label: 'Results',
            command: (event) => {
                if (documentId !== undefined) {
                    history.push('/document/' + documentId)
                }
            }
        },
        {
            label: 'Publish',
            command: (event) => {

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
