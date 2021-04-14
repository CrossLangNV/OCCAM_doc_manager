import {useDispatch, useSelector} from "react-redux";
import {GetDocument} from "../actions/documentActions";
import React from "react";
import _ from "lodash"

const Document = (props) => {
    const documentId = props.match.params.documentId
    const dispatch = useDispatch()
    const documentState = useSelector(state => state.document)

    React.useEffect(() => {
        dispatch(GetDocument(documentId))
    }, [])

    const showData = () => {
        if (!_.isEmpty(documentState.data[documentId])) {

            const documentData = documentState.data[documentId]
            return(
                <div>
                    <h1>{documentData.name}</h1>
                    <p>{documentData.content}</p>
                    <p>State: {documentData.state}</p>
                    <p>Created at: {documentData.created_at}</p>
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
