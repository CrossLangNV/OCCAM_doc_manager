import React from 'react';

const DocumentPreview = (props) => {
    const document = props.document;

    const getImage = () => {
        if (document.document_page.length > 0) {
            return document.document_page[0].file
        } else {
            return "/document-logo.png"
        }
    }

    return (
        <img src={getImage()} width="100"/>
    );
};

export default DocumentPreview;
