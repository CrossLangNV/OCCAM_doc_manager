import React, {useState} from 'react';
import axios from "axios";
import {Timeline} from "primereact/timeline";
import {baseUrl} from "../../constants/axiosConf";
import _ from "lodash";

const PageMetadata = (props) => {
    const page = props.page
    const [metadata, setMetadata] = useState([]);

    React.useEffect(() => {
        const labels = []

        const metadata = Object.entries(page.metadata)
        metadata.forEach(label => {
            labels.push({status: `${label[0]}`, date: label[1].join(", ")})
        })

        setMetadata(labels)
    }, [])

    return (
        <div>
            {(_.isEmpty(metadata) &&
                <p>No metadata available.</p>
            )}

            <Timeline value={metadata} opposite={(item) => item.status}
                      content={(item) => <small className="p-text-secondary">{item.date}</small>}/>
        </div>
    );
};

export default PageMetadata;
