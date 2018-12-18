import React, { Component } from 'react';
import { Provider } from 'react-redux';
import { BrowserRouter as Router, Route } from 'react-router-dom';
import Home from './pages/Home';
import UploadData from './pages/UploadData';
import { store } from './store/store';

class App extends Component {
  render() {
    return (
      <Provider store={store}>
        <Router>
          <div className="App">
            <Route path="/" exact component={Home} />
            <Route path="/uploadData/" component={UploadData} />
          </div>
        </Router>
      </Provider>
    );
  }
}

export default App;
