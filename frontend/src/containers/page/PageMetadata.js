import React, {useState} from 'react';
import axios from "axios";
import {Timeline} from "primereact/timeline";

const PageHistory = (props) => {
    const pageId = props.pageId


    const [metadata, setMetadata] = useState([]);

    React.useEffect(() => {
        fetchMetadataForPage(pageId)
    }, [])

    const fetchMetadataForPage = async (pageId) => {
        const baseUrl = process.env.REACT_APP_API_URL

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
