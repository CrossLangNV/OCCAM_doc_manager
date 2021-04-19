import React, {useState} from 'react';
import {InputText} from "primereact/inputtext";
import {Card} from "primereact/card";
import {Button} from "primereact/button";
import {InputTextarea} from "primereact/inputtextarea";
import axios from "axios";
import {useHistory} from "react-router-dom";
import {FileUpload} from "primereact/fileupload";


const DocumentAdd = (props) => {

    const [title, setTitle] = useState("");
    const [content, setContent] = useState("");
    let history = useHistory();

    const ACCEPTED_FILE_TYPES = "image/*,application/pdf"

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
                label="Cancel"
                icon="pi pi-times"
                onClick={() => history.push("/")}
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
                <h5>Document information</h5>
                <br/>
                <span className="p-float-label">
                    <InputText
                        id="title"
                        value={title}
                        autoComplete={"off"}
                        onChange={(e) => setTitle(e.target.value)}/>
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

                <br/>
                <h5>Upload pages</h5>

                <div>
                    <FileUpload
                        name="demo[]"
                        url="./upload"
                        multiple
                        accept={ACCEPTED_FILE_TYPES}
                        maxFileSize="1000000"
                    />
                </div>


            </Card>

        </>
    );
};

export default DocumentAdd;
