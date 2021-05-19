import React from 'react';
import {useDispatch, useSelector} from "react-redux";
import {GetActivityList} from "../actions/acitvityActions";
import _ from "lodash";
import {Link} from "react-router-dom";
import DocumentState from "./DocumentState";
import Moment from "react-moment";
import {Button} from "primereact/button";
import {Table} from "react-bootstrap";
import ReactPagiate from "react-paginate";

const ActivityLogs = () => {
    const dispatch = useDispatch();
    const activityList = useSelector(state => state.activityLogsList);

    React.useEffect(() => {
        fetchActivityLogs(5, 1);
    }, []);

    const fetchActivityLogs = (rows, page) => {
        dispatch(GetActivityList(rows, page, "", ""))
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
                                {item.state}
                            </td>
                            <td>
                                {item.page}
                            </td>
                            <td>
                                {item.overlay}
                            </td>
                            <td className='w-10'>
                                <Moment format="DD/MM/YYYY H:mm" date={item.created_at}/>
                            </td>
                            <td className='w-10'>
                                <Moment format="DD/MM/YYYY H:mm" date={item.updated_at}/>
                            </td>
                            <td className='w-10'>

                            </td>
                        </tr>
                    })}
                </>
            )
        }
    }


    return (
        <div>
            <Table striped borderless hover>
                <thead>
                <tr>
                    <th>#</th>
                    <th>Type</th>
                    <th>State</th>
                    <th>Page</th>
                    <th>Overlay</th>
                    <th>Created at</th>
                    <th>Last updated</th>
                    <th>Actions</th>
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
