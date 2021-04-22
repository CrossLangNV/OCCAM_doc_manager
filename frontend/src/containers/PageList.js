import React, {useRef} from 'react';
import {Card} from "primereact/card";
import {Image, Row} from "react-bootstrap";
import {useSelector, useDispatch} from "react-redux";
import {DeletePage, GetPageList} from "../actions/pageActions";
import {Button} from "primereact/button";
import {confirmPopup} from "primereact/confirmpopup";
import {Toast} from "primereact/toast";


const PageList = (props) => {
    const dispatch = useDispatch()

    const pageList = useSelector(state => state.pageList);
    const documentId = props.documentId;

    const toast = useRef(null);


    React.useEffect(() => {
        dispatch(GetPageList(100, 1, documentId))
    }, [])

    const confirmDeletePage = (event) => {
        confirmPopup({
            target: event.currentTarget,
            message: 'Are you sure you want to delete this page?',
            icon: 'pi pi-exclamation-triangle',
            accept: () =>
            {
                dispatch(DeletePage(event))
                toast.current.show({severity: 'success', summary: 'Success', detail: 'Page has been deleted'});
            },
        });
    }

    return (
        <Row className='scroll-horizontally'>
            {pageList.data.map(page => {
                return <Card key={page.id} className='page-card'>
                    <Image className='page-card-img' src={page.file} />
                    <Button
                        onClick={() => confirmDeletePage(page.id)}
                        label=""
                        icon="pi pi-trash"
                        className="p-button-danger btn-margin-left"
                        tooltip="Delete page"
                        tooltipOptions={{position: 'bottom'}}
                    />
                </Card>
            })}
            <Toast ref={toast} />
        </Row>
    );
};

export default PageList;
