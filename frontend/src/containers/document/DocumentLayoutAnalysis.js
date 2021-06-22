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

const DocumentLayoutAnalysis = (props) => {
    const documentId = props.match.params.documentId
    let history = useHistory();
    const toast = useRef(null);

    const config = {
        headers: {
            'Authorization': `Bearer ${localStorage.getItem("access")}`
        }
    }

    const [options, setOptions] = useState([{name: "None", value: "None"}]);

    useEffect(() => {
        fetchLayoutModels()
    }, [])

    const fetchLayoutModels = async () => {
        if (documentId !== undefined) {
            await axios.get(`${baseUrl}/documents/api/layout_analysis_models`, config).then((res) => {
                let models = []
                res.data.forEach(model => {
                    models.push({name: model.name, value: model.name, id: model.id})
                })
                models.push({name: 'None', value: 'None'})
                setOptions(models)
            }).catch((reason => {
                toast.current.show({severity: 'danger', summary: 'Failed', detail: 'Failed to load layout analysis models'});
            }))
        }
    }

    const [selectedOption, setSelectedOption] = useState(options[0]);

    const handleSubmit = async (evt) => {
        evt.preventDefault();

        if (selectedOption.value !== "None") {
            const data = {
                layout_analysis_model: selectedOption.id,
            }

            if (selectedOption.value !== "") {
                await axios.put(`${baseUrl}/documents/api/document/${documentId}`, data, config
                ).then((res) => {
                    history.push(`/document/${documentId}`)
                });
            }
        } else {
            history.push(`/document/${documentId}`)
        }

    }

    return (
        <>
            <Row>
                <ProgressBar activeStep={3} documentId={documentId}/>
            </Row>

            <Row className="margin-top">
                <Col md={3}></Col>
                <Col md={6}>
                    <Card>
                        <h5>Choose a layout analysis engine</h5>
                        <br/>
                        {
                            options && options.map((option) => {
                                return (
                                    <div key={option.value} className="p-field-radiobutton">
                                        <RadioButton inputId={option.value} name="layout_model" value={option} onChange={(e) => setSelectedOption(e.value)} checked={selectedOption.value === option.value} />
                                        <label htmlFor={option.value}>{option.name}</label>
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
