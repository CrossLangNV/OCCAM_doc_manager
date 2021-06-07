import React, {useState} from 'react';
import axios from "axios";
import {Timeline} from "primereact/timeline";
import moment from "moment";
import {baseUrl} from "../../constants/axiosConf";

const PageHistory = (props) => {
    const pageId = props.pageId


    const [history, setHistory] = useState([]);

    React.useEffect(() => {
        fetchHistoryForPage(pageId)
    }, [])

    const fetchHistoryForPage = async (pageId) => {

        const config = {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem("access")}`
            }
        }

        const res = await axios.get(`${baseUrl}/activitylogs/api/activitylogs?rows=100&offset=0&page=${pageId}&linked_overlays=true`,
            config)

        const events = []

        res.data.results.forEach(log => {
            events.push({status: `${log.type} ${log.state}`, date: moment(log.created_at).format("MM/DD/YYYY HH:MM")})
        })

        setHistory(events)

    }

    return (
        <div>
            {/*<Timeline value={history} content={(item) => item.status} />*/}
            <Timeline value={history} opposite={(item) => item.status}
                      content={(item) => <small className="p-text-secondary">{item.date}</small>}/>
        </div>
    );
};

export default PageHistory;
