import React, {useRef} from 'react';
import {FileUpload} from "primereact/fileupload";
import {useDispatch} from "react-redux";
import {Toast} from "primereact/toast";
import {AddOverlay} from "../../actions/overlayActions";
import {useTranslation} from "react-i18next";

const OverlayAdd = (props) => {
    const dispatch = useDispatch();
    const ACCEPTED_FILE_TYPES = "application/xml"
    const pageId = props.pageId
    const toast = useRef(null);
    const label = props.label
    const {t} = useTranslation();

    const overlayUploader = async (event) => {
        const files = event.files

        if (files) {
            dispatch(AddOverlay(pageId, files))
            toast.current.show({severity: 'success', summary: 'Success', detail: t("overlay-add.Overlay has been uploaded")});
        }
    }

    return (
        <>
            <FileUpload
                name="demo[]"
                url="./upload"
                accept={ACCEPTED_FILE_TYPES}
                maxFileSize={1000000}
                customUpload
                uploadHandler={overlayUploader}
                mode="basic"
                chooseLabel={label}
            />
            <Toast ref={toast} />
        </>
    );
};

export default OverlayAdd;
