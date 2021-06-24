import React from 'react';
import _ from "lodash";

const PagePlainText = (props) => {
    const content = props.content
    return (
        <div>
            {(content === "" &&
                <p>No plain text available. </p>
            )}

            { content }
        </div>
    );
};

export default PagePlainText;
