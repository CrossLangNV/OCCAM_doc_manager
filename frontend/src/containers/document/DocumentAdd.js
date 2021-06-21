import React, {useState} from 'react';
import {InputText} from "primereact/inputtext";
import {Card} from "primereact/card";
import {Button} from "primereact/button";
import {InputTextarea} from "primereact/inputtextarea";
import axios from "axios";
import {useHistory} from "react-router-dom";
import {useSelector} from "react-redux";
import {baseUrl} from "../../constants/axiosConf";
import ProgressBar from "../ProgressBar";
import {Col, Row} from "react-bootstrap";


const DocumentAdd = (props) => {
    let history = useHistory();
    const auth = useSelector(state => state.auth);

    const [title, setTitle] = useState("");
    const [content, setContent] = useState("");

    const handleSubmit = async (evt) => {
        evt.preventDefault();

        const data = {
            name: title,
            content: content,
            state: 'New',
            user: auth.user
        }

        const config = {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem("access")}`
            }
        }

        if (title !== "") {
            await axios.post(`${baseUrl}/documents/api/documents`, data, config

            ).then((res) => {
                    history.push('/document/' + res.data.id + "/add-pages")
            });
        }
    }

    const footer =
        <span>
            <Button
                label="Cancel"
                icon="pi pi-times"
                onClick={() => history.push("/")}
                className="p-button-secondary"/>
        </span>;

    return (
        <>
            <Row>
                <ProgressBar activeStep={1}/>
            </Row>

            <Row className="margin-top">
                <Col md={5}></Col>
                <Col md={6}>
                    <h3>Add new document</h3>
                </Col>

            </Row>

            <Row className="margin-top">
                <Col md={3}></Col>
                <Col md={6}>
                    <Card footer={footer}>
                        <h5>Document information</h5>
                        <br/>
                        <span className="p-float-label">
                            <InputText
                                id="title"
                                value={title}
                                autoComplete={"off"}
                                onChange={(e) => setTitle(e.target.value)}
                                autoFocus={true}
                                className='occ-full-width'
                            />
                            <label htmlFor="title">Title</label>
                        </span>

                        <br/>

                        <span className="p-float-label">
                    <InputTextarea
                        id="content"
                        value={content}
                        rows={5}
                        cols={30}
                        onChange={(e) => setContent(e.target.value)}
                        className='occ-full-width occ-summary-field'
                    />
                    <label htmlFor="content">Content</label>
                </span>
                    </Card>
                </Col>
            </Row>

            <Row className="margin-top">
                <Col md={3}></Col>
                <Col md={6}>
                    <div className='occ-center'>
                        <Button onClick={handleSubmit}
                                label="Next"
                                style={{marginRight: '.25em'}}
                                disabled={!title}
                        />
                    </div>
                </Col>



            </Row>


        </>
    );
};

export default DocumentAdd;
