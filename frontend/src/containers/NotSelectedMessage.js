import React from 'react';
import {Card} from "primereact/card";
import _ from "lodash";

const NotSelectedMessage = (props) => {
    const context = props.context;
    const message = props.message;

    return (
        <div>
            {((context === "" || _.isEmpty(context)) &&
                <Card className="occ-ui-empty-leaflet-container">
                    <div className="p-d-flex p-ai-center p-dir-col">
                        <i className="pi pi-image p-mt-3 p-p-5" style={{'fontSize': '5em', borderRadius: '50%', backgroundColor: 'var(--surface-b)', color: 'var(--surface-d)'}}/>
                        <span style={{'fontSize': '1.2em', color: 'var(--text-color-secondary)'}} className="p-my-5">{message}</span>
                    </div>
                </Card>
            )}
        </div>
    );
};

export default NotSelectedMessage;
