import {useDispatch, useSelector} from "react-redux";
import {DeleteDocument, GetDocument} from "../actions/documentActions";
import React from "react";
import _ from "lodash"
import {FileUpload} from "primereact/fileupload";
import {Card} from "primereact/card";
import {Button} from "primereact/button";
import {confirmPopup} from "primereact/confirmpopup";
import {Col, Row} from "react-bootstrap";
import {useHistory} from "react-router-dom";
import Moment from "react-moment";

const Document = (props) => {
    const ACCEPTED_FILE_TYPES = "image/*,application/pdf"

    const documentId = props.match.params.documentId
    const dispatch = useDispatch()
    const documentState = useSelector(state => state.document)

    let history = useHistory();

    React.useEffect(() => {
        dispatch(GetDocument(documentId))
    }, [])

    const pagesUploader = (event) => {
        const files = event.files
        console.log(files)
    }

    const confirmDeleteDoc = (event) => {
        confirmPopup({
            target: event.currentTarget,
            message: 'Are you sure you want to proceed?',
            icon: 'pi pi-exclamation-triangle',
            accept: () =>
            {
                dispatch(DeleteDocument(event))
                history.push("/")
            },
        });
    }

    const showData = () => {
        if (!_.isEmpty(documentState.data[documentId])) {

            const documentData = documentState.data[documentId]
            return(
                <div>
                    <Row>
                        <Col sm={11}>
                            <h1>{documentData.name}</h1>
                        </Col>
                        <Col>
                            <Button
                                onClick={() => confirmDeleteDoc(documentId)}
                                label=""
                                icon="pi pi-trash"
                                className="p-button-danger"
                            />
                        </Col>
                    </Row>

                    <p><b>Content: </b> {documentData.content}</p>
                    <p><b>State:</b> {documentData.state}</p>
                    <p><b>Created at:</b> <Moment format="DD/MM/YYYY H:mm" date={documentData.created_at} /></p>

                    <br/>
                    {!_.isEmpty(documentData.document_page) && (
                        <div>
                            <h5>Pages</h5>

                            {documentData.document_page}

                            <br/><br/>
                        </div>

                    )}

                    <h5>Upload pages</h5>

                    <div>
                        <FileUpload
                            name="demo[]"
                            url="./upload"
                            multiple
                            accept={ACCEPTED_FILE_TYPES}
                            maxFileSize={1000000}
                            customUpload
                            uploadHandler={pagesUploader}
                        />
                    </div>
                </div>
            )
        }

        if (documentState.loading) {
            return <p>Loading...</p>
        }

        if (documentState.errorMsg !== "") {
            return <p>{documentState.errorMsg}</p>
        }

        return <p>Error fetching document</p>

    }

    return (
        <div>
            {showData()}
        </div>
    )
}
export default Document
