import React, {useState} from 'react';
import ProgressBar from "../ProgressBar";
import {Col, Image, Row} from "react-bootstrap";
import {useTranslation} from "react-i18next";
import {Button} from "primereact/button";
import {baseUrl} from "../../constants/axiosConf";
import {useDispatch, useSelector} from "react-redux";
import {GetDocument, PublishDocument} from "../../actions/documentActions";
import _ from "lodash";
import {GetPageList} from "../../actions/pageActions";
import {ScrollPanel} from "primereact/scrollpanel";
import {Card} from "primereact/card";
import NotSelectedMessage from "../NotSelectedMessage";
import {Checkbox} from "primereact/checkbox";
import DocumentPublishOverlay from "./DocumentPublishOverlay";
import DocumentPublishTranslation from "./DocumentPublishTranslation";
import axios from "axios";

const DocumentPublish = (props) => {
    const documentId = props.match.params.documentId;
    const dispatch = useDispatch();
    const {t} = useTranslation();

    // Redux states
    const pageList = useSelector(state => state.pageList);
    const uiStates = useSelector(state => state.uiStates);
    const auth = useSelector(state => state.auth);
    const documentState = useSelector(state => state.document);
    const documentPublishState = useSelector(state => state.documentPublish);

    const [selectedPages, setSelectedPages] = useState([]);

    const config = {
        headers: {
            'Authorization': `Bearer ${localStorage.getItem("access")}`
        }
    }

    React.useEffect(() => {
        dispatch(GetDocument(documentId));
        dispatch(GetPageList(100, 0, documentId));
    }, [])

    // UI
    const linkStyle = {
        color: 'inherit',
        textDecoration: 'inherit'
    };

    const onPageImageClick = async (pageFile) => {
        console.log("Clicked on: " + pageFile)
    }

    const onPageSelection = async (e) => {
        let localSelectedPages = [...selectedPages];

        if (e.checked) {
            localSelectedPages.push(e.value);
        } else {
            for (let i = 0; i < localSelectedPages.length; i++) {
                const selectedPage = localSelectedPages[i];

                if (selectedPage.id === e.value.id) {
                    localSelectedPages.splice(i, 1);
                    break;
                }
            }
        }
        setSelectedPages(localSelectedPages);
    }

    const onMetadataSelection = async (e) => {

    }

    const onOverlaySelection = async (e) => {

    }

    const onPublishClick = async () => {
        // await axios.get(`${baseUrl}/documents/api/publish?document=${documentId}`, config).then(res => {
        //         console.log('Document published to OAI-PMH server')
        //     }
        // )
        dispatch(PublishDocument(documentId));
    }

    const showData = () => {
        if (!_.isEmpty(documentState.data[documentId])) {

            const documentData = documentState.data[documentId];

            return (
                <>
                    <Row className="justify-content-between">
                        <Col md={3}>
                            <h2>{documentData.name}</h2>
                        </Col>
                        <Col md={9}>
                            <ProgressBar activeStep={5} documentId={documentId}/>
                        </Col>
                    </Row>

                    <h5>Pages ({pageList.count})</h5>
                    <Row className="margin-top">
                        <Col>
                            <h3>Download results</h3>
                        </Col>
                    </Row>
                    {!_.isEmpty(pageList.data) && (
                        <ScrollPanel className="occ-ui-publish-pages-list-scroll">
                            <Row className="flex-md-nowrap">
                                {pageList.data.map(page => {
                                    return <Col md={3}>
                                        <Card className="m-md-1" key={page.id}>
                                            <Row>
                                                <Image
                                                    className="page-card-img"
                                                    src={page.file}
                                                    onClick={e => onPageImageClick(page.file)}
                                                />
                                            </Row>
                                            <Row>
                                                <div className="p-field-checkbox m-md-1">
                                                    <Checkbox inputId={page.id} name="page" value={page}
                                                              onChange={onPageSelection}
                                                              checked={selectedPages.some((item) => item.id === page.id)}/>
                                                    <label className="m-md-2"
                                                           htmlFor={page.id}>{page.metadata.titles[0].split('/')[1]}</label>
                                                </div>
                                            </Row>
                                            <Row>
                                                <div className="p-field-checkbox m-md-1">
                                                    <Checkbox inputId={page.id + "/metadata"} name="metadata"
                                                              value={page.id}/>
                                                    <label className="m-md-2"
                                                           htmlFor={page.id + "/metadata"}>Metadata</label>
                                                </div>
                                            </Row>
                                            <Row>
                                                <DocumentPublishOverlay page={page}/>
                                            </Row>
                                            <Row>
                                                <DocumentPublishTranslation page={page}/>
                                            </Row>
                                        </Card>
                                    </Col>
                                })}
                            </Row>

                        </ScrollPanel>
                    )}

                    <NotSelectedMessage context={pageList.data}
                                        message={t("page-list.No pages are uploaded yet")}/>

                    <Row>
                        <Col>
                            <Button>
                                <a style={linkStyle}
                                   href={`${baseUrl}/documents/api/export/metadata?document=${documentId}`}>{t("publish.Download")}</a>
                            </Button>
                        </Col>
                    </Row>
                    <hr/>
                    <Row className="margin-top">
                        <Col>
                            <Button className="p-button-success" onClick={onPublishClick}>
                                {t("publish.Publish")}
                            </Button>
                        </Col>
                    </Row>
                </>
            );
        }
        if (documentState.loading) {
            return <p>{t("ui.loading")}...</p>
        }

        if (documentState.errorMsg !== "") {
            return <p>{documentState.errorMsg}</p>
        }

        return <p>{t("document.Error fetching document")}</p>
    }

    return (
        <div>
            {showData()}
        </div>
    )
};

export default DocumentPublish;
