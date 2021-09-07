import {useDispatch, useSelector} from "react-redux";
import _ from 'lodash';
import {DeleteDocument, GetDocumentList} from "../../actions/documentActions";
import React, {useState} from "react";
import {Link, useHistory} from "react-router-dom";
import {Col, Row, Table} from "react-bootstrap";
import ReactPaginate from "react-paginate"
import {Button} from "primereact/button";
import Moment from 'react-moment';
import {confirmPopup} from "primereact/confirmpopup";
import Tour from "reactour";
import {ChangeTutorialState, CloseTutorial} from "../../actions/authActions";
import DocumentPreview from "./DocumentPreview";
import {useTranslation} from "react-i18next";
import LanguageSelector from "../core/LanguageSelector";
import {InputSwitch} from "primereact/inputswitch";
import {ModifyDocumentQuery, ModifySelectedWebsite, ModifyShowDemoContent} from "../../actions/uiActions";
import {Dropdown} from "primereact/dropdown";
import {InputText} from "primereact/inputtext";


const DocumentList = () => {
    const dispatch = useDispatch();
    let history = useHistory();
    const {t} = useTranslation();

    // Redux states
    const documentList = useSelector(state => state.documentList);
    const uiStates = useSelector(state => state.uiStates);
    const auth = useSelector(state => state.auth)
    const [checkedDemoContent, setCheckedDemoContent] = useState(false);


    React.useEffect(() => {
        fetchDocuments(5, 1, uiStates.documentQuery, false);
    }, []);

    const fetchDocuments = (rows, page, query, showDemoContent) => {
        dispatch(GetDocumentList(rows, page, query, ""))
    }

    const confirmDeleteDoc = (event) => {
        confirmPopup({
            target: event.currentTarget,
            message: t("document-list.Are you sure you want to delete this document and all its pages?"),
            icon: 'pi pi-exclamation-triangle',
            accept: () => dispatch(DeleteDocument(event)),
        });
    }

    const searchDocuments = async (query) => {
        dispatch(ModifyDocumentQuery(query))
        dispatch(GetDocumentList(5, 1, query, uiStates.selectedWebsite))
    }

    const loadTableRows = () => {
        if (!_.isEmpty(documentList.data)) {
            return (
                <>
                    {documentList.data.map(item => {
                        return <tr key={item.id}>
                            <td className='w-10 occ-doc-list-td'>
                                <DocumentPreview document={item} />
                            </td>
                            <td className='w-50 occ-doc-list-td'><Link to={`/document/${item.id}`}>{item.name}</Link></td>
                            <td className="occ-doc-list-td">
                                <Moment format="DD/MM/YYYY H:mm" date={item.updated_at} />
                            </td>
                            <td className='w-10 occ-doc-list-td'>
                                <Moment format="DD/MM/YYYY H:mm" date={item.created_at} />
                            </td>
                            <td className='w-10 occ-doc-list-td'>
                                <Button
                                    onClick={() => confirmDeleteDoc(item.id)}
                                    label=""
                                    icon="pi pi-trash"
                                    className="p-button-danger"
                                />
                            </td>
                        </tr>
                    })}
                </>
            )
        }

        if (documentList.errorMsg !== "") {
            return <tr>
                <td>{documentList.errorMsg}</td>
            </tr>
        }
    }

    const steps = [
        {
            content: () => (
                <div>
                    <h3>{t("tour.welcome")}</h3>
                    <p>{t("tour.Let's take a quick tour on how to use the application")}</p>
                    <br/>
                    <LanguageSelector inline={true}/>
                    <br />
                    <Button label={t("tour.skip")} onClick={() => {
                        dispatch(ChangeTutorialState(auth.user, true))
                    }}/>
                </div>

            )
        },
        {
            selector: '.doc-list-step-two',
            content: () => (
                <div>
                    <h3>{t("tour.Document List")}</h3>
                    <p>{t("tour.This is a table with all your documents")}</p>
                    <p>{t("tour.At the first glance, it should look pretty empty")}</p>
                    <p>{t("tour.When you created documents, you can always navigate to them by clicking on the titles")}</p>
                    <p>{t("tour.The table is paginated, and a search button in the header allows you to search for documents")}</p>
                </div>
            )
        },
        {
            selector: '.doc-list-step-three',
            content: () => (
                <div>
                    <h3>{t("tour.Add new document")}</h3>
                    <p>{t("tour.By pressing this button you can create a new document")}</p>
                </div>
            )
        }
    ]

    return (
        <div className="doc-list-step-two">
            <Tour
                steps={steps}
                isOpen={!auth.hasCompletedTutorial}
                onRequestClose={() => dispatch(CloseTutorial())}
                className={"occ-tour-lg"}
            />

            <div>
                <br/>

                <Row>
                    <Col md={"auto"}>
                        <Button onClick={() => history.push("/document-add")}
                                label={t("document-list.New document")}
                                icon="pi pi-plus"
                                className="doc-list-step-three"
                        />
                    </Col>

                    <Col md={7}>
                        <div className="p-inputgroup">
                            <Button label="Search"/>
                            <InputText
                                placeholder={t("nav.search-document")}
                                value={uiStates.documentQuery}
                                onChange={(e) => {
                                    searchDocuments(e.target.value)
                                }}
                                onKeyPress={(e) => {
                                    if (e.key === "Enter") {
                                        e.preventDefault()
                                        searchDocuments(e.target.value)
                                    }
                                }}
                            />
                        </div>
                    </Col>

                    <Col md={3}>
                        <Dropdown options={uiStates.websites}
                                  placeholder="Website..."
                                  value={uiStates.selectedWebsite}
                                  optionValue="name"
                                  optionLabel="name"
                                  onChange={(e => {
                                      console.log(e)
                                      dispatch(ModifySelectedWebsite(e.value))
                                      dispatch(GetDocumentList(5, 1, uiStates.documentQuery, e.value))
                                  })}
                                  showClear={true}
                                  className="w-100"
                        />

                    </Col>
                    <Col md="mr-auto">
                        <p className="occ-table-result-count">{t("document-list.Document(s) found")} {documentList.count}</p>
                    </Col>
                </Row>
            </div>

            <br/>

            <Table striped borderless hover>
                <thead>
                <tr>
                    <th width="2rem">{t("ui.preview")}</th>
                    <th>{t("ui.title")}</th>
                    <th>{t("ui.last-updated")}</th>
                    <th>{t("ui.created-at")}</th>
                    <th>{t("ui.actions")}</th>
                </tr>
                </thead>
                <tbody>
                    {loadTableRows()}
                </tbody>
            </Table>

            {/* Pagination for the table */}
            {!_.isEmpty(documentList.data) && (
                <ReactPaginate
                    pageCount={Math.ceil(documentList.count / documentList.rows)}
                    pageRangeDisplayed={2}
                    pageMarginDisplayed={1}
                    onPageChange={(data) => fetchDocuments(documentList.rows, data.selected + 1, uiStates.documentQuery, uiStates.showDemoContent)}
                    containerClassName={"pagination"}
                    activeClassName={'active'}
                    breakClassName={'page-item'}
                />
            )}
        </div>
    )
};

export default DocumentList
