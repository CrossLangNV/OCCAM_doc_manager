import React, {useState} from 'react';
import {InputText} from "primereact/inputtext";
import {Card} from "primereact/card";
import {Button} from "primereact/button";
import {InputTextarea} from "primereact/inputtextarea";
import axios from "axios";
import {useHistory} from "react-router-dom";


const DocumentAdd = (props) => {
    let history = useHistory();

    const [title, setTitle] = useState("");
    const [content, setContent] = useState("");

    const handleSubmit = async (evt) => {
        evt.preventDefault();

        const baseUrl = process.env.REACT_APP_API_URL

        const data = {
            name: title,
            content: content,
            state: 'New'
        }

        const config = {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem("access")}`
            }
        }

        if (title !== "") {
            await axios.post(`${baseUrl}/documents/api/documents`, data, config

            ).then((res) => {
                    history.push('/document/' + res.data.id + "/")
            });
        }
    }

    const footer =
        <span>
            <Button onClick={handleSubmit}
                    label="Save"
                    icon="pi pi-check"
                    style={{marginRight: '.25em'}}
                    disabled={!title}
            />
            <Button
                label="Cancel"
                icon="pi pi-times"
                onClick={() => history.push("/")}
                className="p-button-secondary"/>
        </span>;

    return (
        <>
            <h3>Add new document</h3>
            <br/>

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
                    />
                    <label htmlFor="content">Content</label>
                </span>
            </Card>
        </>
    );
};

export default DocumentAdd;
