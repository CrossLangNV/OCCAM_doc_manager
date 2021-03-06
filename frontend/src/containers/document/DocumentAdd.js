import React, {useEffect, useRef, useState} from 'react';
import {InputText} from "primereact/inputtext";
import {Card} from "primereact/card";
import {Button} from "primereact/button";
import {InputTextarea} from "primereact/inputtextarea";
import axios from "axios";
import {useHistory} from "react-router-dom";
import {useDispatch, useSelector} from "react-redux";
import {baseUrl} from "../../constants/axiosConf";
import ProgressBar from "../ProgressBar";
import {Col, Row} from "react-bootstrap";
import {Toast} from "primereact/toast";
import Tour from "reactour";
import {ChangeTutorialState, CloseTutorial} from "../../actions/authActions";
import {useTranslation} from "react-i18next";
import {RadioButton} from "primereact/radiobutton";
import {Message} from "primereact/message";
import {load} from "cheerio";
import {AddPage} from "../../actions/pageActions";


const DocumentAdd = (props) => {
    const documentId = props.match.params.documentId

    // Enable/disable Europeana functionality
    const EUROPEANA_ENABLED = false;

    let history = useHistory();
    const dispatch = useDispatch();
    const {t} = useTranslation();

    // Redux states
    const uiStates = useSelector(state => state.uiStates);
    const auth = useSelector(state => state.auth);

    const [websiteId, setWebsiteId] = useState(0);
    const [title, setTitle] = useState("");
        const [content, setContent] = useState("");

        const europeanaBaseUrl = "https://www.europeana.eu/en/item/";
        const [europeanaItemId, setEuropeanaItemId] = useState("");
        const [europeanaData, setEuropeanaData] = useState({title: "", imageUrl: "", thumbUrl: ""});

        const toast = useRef(null);

        const config = {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem("access")}`
            }
        }

        // Change the fields to the current values
        useEffect(() => {

            if (documentId !== undefined) {
                axios.get(`${baseUrl}/documents/api/document/${documentId}`, config).then((res) => {
                    setTitle(res.data.name);
                    setContent(res.data.content);
                    setWebsiteId(res.data.website);
                    setEuropeanaItemId(res.data.europeana_item_id);
                    fetchEuropeanaItem(res.data.europeana_item_id);
                }).catch((err => {
                    history.push("/");
                    console.log(err);
                }))
            }

        }, [])


        const handleSubmit = async (evt) => {
            evt.preventDefault();

            if (!documentId) {
                await addDocument()
            } else {
                await editDocument()
            }
        }

        const addDocument = async () => {
            const data = {
                name: title,
                content: content,
                state: 'New',
                user: auth.user,
                website: websiteId === 0 ? null : websiteId,
                europeana_item_id: europeanaItemId
            }

            if (title !== "") {
                if (websiteId === 5) {
                    await axios.post(`${baseUrl}/documents/api/documents`, data, config
                    ).then((res) => {
                        addEuropeanaPage(res.data.id, europeanaData.imageUrl);
                        history.push(`/document-edit/${res.data.id}/layout_model`);
                    });

                } else {
                    await axios.post(`${baseUrl}/documents/api/documents`, data, config
                    ).then((res) => {
                        history.push(`/document/${res.data.id}/add-pages`);
                    });
                }
            }

        }

        const editDocument = async () => {
            const data = {
                name: title,
                content: content,
            }

            if (title !== "") {
                await axios.put(`${baseUrl}/documents/api/document/${documentId}`, data, config
                ).then((res) => {
                    toast.current.show({
                        severity: 'success',
                        summary: t("ui.success"),
                        detail: t("document-add.Document information saved.")
                    });
                });
            }
        }

        const footer =
            <span>
            <Button
                label={t("ui.cancel")}
                icon="pi pi-times"
                onClick={() => history.push("/")}
                className="p-button-secondary"/>
        </span>;

        const steps = [
            {
                selector: '.add-doc-step-one',
                content: () => (
                    <div>
                        <h3>{t("document-add.Document Title")}</h3>
                        <p>{t("document-add.A document is a collection of pages/images")}</p>
                        <p>{t("document-add.Here you can fill in a title for your new document")}</p>
                        <br/>
                        <Button label={t("tour.skip")} onClick={() => {
                            dispatch(ChangeTutorialState(auth.user, true))
                        }}/>
                    </div>
                )
            },
            {
                selector: '.add-doc-step-two',
                content: () => (
                    <div>
                        <h3>{t("document-add.Summary")}</h3>
                        <p>
                            <b>{t("document-add.Optional")}</b>: {t("document-add.A summary of your document, for your own reference")}
                        </p>
                    </div>
                )
            },
            {
                selector: '.doc-list-step-five',
                content: () => (
                    <div>
                        <h3>{t("document-add.Next button")}</h3>
                        <p>
                            {t("document-add.When you have filled in the information of your document, you can press this button to proceed to the next step")}
                        </p>
                    </div>
                )
            }
        ]

        const changeDocumentWebsite = (e) => {
            setWebsiteId(e);
        }

        const fetchEuropeanaItem = async (itemId) => {
            await axios.get(europeanaBaseUrl + itemId).then(response => {
                console.log(response.data)
                const $ = load(response.data);
                const title = $('h1').text();
                const imageUrl = $('div.item-hero a').attr('href');
                const thumbUrl = $('div.item-hero img').attr('src');
                setEuropeanaData({title: title, imageUrl: imageUrl, thumbUrl: thumbUrl});
                setTitle(title);
            });
        }

        const addEuropeanaPage = async (documentId, imageUrl) => {
            let files = []
            await axios.get(imageUrl, {responseType: 'blob'}).then(response => {
                files.push(new File([response.data], title + '.jpg'));
            });

            await dispatch(AddPage(documentId, files));
        }

        return (
            <>
                <Tour
                    steps={steps}
                    isOpen={!auth.hasCompletedTutorial}
                    onRequestClose={() => dispatch(CloseTutorial())}
                />

                <Row className="doc-list-step-four">
                    <ProgressBar activeStep={1} documentId={documentId}/>
                </Row>

                <Row className="margin-top">
                    <Col md={5}/>
                    <Col md={6}>
                        <h3>{t("document-add.Add new document")}</h3>
                    </Col>

                </Row>

                {(documentId === undefined) && (
                    <Row className="margin-top">
                        <Col md={3}/>
                        <Col md={6}>
                            <Card>
                                <div key="manual" className="p-field-radiobutton">
                                    <RadioButton inputId="manual" name="documentType" value="0"
                                                 onChange={(e) => changeDocumentWebsite(parseInt(e.value))}
                                                 checked={websiteId === 0}/>
                                    <Col md={4}>
                                        <label htmlFor="manual">{t("document-add.Manual")}</label>
                                    </Col>
                                    <Col md={8}>
                                        {(websiteId === 0) && (
                                            <Message className="margin-left" severity="info"
                                                     text={t("document-add.Manual")}/>
                                        )}
                                    </Col>
                                </div>
                                {(EUROPEANA_ENABLED) && (
                                    <div key="europeana" className="p-field-radiobutton">
                                        <RadioButton inputId="europeana" name="documentType" value="5"
                                                     onChange={(e) => changeDocumentWebsite(parseInt(e.value))}
                                                     checked={websiteId === 5}
                                        />
                                        <Col md={4}>
                                            <label htmlFor="europeana">{t("document-add.Europeana")}</label>
                                        </Col>
                                        <Col md={8}>
                                            {(websiteId === 5) && (
                                                <Message className="margin-left" severity="info"
                                                         text={t("document-add.Europeana")}/>
                                            )}
                                        </Col>
                                    </div>
                                )}
                            </Card>
                        </Col>
                    </Row>
                )}

                <Row className="margin-top">
                    <Col md={3}/>
                    <Col md={6}>
                        {((websiteId === 0) || (websiteId === null && documentId !== undefined)) && (
                            <Card footer={footer}>
                                <h5>{t("document-add.Document information")}</h5>
                                <br/>
                                <span className="p-float-label add-doc-step-one">
                            <InputText
                                id="title"
                                value={title}
                                autoComplete={"off"}
                                onChange={(e) => setTitle(e.target.value)}
                                autoFocus={true}
                                className='occ-full-width'
                            />
                            <label htmlFor="title">{t("ui.title")}</label>
                            </span>

                                <br/>

                                <span className="p-float-label">
                                <InputTextarea
                                    id="content"
                                    value={content}
                                    rows={5}
                                    cols={30}
                                    onChange={(e) => setContent(e.target.value)}
                                    className='occ-full-width occ-summary-field add-doc-step-two'
                                />
                                <label htmlFor="content">{t("ui.summary")}</label>
                            </span>
                            </Card>
                        )}
                        {(websiteId === 5) && (
                            <Card footer={footer}>
                                <h5>{t("document-add.Document information")}</h5>
                                <br/>
                                <span className="p-float-label add-doc-step-one">
                                <div className="p-inputgroup">
                                    <span className="p-inputgroup-addon">{europeanaBaseUrl}</span>
                                    <InputText
                                        id="europeanaItemId"
                                        value={europeanaItemId}
                                        autoComplete={"off"}
                                        onChange={(e) => {
                                            setEuropeanaItemId(e.target.value);
                                            fetchEuropeanaItem(e.target.value);
                                        }}
                                        autoFocus={true}
                                    />
                                </div>
                                <div className="margin-top">
                                    <h6>{t("ui.preview")}</h6>
                                    {(europeanaData.title) && (
                                        <div>{europeanaData.title}</div>
                                    )}
                                    {(europeanaData.thumbUrl) && (
                                        <div className="margin-top-lesser">
                                            <img src={europeanaData.thumbUrl}/>
                                        </div>
                                    )}
                                </div>
                                </span>
                            </Card>
                        )}

                    </Col>
                </Row>

                <Row>
                    <Col md={3}/>
                    <Col md={6}>
                        <div className='occ-center'>
                            <Button onClick={handleSubmit}
                                    label={documentId !== undefined ? "Save" : "Next"}
                                    style={{marginRight: '.25em'}}
                                    disabled={!title}
                                    className="margin-top doc-list-step-five"
                            />
                        </div>
                    </Col>


                </Row>

                <Toast ref={toast}/>

            </>
        );
    }
;

export default DocumentAdd;
