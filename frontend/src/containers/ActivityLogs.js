import React from 'react';
import {useDispatch, useSelector} from "react-redux";
import {GetActivityList} from "../actions/acitvityActions";
import _ from "lodash";
import {useHistory} from "react-router-dom";
import DocumentState from "./document/DocumentState";
import Moment from "react-moment";
import {Button} from "primereact/button";
import {Col, Row, Table} from "react-bootstrap";
import ReactPagiate from "react-paginate";
import LoadingSpinner from "./core/LoadingSpinner";
import {useTranslation} from "react-i18next";

const ActivityLogs = () => {
    const dispatch = useDispatch();
    const history = useHistory();
    const activityList = useSelector(state => state.activityLogsList);
    const {t} = useTranslation();

    React.useEffect(() => {
        fetchActivityLogs(5, 1);
    }, []);

    const fetchActivityLogs = (rows, page) => {
        dispatch(GetActivityList(rows, page, "", "", "", false))
    }

    const loadTableRows = () => {
        if (!_.isEmpty(activityList.data)) {
            return (
                <>
                    {activityList.data.map(item => {
                        return <tr key={item.id}>
                            <td className='w-10'>
                                {item.id}
                            </td>
                            <td>
                                {item.type}
                            </td>
                            <td>
                                <DocumentState state={item.state} />

                                {((item.state === "Processing" || item.state === "Waiting") &&
                                    <LoadingSpinner/>
                                )}
                            </td>
                            <td>
                                {(!_.isEmpty(item.page) &&
                                    <>
                                        {item.page.file.split('pages/')[1]}
                                    </>
                                )}
                            </td>
                            <td>
                                {(!_.isEmpty(item.overlay) &&
                                    <>
                                        {item.overlay.file.split('pages/')[1]}
                                    </>
                                )}
                            </td>
                            <td className='w-10'>
                                <Moment format="DD/MM/YYYY H:mm" date={item.created_at}/>
                            </td>
                            <td className='w-10'>
                                <Moment format="DD/MM/YYYY H:mm" date={item.updated_at}/>
                            </td>
                            <td className='w-10'>
                                <Button
                                    label=""
                                    tooltip={t("activity-logs.View document")}
                                    tooltipOptions={{position: 'bottom'}}
                                    icon="pi pi-search"
                                    onClick={() => history.push(`/document/${!_.isEmpty(item.page) ? item.page.document.id : item.overlay.page.document}`)}

                                    className="p-button-secondary"/>
                            </td>
                        </tr>
                    })}
                </>
            )
        }

        if (activityList.loading) {
            return <p>{t("ui.loading")}...</p>
        }

        if (activityList.errorMsg !== "") {
            return <p>{activityList.errorMsg}</p>
        }
    }


    return (
        <div>

            <Row className="justify-content-between">
                <Col>
                    <Button
                        onClick={() => fetchActivityLogs(5, 1)}
                        label=""
                        icon="pi pi-refresh"
                        className="p-button-primary margin-left"
                        tooltip={t("ui.refresh")}
                        tooltipOptions={{position: 'bottom'}}
                    />
                </Col>
                <Col md="mr-auto">
                    <p className="occ-table-result-count">{t("activity-logs.Activity logs found")}: {activityList.count}</p>
                </Col>
            </Row>
            <Table striped borderless hover>
                <thead>
                <tr>
                    <th>#</th>
                    <th>{t("ui.type")}</th>
                    <th>{t("ui.state")}</th>
                    <th>{t("ui.Page")}</th>
                    <th>{t("ui.Overlay")}</th>
                    <th>{t("ui.created-at")}</th>
                    <th>{t("ui.last-updated")}</th>
                    <th>{t("ui.actions")}</th>
                </tr>
                </thead>
                <tbody>
                    {loadTableRows()}
                </tbody>
            </Table>

            {/* Pagination for the table */}
            {!_.isEmpty(activityList.data) && (
                <ReactPagiate
                    pageCount={Math.ceil(activityList.count / activityList.rows)}
                    pageRangeDisplayed={2}
                    pageMarginDisplayed={1}
                    onPageChange={(data) => fetchActivityLogs(activityList.rows, data.selected + 1)}
                    containerClassName={"pagination"}
                    activeClassName={'active'}
                    breakClassName={'page-item'}
                />
            )}
        </div>
    );
};

export default ActivityLogs;
