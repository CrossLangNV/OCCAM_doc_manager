import React, {useState} from 'react';
import axios from "axios";
import {Timeline} from "primereact/timeline";
import {baseUrl} from "../../constants/axiosConf";

const PageHistory = (props) => {
    const page = props.page
    const pageId = page.id

    // TODO
    // page.metadata
    // page.metadata_xml

    const [metadata, setMetadata] = useState([]);

    React.useEffect(() => {
        fetchMetadataForPage(pageId)
    }, [])

    const fetchMetadataForPage = async (pageId) => {

        const config = {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem("access")}`
            }
        }

        const res = await axios.get(`${baseUrl}/documents/api/labels?pageId=${pageId}`,
            config)

        console.log(res)

        const labels = []

        res.data.forEach(label => {
            labels.push({status: `${label.name}`, date: label.value})
        })

        setMetadata(labels)

    }

    return (
        <div>
            <Timeline value={metadata} opposite={(item) => item.status}
                      content={(item) => <small className="p-text-secondary">{item.date}</small>}/>
        </div>
    );
};

export default PageHistory;
