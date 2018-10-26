import React, { Component } from 'react';
import {Link} from "react-router-dom";
import './navbar.css'

class Navbar extends Component {

    render() {
        return (
            <div className="navbar">
                <Link to="/"><div className="navbar-logo">Antares</div></Link>
            </div>
        );
    }
}

export default Navbar;
