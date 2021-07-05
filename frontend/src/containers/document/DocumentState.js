import React from 'react';
import {Tag} from "primereact/tag";
import {useTranslation} from "react-i18next";

const DocumentState = (props) => {
    const {t} = useTranslation();

    const getStateIcon = (state) => {

        const successStates = ["OCR completed.", "Success"]
        const failStates = ["Failed"]

        if (successStates.includes(state)) {
            return <Tag value={t(state)} icon="pi pi-check" severity="success"/>
        } else if (failStates.includes(state)) {
            return <Tag value={t(state)} icon="pi pi-times" severity="danger"/>
        } else if (!state) {
            return <Tag value={t("ui.not-started")}/>
        } else {
            return <Tag value={t(state)}/>
        }
    }

    return (
        <>
            {getStateIcon(props.state)}
        </>
    );
};

export default DocumentState;
