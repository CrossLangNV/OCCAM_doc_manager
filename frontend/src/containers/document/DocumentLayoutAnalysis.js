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
import Tour from "reactour";
import {ChangeTutorialState, CloseTutorial} from "../../actions/authActions";
import {useTranslation} from "react-i18next";

const DocumentLayoutAnalysis = (props) => {
    const documentId = props.match.params.documentId
    let history = useHistory();
    const toast = useRef(null);
    const dispatch = useDispatch();
    const {t} = useTranslation();

    const uiStates = useSelector(state => state.uiStates);
    const auth = useSelector(state => state.auth);

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

    const steps = [
        {
            selector: '.document-layout-step-one',
            content: () => (
                <div>
                    <h3>{t("layout.Layout Analysis Engine")}</h3>
                    <p>{t("layout.In this step you can select which model you wish to use for the layout analysis (OCR)")} </p>
                    <p>
                        {t("layout.Depending on your documents and the selected engine, the layout analysis results might be different")}
                    </p>
                    <br/>
                    <Button label={t("ui.dont-show-me-again")} onClick={() => {
                        dispatch(ChangeTutorialState(auth.user, true))
                    }}/>
                </div>
            )
        }
    ]

    return (
        <>
            <Tour
                steps={steps}
                isOpen={!auth.hasCompletedTutorial}
                onRequestClose={() => dispatch(CloseTutorial())}
            />

            <Row>
                <ProgressBar activeStep={3} documentId={documentId}/>
            </Row>

            <Row className="margin-top">
                <Col md={3}/>
                <Col md={6}>
                    <Card className="document-layout-step-one">
                        <h5>{t("ui.ocr")}</h5>
                        <br/>
                        {
                            uiStates.layout_engines && uiStates.layout_engines.map((option) => {
                                return (
                                    <div key={option.name} className="p-field-radiobutton">

                                        {(!_.isEmpty(uiStates.selected_layout_engine) &&
                                            <>
                                                <RadioButton inputId={option.value} name="layout_model" value={option} onChange={(e) => changeSelected(e.value)} checked={uiStates.selected_layout_engine[0].name === option.name} />
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
                    <Button onClick={handleSubmit} label={t("ui.next")} />
                </Col>
            </Row>

            <Toast ref={toast} />
        </>
    );
};

export default DocumentLayoutAnalysis;
