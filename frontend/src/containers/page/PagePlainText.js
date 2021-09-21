import React from 'react';
import {useTranslation} from "react-i18next";
import {ScrollPanel} from "primereact/scrollpanel";

const PagePlainText = (props) => {
    const content = props.content
    const {t} = useTranslation();

    return (
        <ScrollPanel style={{width: '100%', height: '1000px'}}>
            {(content === "" &&
                <p>{t("page-plaintext.No plain text available")}</p>
            )}

            <p className={"occ-page-plain-text"}>
                {content}
            </p>

        </ScrollPanel>
    );
};

export default PagePlainText;
