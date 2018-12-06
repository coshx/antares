import React, { Component } from 'react';
import { connect } from 'react-redux';
import { Button, FormLabel, TextField } from '@material-ui/core/';
import { authenticationAction } from '../../../store/actions/index';
import { signInUser } from '../../../store/actions/index';

class Login extends Component {
  constructor(props) {
    super(props);
    this.state = {
      username: '',
      password: '',
      error: '',
    };
  }

  dismissError = () => {
    this.setState({ error: '' });
  }

  handleSubmit = (evt) => {

    return this.setState({ error: '' });
  }

  handleUserChange = (evt) => {
    this.setState({
      username: evt.target.value,
    });
  };

  handlePassChange = (evt) => {
    this.setState({
      password: evt.target.value,
    });
  }

  render() {
    return (
      <form onSubmit={this.handleSubmit} style={{padding: '20px'}}>
        {
          this.state.error &&
          <h3 data-test="error">
            <button onClick={this.dismissError}>✖</button>
            {this.state.error}
          </h3>
        }
        <FormLabel>User Name</FormLabel>
        <br />
        <TextField type="text" data-test="username" value={this.state.username} onChange={this.handleUserChange} style={{marginBottom: '10px'}} />
        <br />
        <FormLabel>Password</FormLabel>
        <br />
        <TextField type="password" data-test="password" value={this.state.password} onChange={this.handlePassChange} style={{marginBottom: '10px'}} />
        <br />

        <Button variant="contained" type="submit" value="Log In" data-test="submit" color="primary">
          Sign In
        </Button>
      </form>
    );
  }
}

const mapDispatchToProps = dispatch => ({
  onAuthenticate: (token, username, email) => {
    dispatch(authenticationAction(token, username));
    dispatch(signInUser(email));
  }
});

const mapStateToProps = state => ({
  authentication: state.authentication,
  user: state.user
});

export default connect(mapStateToProps, mapDispatchToProps)(Login);
