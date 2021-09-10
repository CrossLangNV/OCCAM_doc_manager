import React from 'react';
import {useLocation} from "react-router-dom";

const Footer = () => {
    const location = useLocation();

    const FOOTER_STICK_TO_BOTTOM = ["/activity", "/login", "/settings"]

    return (
        <div className={FOOTER_STICK_TO_BOTTOM.includes(location.pathname) ? "occ-footer occ-footer-bottom" : "occ-footer"}>
            <a href="http://www.crosslang.com" target="_blank" rel="noreferrer">
                <img src="/crosslang-logo.png" className="occ-footer-logo" alt="Crosslang logo"/>
            </a>
            <a href="https://www.vutbr.cz/en/" target="_blank" rel="noreferrer">
                <img src="/brno-logo.png" className="occ-footer-logo" alt="Brno logo"/>
            </a>
            <a href="https://platformdh.uantwerpen.be/index.php/clariah-vl/" target="_blank" rel="noreferrer">
                <img src="/clariah-logo.png" className="occ-footer-logo" alt="Clariah logo"/>
            </a>
            <a href="https://ec.europa.eu/" target="_blank" rel="noreferrer">
                <img src="/europe-logo.png" className="occ-footer-logo" alt="Europe logo"/>
            </a>
        </div>
    );
};

export default Footer;
