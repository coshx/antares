import React, { Component } from 'react';
import { Button, FormLabel, TextField } from '@material-ui/core/';
import { connect } from 'react-redux';
import { authenticationAction } from '../../../store/actions/index';

class SignUp extends Component {
  constructor() {
    super();
    this.state = {
      password: '',
      passwordConfirmed: false,
      email: '',
    };
  }

  dismissError = () => {
    this.setState({ error: '' });
  }

  handleRegistration = (evt) => {
    evt.preventDefault();
    if (this.state.passwordConfirmed === false) {
      return this.setState({
        error: 'Passwords do not match!',
      });
    }
    fetch(`http://localhost:8888/registration`, {
      method: 'POST',
      body: JSON.stringify({email: this.state.email,
                            password: this.state.password})
    }).then(res => res.json()).then((response) => {
      if (!response.error) {
        this.props.onAuthenticate(response.email, response.session_token);
      } else {
        this.setState({ error: JSON.stringify(response.error.message) });
      }
    }).catch(error => this.setState({ error: 'Something went wrong' }));
  }

  handleEmailChange = (evt) => {
    this.setState({
      email: evt.target.value,
    });
  }

  handlePassChange = (evt) => {
    this.setState({
      password: evt.target.value,
    });
  }

  handlePassConfirm = (evt) => {
    if (this.state.password.localeCompare(evt.target.value) === 0) {
      this.setState({
        passwordConfirmed: true,
      });
    } else {
      this.setState({
        passwordConfirmed: false,
      });
    }
  }

  render() {
    return (
      <form onSubmit={this.handleRegistration} style={{ padding: '20px' }}>
        {
          this.state.error
            && (
            <h3 data-test="error">
              <button onClick={this.dismissError}>✖</button>
              {this.state.error}
            </h3>
            )
        }
        <br />
        <FormLabel>Email </FormLabel>
        <br />
        <TextField type="text" data-test="email" value={this.state.email} onChange={this.handleEmailChange} style={{ marginBottom: '10px' }} />
        <br />
        <FormLabel>New Password </FormLabel>
        <br />
        <TextField type="password" data-test="password" value={this.state.password} onChange={this.handlePassChange} style={{ marginBottom: '10px' }} />
        <br />
        <FormLabel>Confirm Password </FormLabel>
        <br />
        <TextField type="password" data-test="password" onChange={this.handlePassConfirm} style={{ marginBottom: '10px' }} />
        <br />
        <Button variant="contained" type="submit" value="Sign up" data-test="submit" color="primary">
          Sign Up
        </Button>
      </form>
    );
  }
}


const mapDispatchToProps = dispatch => ({
  onAuthenticate: (email, token) => {
    dispatch(authenticationAction(email, token));
  },
});

const mapStateToProps = state => ({
  authentication: state.authenticationReducer,
  user: state.user,
});

export default connect(mapStateToProps, mapDispatchToProps)(SignUp);
