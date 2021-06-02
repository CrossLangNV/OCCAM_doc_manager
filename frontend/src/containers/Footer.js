import React from 'react';
import {useLocation} from "react-router-dom";

const Footer = () => {
    const location = useLocation();

    const FOOTER_STICK_TO_BOTTOM = ["/", "/activity", "/help"]

    return (
        <div className={FOOTER_STICK_TO_BOTTOM.includes(location.pathname) ? "occ-footer occ-footer-bottom" : "occ-footer"}>
            <a href="http://www.crosslang.com" target="_blank">
                <img src="/crosslang-logo.png" className="occ-footer-logo"/>
            </a>
            <a href="https://www.vutbr.cz/en/" target="_blank">
                <img src="/brno-logo.png" className="occ-footer-logo"/>
            </a>
            <a href="https://platformdh.uantwerpen.be/index.php/clariah-vl/" target="_blank">
                <img src="/clariah-logo.png" className="occ-footer-logo"/>
            </a>
        </div>
    );
};

export default Footer;
