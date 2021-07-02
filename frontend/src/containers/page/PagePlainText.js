import React from 'react';
import _ from "lodash";
import {useTranslation} from "react-i18next";

const PagePlainText = (props) => {
    const content = props.content
    const {t} = useTranslation();

    return (
        <div>
            {(content === "" &&
                <p>{t("page-plaintext.No plain text available")}</p>
            )}

            { content }
        </div>
    );
};

export default PagePlainText;
