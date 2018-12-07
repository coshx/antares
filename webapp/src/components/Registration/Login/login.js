import React, { Component } from 'react';
import { connect } from 'react-redux';
import { Button, FormLabel, TextField } from '@material-ui/core/';
import { authenticationAction } from '../../../store/actions/index';
import { signInUser } from '../../../store/actions/index';

class Login extends Component {
  constructor(props) {
    super(props);
    this.state = {
      email: '',
      password: '',
      error: '',
    };
  }

  dismissError = () => {
    this.setState({ error: '' });
  }

  handleSubmit = (evt) => {
    evt.preventDefault();
    this.props.onAuthenticate(this.state.email, this.state.password);
    return this.setState({ error: '' });
  }

  handleEmailChange = (evt) => {
    this.setState({
      email: evt.target.value,
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
        <FormLabel>Email</FormLabel>
        <br />
        <TextField type="text" data-test="email" value={this.state.email} onChange={this.handleEmailChange} style={{marginBottom: '10px'}} />
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
  onAuthenticate: (email, password) => {
    dispatch(authenticationAction(email, password));
    //dispatch(signInUser(email));
  }
});

const mapStateToProps = state => ({
  authentication: state.authentication,
  user: state.user
});

export default connect(mapStateToProps, mapDispatchToProps)(Login);
