import React, { Component } from 'react';
import { Button, Dialog } from '@material-ui/core/';
import SignUp from './Signup/signup';
import Login from './Login/login';

class Registration extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isSigningUp: false,
    };
  }

  switchSignUpState = () => {
    this.setState({ isSigningUp: !this.state.isSigningUp });
  }

  render() {
    let body = <Login />;
    let buttonText = 'Sign Up?';
    if (this.state.isSigningUp) {
      body = <SignUp switchSignUpState={this.switchSignUpState} />;
      buttonText = 'Already a member?';
    }
    return (
      <Dialog open className="Login">
        {body}
        <Button onClick={this.switchSignUpState} variant="contained" type="signup" value={buttonText} data-test="signup" color="secondary">
          {buttonText}
        </Button>
      </Dialog>
    );
  }
}

export default Registration;
