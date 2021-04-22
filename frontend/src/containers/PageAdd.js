import React from 'react';
import {FileUpload} from "primereact/fileupload";

const PageAdd = (props) => {
    const ACCEPTED_FILE_TYPES = "image/*,application/pdf"
    const documentId = props.documentId

    const pagesUploader = (event) => {
        const files = event.files
        console.log(files)
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
        </div>
    );
};

export default PageAdd;
