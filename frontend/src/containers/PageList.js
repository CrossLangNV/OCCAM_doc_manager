import React from 'react';
import {Card} from "primereact/card";
import {Image, Row} from "react-bootstrap";
import {useSelector, useDispatch} from "react-redux";
import {GetPageList} from "../actions/pageActions";


const PageList = (props) => {
    const dispatch = useDispatch()

    const pageList = useSelector(state => state.pageList);
    const documentId = props.documentId;

    React.useEffect(() => {
        dispatch(GetPageList(100, 1, documentId))
    }, [])

    return (
        <Row className='scroll-horizontally'>
            {pageList.data.map(page => {
                return <Card key={page.id} className='page-card'>
                    <Image className='page-card-img' src={page.file} />
                </Card>
            })}
        </Row>
    );
};

export default PageList;
