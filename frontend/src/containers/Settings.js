import React, {useRef, useState} from 'react';
import {useDispatch, useSelector} from "react-redux";
import _ from "lodash";
import { FileUpload } from 'primereact/fileupload';
import { GetTmStats, UploadTMX } from '../actions/tmActions';
import { Toast } from 'primereact/toast';
import {Button} from "primereact/button";
import {Col, Row, Table} from "react-bootstrap";
import {ChangeTutorialState} from "../actions/authActions";
import {InputSwitch} from "primereact/inputswitch";
import LanguageSelector from "./core/LanguageSelector";

const Settings = () => {
    // Redux
    const dispatch = useDispatch();
    const tmStats = useSelector(state => state.tmStats);
    const auth = useSelector(state => state.auth);
    const hasCompletedTutorial = auth.hasCompletedTutorial;

    const toast = useRef(null);
    const uploadRef = useRef(null);
    const [checkedTutorial, setCheckedTutorial] = useState(false);


    React.useEffect(() => {
        fetchTmStats();
        if (hasCompletedTutorial === false) {
            setCheckedTutorial(true)
        } else {
            setCheckedTutorial(false)
        }
    }, [hasCompletedTutorial]);

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


    const showTranslationMemoryTable = () => {
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
            </div>
        );
    }

    const showProductTourSetting = () => {
        return (
            <>
                <h2 className="margin-top">Product tour</h2>

                <div className="p-field-checkbox">
                    <InputSwitch inputId="enableTutorial" checked={checkedTutorial} onChange={e => {
                        setCheckedTutorial(e.value)
                        dispatch(ChangeTutorialState(auth.user, !e.value))
                    }} />
                    <label htmlFor="enableTutorial">Show product tour</label>
                </div>
            </>
        )
    }

    const showLanguageSetting = () => {
        return (
            <>
                <h2 className="margin-top">Language</h2>
                <LanguageSelector />
            </>
        )
    }

    return (
        <div>
            {showTranslationMemoryTable()}

            {showProductTourSetting()}

            {showLanguageSetting()}

            <Toast ref={toast} />
        </div>
    )
};

export default Settings;
