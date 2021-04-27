import React from 'react';
import {Tag} from "primereact/tag";

const DocumentState = (props) => {

    const getStateIcon = (state) => {
        switch (state) {
            case "OCR completed.":
                return <Tag value={state} icon="pi pi-check" severity="success"/>
            default:
                return <Tag value={state} />
        }
    }

    return (
        <>
            {getStateIcon(props.state)}
        </>
    );
};

export default DocumentState;
