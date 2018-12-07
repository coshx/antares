import React, { Component } from 'react';
import { Button, FormLabel, TextField } from '@material-ui/core/';

class SignUp extends Component {
  constructor() {
    super();
    this.state = {
      name: '',
      username: '',
      password: '',
      email: '',
      phoneNumber: '',
    };
  }

  dismissError = () => {
    this.setState({ error: '' });
  }

  handleRegistration = (evt) => {
    evt.preventDefault();
    return this.setState({ error: '' });
  }

  handleVerification = (evt) => {
    evt.preventDefault();
    this.setState({ error: '' });
  }

  handleNameChange = (evt) => {
    this.setState({
      name: evt.target.value,
    });
  }

  handleUserChange = (evt) => {
    this.setState({
      username: evt.target.value,
    });
  };

  handleEmailChange = (evt) => {
    this.setState({
      email: evt.target.value,
    });
  }

  handlePhoneChange = (evt) => {
    this.setState({
      phoneNumber: evt.target.value,
    });
  }

  handlePassChange = (evt) => {
    this.setState({
      password: evt.target.value,
    });
  }

  handleCodeChange = (evt) => {
    this.setState({
      confirmationCode: evt.target.value,
    });
  }

  render() {
    return (
      <form onSubmit={this.handleRegistration} style={{padding: '20px'}}>
        {
          this.state.error &&
            <h3 data-test="error">
              <button onClick={this.dismissError}>✖</button>
              {this.state.error}
            </h3>
        }
        <br />
        <FormLabel>New User Name</FormLabel>
        <br />
        <TextField type="text" data-test="username" value={this.state.username} onChange={this.handleUserChange} style={{marginBottom: '10px'}} />
        <br />
        <FormLabel>Email </FormLabel>
        <br />
        <TextField type="text" data-test="email" value={this.state.email} onChange={this.handleEmailChange} style={{marginBottom: '10px'}} />
        <br />
        <FormLabel>New Password </FormLabel>
        <br />
        <TextField type="password" data-test="password" value={this.state.password} onChange={this.handlePassChange} style={{marginBottom: '10px'}} />
        <br />
        <Button variant="contained" type="submit" value="Sign up" data-test="submit" color="primary" >
          Sign up
        </Button>
      </form>
    );
  }
}

export default SignUp;
