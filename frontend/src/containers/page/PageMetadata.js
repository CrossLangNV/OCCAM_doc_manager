import React, {useState} from 'react';
import axios from "axios";
import {Timeline} from "primereact/timeline";
import {baseUrl} from "../../constants/axiosConf";
import _ from "lodash";
import {useTranslation} from "react-i18next";

const PageMetadata = (props) => {
    const page = props.page
    const [metadata, setMetadata] = useState([]);
    const {t} = useTranslation();

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
                <p>{t("page-metadata.No metadata available")}</p>
            )}

            <Timeline value={metadata} opposite={(item) => item.status}
                      content={(item) => <small className="p-text-secondary">{item.date}</small>}/>
        </div>
    );
};

export default PageMetadata;
