import React from 'react';
import {Checkbox} from "primereact/checkbox";

const DocumentPublishOverlay = (props) => {
    const page = props.page;

    const showData = (page) => {
        if (page.page_overlay.length === 0) {
            return <>
                <Checkbox style={{visibility: "hidden"}} inputId={page.id + "/overlay"}
                          name="overlay"
                          value={page.id}/>
                <label className="m-md-2"
                       htmlFor={page.id + "/overlay"}>No overlay available</label>
            </>
        }
        return page.page_overlay.map(overlay => {
            return <>
                <div className="p-field-checkbox m-md-1">
                    <Checkbox inputId={page.id + "/overlay"} name="overlay"
                              value={page.id}/>
                    <label className="m-md-2"
                           htmlFor={page.id + "/overlay"}>Overlay</label>
                </div>
            </>
        })
    }

    return (
        <>
            {showData(page)}
        </>
    )
};

export default DocumentPublishOverlay;