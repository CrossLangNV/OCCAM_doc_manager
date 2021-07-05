import React, {useState} from 'react';
import axios from "axios";
import {Timeline} from "primereact/timeline";
import moment from "moment";
import {baseUrl} from "../../constants/axiosConf";
import _ from "lodash";
import {useTranslation} from "react-i18next";

const PageHistory = (props) => {
    const pageId = props.pageId
    const {t} = useTranslation();


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
            {(_.isEmpty(history) &&
                <p>{t("page-history.No history available")}</p>
            )}
            <Timeline value={history} opposite={(item) => item.status}
                      content={(item) => <small className="p-text-secondary">{item.date}</small>}/>
        </div>
    );
};

export default PageHistory;
