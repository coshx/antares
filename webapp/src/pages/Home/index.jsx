import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import './home.css';

class Home extends Component {
  render() {
    return (
      <div className="Home">
        <div className="welcome">
Welcome to Antares - The Explainable AI
        </div>
        <div className="instructions">
To get started, get your CSV dataset and click the button below
        </div>
        <Link to="/uploadData/">
          <button className="btn get-started">
Get Started
          </button>
        </Link>
      </div>
    );
  }
}

export default Home;
