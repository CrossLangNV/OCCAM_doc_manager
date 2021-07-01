import React from 'react';
import {useTranslation} from "react-i18next";
import {Dropdown} from "primereact/dropdown";
import {useDispatch, useSelector} from "react-redux";
import {ModifyLanguage} from "../../actions/uiActions";

const LanguageSelector = () => {
    const { i18n } = useTranslation();
    const dispatch = useDispatch();
    const uiStates = useSelector(state => state.uiStates);

    const languages = [
        { name: 'English', value: 'en' },
        { name: 'Dutch', value: 'nl' },
        { name: 'French', value: 'fr' },
    ];


    const changeLanguage = lng => {
        i18n.changeLanguage(lng).then(r => {
            dispatch(ModifyLanguage(lng))
        });
    }

    return (
        <div>
            <Dropdown value={uiStates.language} options={languages} onChange={(e) => {
                changeLanguage(e.value)
            }} optionLabel="name" placeholder="Select a City"
            />
        </div>
    );
};

export default LanguageSelector;
