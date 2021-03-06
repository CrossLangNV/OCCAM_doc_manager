import React, {useRef, useState} from 'react';
import {useDispatch, useSelector} from "react-redux";
import _ from "lodash";
import { FileUpload } from 'primereact/fileupload';
import { GetTmStats, UploadTMX } from '../actions/tmActions';
import { Toast } from 'primereact/toast';
import {Button} from "primereact/button";
import {Col, Row, Table} from "react-bootstrap";
import {ChangeTutorialState} from "../actions/authActions";
import {InputSwitch} from "primereact/inputswitch";
import LanguageSelector from "./core/LanguageSelector";
import {useTranslation} from "react-i18next";
import ReactPaginate from "react-paginate";
import LoadingSpinner from "./core/LoadingSpinner";

const Settings = () => {
    // Redux
    const dispatch = useDispatch();
    const tmStats = useSelector(state => state.tmStats);
    const auth = useSelector(state => state.auth);
    const hasCompletedTutorial = auth.hasCompletedTutorial;
    const {t} = useTranslation();

    const toast = useRef(null);
    const uploadRef = useRef(null);
    const [checkedTutorial, setCheckedTutorial] = useState(false);

    const [currentPage, setCurrentPage] = useState(0);
    const [perPage] = useState(5);


    React.useEffect(() => {
        fetchTmStats();
        if (hasCompletedTutorial === false) {
            setCheckedTutorial(true)
        } else {
            setCheckedTutorial(false)
        }
    }, [hasCompletedTutorial]);

    const fetchTmStats = () => {
        dispatch(GetTmStats());
    }

    const offset = currentPage * perPage;
    const paginatedTmStats = tmStats.data.slice(offset, offset + perPage)
    const pageCount = Math.ceil(tmStats.data.length / perPage);

    const tmxUploader = async (event) => {
        const files = event.files

        if (files) {
            dispatch(UploadTMX(files[0]));
            toast.current.show({ severity: 'success', summary: 'Success', detail: 'TMX file has been uploaded.' });
            uploadRef.current.clear();
        }
    }

    const loadTableRows = () => {
        if (!_.isEmpty(paginatedTmStats)) {
            return (
                paginatedTmStats.map(d => (
                    <tr>
                        <td className='w-10'>{d['langpair']}</td>
                        <td>{d['amount']}</td>
                    </tr>
                ))
            )
        }
    }

    function handlePageClick({ selected: selectedPage}) {
        setCurrentPage(selectedPage);
        loadTableRows();
    }


    const showTranslationMemoryTable = () => {
        return (
            <div>
                <h2>{t("settings.translation-memory")}</h2>
                <Row className="justify-content-between">
                    <Col>
                        <Button
                            onClick={() => fetchTmStats()}
                            label=""
                            icon="pi pi-refresh"
                            className="p-button-primary margin-left"
                            tooltip={t("ui.refresh")}
                            tooltipOptions={{ position: 'bottom' }}
                        />
                    </Col>
                </Row>
                <Table striped borderless hover>
                    <thead>
                        <tr>
                            <th>{t("settings.language-pair")}</th>
                            <th>{t("settings.amount-of-tus")}</th>
                        </tr>
                    </thead>
                    <tbody>
                        {tmStats.loading && (
                            <div>
                                <LoadingSpinner />
                                <span className="margin-left">
                                    {t("ui.loading")}...
                                </span>
                            </div>
                        )}
                        {loadTableRows()}
                    </tbody>
                </Table>
                {/* Pagination for the table */}
                {!_.isEmpty(paginatedTmStats) && (
                    <ReactPaginate
                        pageCount={pageCount}
                        pageRangeDisplayed={2}
                        pageMarginDisplayed={1}
                        onPageChange={handlePageClick}
                        containerClassName={"pagination"}
                        activeClassName={'active'}
                        breakClassName={'page-item'}
                    />
                )}
                <br/>
                <FileUpload
                    ref={uploadRef}
                    name="tmx"
                    maxFileSize={10000000}
                    accept={".tmx"}
                    mode="basic"
                    auto={true}
                    customUpload
                    uploadHandler={tmxUploader}
                    chooseLabel={t("settings.upload-tmx")}
                />
            </div>
        );
    }

    const showProductTourSetting = () => {
        return (
            <>
                <h2 className="margin-top">{t("settings.product-tour")}</h2>

                <div className="p-field-checkbox">
                    <InputSwitch inputId="enableTutorial" checked={checkedTutorial} onChange={e => {
                        setCheckedTutorial(e.value)
                        dispatch(ChangeTutorialState(auth.user, !e.value))
                    }} />
                    <label htmlFor="enableTutorial">{t("settings.show-product-tour")}</label>
                </div>
            </>
        )
    }

    const showLanguageSetting = () => {
        return (
            <>
                <h2 className="margin-top">{t("settings.language")}</h2>
                <LanguageSelector inline={false}/>
            </>
        )
    }

    return (
        <div>
            {showTranslationMemoryTable()}

            {showProductTourSetting()}

            {showLanguageSetting()}

            <Toast ref={toast} />
        </div>
    )
};

export default Settings;
