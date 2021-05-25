import React, {useRef} from 'react';
import {FileUpload} from "primereact/fileupload";
import {useDispatch} from "react-redux";
import {Toast} from "primereact/toast";
import {AddOverlay} from "../actions/overlayActions";

const OverlayAdd = (props) => {
    const dispatch = useDispatch();
    const ACCEPTED_FILE_TYPES = "application/xml"
    const pageId = props.pageId
    const toast = useRef(null);
    const label = props.label

    const overlayUploader = async (event) => {
        const files = event.files

        if (files) {
            dispatch(AddOverlay(pageId, files))
            toast.current.show({severity: 'success', summary: 'Success', detail: 'Overlay have been uploaded.'});
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
