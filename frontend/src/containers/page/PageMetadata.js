import React, {useState} from 'react';
import {Timeline} from "primereact/timeline";
import _ from "lodash";
import {useTranslation} from "react-i18next";
import {Button} from "primereact/button";
import {Dialog} from "primereact/dialog";
import {InputTextarea} from "primereact/inputtextarea";
import {useDispatch} from "react-redux";

const PageMetadata = (props) => {
    const page = props.page
    const [metadata, setMetadata] = useState([]);
    const {t} = useTranslation();
    const editable = ["titles", "descriptions", "description"]
    const dispatch = useDispatch();
    const [editMetadataDialog, setEditMetadataDialog] = useState(false);
    const [newMetadataValue, setNewMetadataValue] = useState("");
    const [newMetadataType, setNewMetadataType] = useState("");


    React.useEffect(() => {
        const labels = []

        const metadata = Object.entries(page.metadata)
        metadata.forEach(label => {
            labels.push({status: `${label[0]}`, date: label[1].join(", ")})
        })

        setMetadata(labels)
    }, [])

    const isNotEditable = metadataItem => {
        if (editable.includes(metadataItem)) {
            return false
        }
        return true
    }

    const changeMetadataItem = (item) => {
        if (editable.includes(item)) {
            console.log(`Changing metadata: ${item}`)
            setNewMetadataType(item)
            setEditMetadataDialog(true)
        }
    };

    return (
        <div>
            <Dialog header="Edit value" visible={editMetadataDialog} style={{width: '40vw'}}
                    onHide={() => setEditMetadataDialog(false)}>
                <InputTextarea className={"space-between-title-and-button"}
                               value={newMetadataValue} onChange={(e) => setNewMetadataValue(e.target.value)}
                               placeholder={"Enter a new value..."}
                               rows={1}
                               cols={70}
                               autoResize={true}
                               autoFocus={true}
                />
                <Button label={t("ui.save")} onClick={() => {
                    console.log(newMetadataType)
                    // dispatch(ChangeTutorialState(auth.user, true))
                }}/>
            </Dialog>

            {(_.isEmpty(metadata) &&
                <p>{t("page-metadata.No metadata available")}</p>
            )}


            <Timeline value={metadata} opposite={(item) => item.status}
                      content={(item) =>
                          <small className="p-text-secondary">
                              {item.date}
                              {!isNotEditable(item.status) ?
                                  <Button
                                      icon="pi pi-pencil"
                                      className="p-button-rounded p-button-outlined small-edit-button p-button-warning"
                                      onClick={((event) => changeMetadataItem(item.status))}
                                  /> : ""
                              }
                          </small>
                      }/>
        </div>
    );
};

export default PageMetadata;
