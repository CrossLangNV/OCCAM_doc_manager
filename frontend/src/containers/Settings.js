import React, { useRef } from 'react';
import {useDispatch, useSelector} from "react-redux";
import _ from "lodash";
import { FileUpload } from 'primereact/fileupload';
import { GetTmStats, UploadTMX } from '../actions/tmActions';
import { Toast } from 'primereact/toast';
import {Button} from "primereact/button";
import {Col, Row, Table} from "react-bootstrap";

const Settings = () => {
    const dispatch = useDispatch();
    const toast = useRef(null);
    const tmStats = useSelector(state => state.tmStats);
    const uploadRef = useRef(null);

    React.useEffect(() => {
        fetchTmStats();
    }, []);

    const fetchTmStats = () => {
        dispatch(GetTmStats());
    }

    const tmxUploader = async (event) => {
        const files = event.files

        if (files) {
            dispatch(UploadTMX(files[0]));
            toast.current.show({ severity: 'success', summary: 'Success', detail: 'TMX file has been uploaded.' });
            uploadRef.current.clear();
        }
    }

    const loadTableRows = () => {
        if (!_.isEmpty(tmStats.data)) {
            return (
                Object.keys(tmStats.data).map((key, index) => (
                    <tr key={index}>
                        <td className='w-10'>{key}</td>
                        <td>{tmStats.data[key]}</td>
                    </tr>
                ))
            )
        }
    }   


    const showData = () => {
        return (
            <div>
                <h2>Translation Memory</h2>
                <Row className="justify-content-between">
                    <Col>
                        <Button
                            onClick={() => fetchTmStats()}
                            label=""
                            icon="pi pi-refresh"
                            className="p-button-primary margin-left"
                            tooltip="Refresh"
                            tooltipOptions={{ position: 'bottom' }}
                        />
                    </Col>
                </Row>
                <Table striped borderless hover>
                    <thead>
                        <tr>
                            <th>Language pair</th>
                            <th>Amount of TUs</th>
                        </tr>
                    </thead>
                    <tbody>
                        {loadTableRows()}
                    </tbody>
                </Table>
                <FileUpload
                    ref={uploadRef}
                    name="tmx"
                    maxFileSize={1000000}
                    accept={".tmx"}
                    mode="basic"
                    auto={true}
                    customUpload
                    uploadHandler={tmxUploader}
                    chooseLabel="Upload TMX"
                />
                <Toast ref={toast} />
            </div>
        );
    }

    return (
        <div>
            {showData()}
        </div>
    )
};

export default Settings;
