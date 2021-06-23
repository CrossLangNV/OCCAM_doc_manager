import React, {useEffect, useRef, useState} from 'react';
import {useHistory} from "react-router-dom";
import {Col, Row} from "react-bootstrap";
import ProgressBar from "../ProgressBar";
import {Card} from "primereact/card";
import {RadioButton} from "primereact/radiobutton";
import {Button} from "primereact/button";
import axios from "axios";
import {baseUrl} from "../../constants/axiosConf";
import {Toast} from "primereact/toast";
import {GetLayoutEngines, ModifySelectedEngine} from "../../actions/uiActions";
import {useDispatch, useSelector} from "react-redux";
import _ from "lodash"

const DocumentLayoutAnalysis = (props) => {
    const documentId = props.match.params.documentId
    let history = useHistory();
    const toast = useRef(null);
    const dispatch = useDispatch();
    const uiStates = useSelector(state => state.uiStates);
    const [selectedOption, setSelectedOption] = useState([]);



    const config = {
        headers: {
            'Authorization': `Bearer ${localStorage.getItem("access")}`
        }
    }

    useEffect(() => {
        dispatch(GetLayoutEngines(documentId));
    }, [])

    const handleSubmit = async (evt) => {
        evt.preventDefault();

        const data = {
            layout_analysis_model: uiStates.selected_layout_engine[0].id,
        }

        await axios.put(`${baseUrl}/documents/api/document/${documentId}`, data, config
        ).then((res) => {
            history.push(`/document/${documentId}`)
        });

    }

    const changeSelected = (e) => {
        setSelectedOption(e)
        dispatch(ModifySelectedEngine(uiStates.layout_engines.filter(p => {
            return e.id === p.id;
        })))
    }

    return (
        <>
            <Row>
                <ProgressBar activeStep={3} documentId={documentId}/>
            </Row>

            <Row className="margin-top">
                <Col md={3} />
                <Col md={6}>
                    <Card>
                        <h5>Choose a layout analysis engine</h5>
                        <br/>
                        {
                            uiStates.layout_engines && uiStates.layout_engines.map((option) => {
                                return (
                                    <div key={option.value} className="p-field-radiobutton">

                                        {(!_.isEmpty(uiStates.selected_layout_engine) &&
                                            <>
                                                <RadioButton inputId={option.value} name="layout_model" value={option} onChange={(e) => changeSelected(e.value)} checked={uiStates.selected_layout_engine[0].value === option.value} />
                                                <label htmlFor={option.value}>{option.name}</label>
                                            </>
                                        )}

                                        {(_.isEmpty(uiStates.selected_layout_engine) &&
                                            <>
                                                <RadioButton inputId={option.value} name="layout_model" value={option} onChange={(e) => changeSelected(e.value)} checked={selectedOption === option.value} />
                                                <label htmlFor={option.value}>{option.name}</label>
                                            </>
                                        )}

                                    </div>
                                )
                            })
                        }
                    </Card>
                </Col>
            </Row>

            <Row className="margin-top">
                <Col md={6} />
                <Col md="auto">
                    <Button onClick={handleSubmit} label="Next" />
                </Col>
            </Row>

            <Toast ref={toast} />
        </>
    );
};

export default DocumentLayoutAnalysis;
