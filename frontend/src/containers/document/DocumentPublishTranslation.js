import React from 'react';
import {Checkbox} from "primereact/checkbox";

const DocumentPublishTranslation = (props) => {
    const page = props.page;

    const showData = (page) => {
        if (page.page_overlay.length === 0) {
            return <>
                <Checkbox style={{visibility: "hidden"}}
                          inputId={page.id + "/translation"}
                          name="translation"
                          value={page.id}/>
                <label className="m-md-2"
                       htmlFor={page.id + "/translation"}>No translation
                    available</label>
            </>
        }
        return page.page_overlay.map(overlay => {
            if (overlay.overlay_geojson.length > 1) {
                return overlay.overlay_geojson.map(geojson => {
                    return <>
                        <div className="p-field-checkbox m-md-1">
                            <Checkbox inputId={page.id + "/translation"}
                                      name="translation"
                                      value={page.id}/>
                            <label className="m-md-2"
                                   htmlFor={page.id + "/translation"}>{geojson.lang}</label>
                        </div>
                    </>
                })
            }
            return <>
                <Checkbox style={{visibility: "hidden"}}
                          inputId={page.id + "/translation"}
                          name="translation"
                          value={page.id}/>
                <label className="m-md-2"
                       htmlFor={page.id + "/translation"}>No translation
                    available</label>
            </>
        })
    }

    return (
        <>
            {showData(page)}
        </>

    )
};

export default DocumentPublishTranslation;