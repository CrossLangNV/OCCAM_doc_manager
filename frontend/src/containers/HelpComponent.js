import React, {useState} from 'react';
import axios from "axios";
import {baseUrl} from "../constants/axiosConf";

import ReactHtmlParser from 'react-html-parser';



const HelpComponent = () => {

    const [manualHtml, setManualHtml] = useState("");


    React.useEffect(() => {
        testGetConfluenceContent()
    }, []);

    const testGetConfluenceContent = async () => {
        const config = {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem("access")}`
            }
        }

        // Get available models/engines
        try {
            const res = await axios.get(`${baseUrl}/tutorial/api/help_page`, config)
            setManualHtml(res.data)
        } catch (e) {
            setManualHtml("Cannot connect to Confluence. ")
        }

    }

    return (
        <div>
            { ReactHtmlParser (manualHtml) }
        </div>
    );
};

export default HelpComponent;
