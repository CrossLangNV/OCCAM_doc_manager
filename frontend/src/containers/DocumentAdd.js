import React, {useState} from 'react';
import {InputText} from "primereact/inputtext";
import {Card} from "primereact/card";
import {Button} from "primereact/button";
import {InputTextarea} from "primereact/inputtextarea";
import axios from "axios";
import {Link, useHistory} from "react-router-dom";


const DocumentAdd = (props) => {

    const [title, setTitle] = useState("");
    const [content, setContent] = useState("");
    let history = useHistory();

    const handleSubmit = (evt) => {
        evt.preventDefault();
        addDocument(title, content).then(r => {
            setTitle("");
            setContent("");
            history.push("/")
        })
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
                as={Link}
                to="/"
                label="Cancel"
                icon="pi pi-times"
                className="p-button-secondary"/>
        </span>;

    const addDocument = async (title, content) => {
        if (title !== "") {
            const res = await axios.post(`http://localhost:8000/documents/api/documents/`,
                {
                    name: title,
                    content: content,
                    state: 'New'
                }).then((res) => {
                console.log(res);

            });
        }

    }

    return (
        <>
            <h3>Add new document</h3>
            <br/>

            <Card footer={footer}>
                <span className="p-float-label">
                    <InputText
                        id="title"
                        value={title}
                        onChange={(e) => setTitle(e.target.value)} />
                    <label htmlFor="title">Title</label>
                </span>

                <br/><br/>

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
