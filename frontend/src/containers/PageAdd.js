import React, {useRef, useState} from 'react';
import {FileUpload} from "primereact/fileupload";
import axios from "axios";
import {useDispatch} from "react-redux";
import {AddPage} from "../actions/pageActions";
import {Toast} from "primereact/toast";

const PageAdd = (props) => {
    const dispatch = useDispatch();
    const ACCEPTED_FILE_TYPES = "image/*,application/pdf"
    const documentId = props.documentId
    const toast = useRef(null);

    const pagesUploader = async (event) => {
        const files = event.files

        if (files) {
            dispatch(AddPage(documentId, files))
            toast.current.show({severity: 'success', summary: 'Success Message', detail: 'Pages have been uploaded.'});
        }
    }

    return (
        <div>
            <FileUpload
                name="demo[]"
                url="./upload"
                multiple
                accept={ACCEPTED_FILE_TYPES}
                maxFileSize={1000000}
                customUpload
                uploadHandler={pagesUploader}
            />
            <Toast ref={toast} />

        </div>
    );
};

export default PageAdd;
