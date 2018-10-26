import React, { Component } from 'react';
import { BrowserRouter as Router, Route } from "react-router-dom";
import Home from './Home'
import UploadData from './UploadData'

class App extends Component {
  render() {
    return (
      <Router>
        <div className="App">
          <Route path="/" exact component={Home} />
          <Route path="/uploadData/" component={UploadData}>
          </Route>
        </div>
      </Router>
    );
  }
}

export default App;
