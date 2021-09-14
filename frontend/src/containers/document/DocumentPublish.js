import React, {useRef, useState} from 'react';
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
import {Tag} from "primereact/tag";
import {Toast} from "primereact/toast";

const DocumentPublish = (props) => {
    const documentId = props.match.params.documentId;
    const dispatch = useDispatch();
    const {t} = useTranslation();
    const [selectedPages, setSelectedPages] = useState([]);
    const [selectedMetadata, setSelectedMetadata] = useState([]);
    const toast = useRef(null);


    // Redux states
    const pageList = useSelector(state => state.pageList);
    const documentState = useSelector(state => state.document);

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
                    if (selectedMetadata.includes(e.value)) {
                        selectedMetadata.splice(i, 1);
                    }
                    break;
                }
            }
        }
        setSelectedPages(localSelectedPages);
    }

    const onMetadataSelection = async (e) => {
        let localSelectedMetadata = [...selectedMetadata]


        if (e.checked) {
            localSelectedMetadata.push(e.value);
            if (!selectedPages.includes(e.value)) {
                selectedPages.push(e.value);
            }
        } else {
            for (let i = 0; i < localSelectedMetadata.length; i++) {
                const selectedPage = localSelectedMetadata[i];

                if (selectedPage.id === e.value.id) {
                    localSelectedMetadata.splice(i, 1);
                    break;
                }
            }
        }
        setSelectedMetadata(localSelectedMetadata);
    }

    const onOverlaySelection = async (e) => {

    }

    const onPublishClick = async () => {
        dispatch(PublishDocument(documentId));
        toast.current.show({severity: 'success', summary: t("ui.success"), detail: t("oaipmh.uploaded")});

    }

    const onViewClick = (e) => {
        window.open(documentState.data[documentId].oaipmh_collection_url, '_blank');

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

                    <Row className="margin-top">
                        <Col>
                            <h3>Publish to OAI-PMH</h3>
                        </Col>
                    </Row>
                    <Row className="margin-top">
                        <Col md={1}>
                            Status:
                        </Col>
                        <Col md={3}>
                            <Tag value={documentData.oaipmh_collection_id ? "Published" : "Not published yet"}
                                 icon={documentData.oaipmh_collection_id ? "pi pi-check" : "pi pi-cross"}
                                 severity={documentData.oaipmh_collection_id ? "success" : "warning"}/>
                        </Col>
                    </Row>

                    {(documentData.oaipmh_collection_id) &&
                    <Row className="margin-top">
                        <Col md={1}>
                            UUID:
                        </Col>
                        <Col md={3}>
                            {documentData.oaipmh_collection_id}
                        </Col>
                    </Row>
                    }

                    <Row className="margin-top">
                        <Col>
                            <Button className="p-button-success" onClick={onPublishClick}>
                                {t("publish.Publish")}
                            </Button>
                            {(documentData.oaipmh_collection_url) &&
                            <Button className="p-button-info margin-left" onClick={onViewClick}>
                                {t("ui.view")}
                            </Button>
                            }
                        </Col>
                    </Row>

                    <br/>

                    <Row className="margin-top">
                        <Col>
                            <h3>Download results</h3>
                            <h5>Pages: ({pageList.count})</h5>
                        </Col>
                    </Row>
                    {!_.isEmpty(pageList.data) && (
                        <ScrollPanel className="occ-ui-publish-pages-list-scroll">
                            <Row className="flex-md-nowrap">
                                {pageList.data.map(page => {
                                    return <Col md={3} key={page.id}>
                                        <Card className="m-md-1" key={page.id}>
                                            <Row>
                                                <Image
                                                    className={selectedPages.some((item) => item.id === page.id) ? "page-card-img selectedForDownload" : "page-card-img"}
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
                                                              value={page}
                                                              onChange={onMetadataSelection}
                                                              checked={selectedMetadata.some((item) => item.id === page.id)}/>
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

                    <Toast ref={toast}/>
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
