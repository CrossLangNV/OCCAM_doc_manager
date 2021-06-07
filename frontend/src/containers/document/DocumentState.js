import React from 'react';
import {Tag} from "primereact/tag";

const DocumentState = (props) => {

    const getStateIcon = (state) => {

        const successStates = ["OCR completed.", "Success"]
        const failStates = ["Failed"]

        if (successStates.includes(state)) {
            return <Tag value={state} icon="pi pi-check" severity="success"/>
        } else if (failStates.includes(state)) {
            return <Tag value={state} icon="pi pi-times" severity="danger"/>
        } else if (!state) {
            return <Tag value="Not started"/>
        } else {
            return <Tag value={state}/>
        }
    }

    return (
        <>
            {getStateIcon(props.state)}
        </>
    );
};

export default DocumentState;
