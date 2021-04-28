import React, {useRef} from 'react';
import {FileUpload} from "primereact/fileupload";
import {useDispatch} from "react-redux";
import {AddPage} from "../actions/pageActions";
import {Toast} from "primereact/toast";

const PageAdd = (props) => {
    const dispatch = useDispatch();
    const ACCEPTED_FILE_TYPES = "image/*"
    const documentId = props.documentId
    const toast = useRef(null);

    const pagesUploader = async (event) => {
        const files = event.files

        if (files) {
            dispatch(AddPage(documentId, files))
            toast.current.show({severity: 'success', summary: 'Success', detail: 'Page(s) have been uploaded.'});
        }
    }

    const emptyTemplate = () => {
        return (
            <div className="p-d-flex p-ai-center p-dir-col">
                <i className="pi pi-image p-mt-3 p-p-5" style={{'fontSize': '5em', borderRadius: '50%', backgroundColor: 'var(--surface-b)', color: 'var(--surface-d)'}}></i>
                <span style={{'fontSize': '1.2em', color: 'var(--text-color-secondary)'}} className="p-my-5">Drag and drop image(s) here</span>
            </div>
        )
    }

    return (
        <div>
            <FileUpload
                name="demo[]"
                url="./upload"
                multiple
                accept={ACCEPTED_FILE_TYPES}
                maxFileSize={10000000}
                customUpload
                uploadHandler={pagesUploader}
                emptyTemplate={emptyTemplate}
            />
            <Toast ref={toast} />

        </div>
    );
};

export default PageAdd;
