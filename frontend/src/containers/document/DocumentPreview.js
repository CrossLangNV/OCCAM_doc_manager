import React from 'react';

const DocumentPreview = ({document}) => {

    return (
        <>
            {document.document_page.length > 0 ?
                <img src={document.document_page[0].file} width="100"/>
                :
                <i className="pi pi-image p-mt-3 p-p-2" style={{
                    'fontSize': '5em',
                    borderRadius: '10%',
                    backgroundColor: 'var(--surface-b)',
                    color: 'var(--surface-d)'
                }}/>
            }
        </>
    );
};

export default DocumentPreview;
