import React, { Component } from 'react';
import { connect } from 'react-redux';
import FileUploader from '../../components/FileUploader';
import Navbar from '../../components/Navbar';
import uploadActions from '../../store/actionTypes/upload';
import Registration from '../../components/Registration/registration';
import './uploadData.css';

class UploadData extends Component {
  render() {
    const { onDrop, token, isAuthenticated } = this.props;
    return (
      <div className="UploadData">
        { !isAuthenticated
                && <Registration />
                }
        <Navbar />
        <div className="instructions">
          First, upload your data and we'll make some models for you.
        </div>
        <div className="file-uploader-wrapper">
          <FileUploader pending={this.props.pending} onDrop={onDrop(token)} />
        </div>
      </div>
    );
  }
}

const mapStateToProps = state => ({
  isAuthenticated: !!state.authenticationReducer.email,
  token: state.authenticationReducer.token,
  pending: state.uploadReducer.pending,
});

const mapDispatchToProps = dispatch => ({
  onDrop: token => (acceptedFiles) => {
    const uploadedFile = acceptedFiles[0];
    dispatch({
      type: uploadActions.UPLOAD,
      file: uploadedFile,
    });
    const form = new FormData();
    form.append('csv', uploadedFile);
    console.log('TIME TO CALL THE API WITH THE FILE', form);
    console.log('TOKEN', token);
    fetch('http://localhost:8888/csv', {
      headers: {
        Authorization: `Bearer ${token}`,
      },
      method: 'POST',
      body: form,
    });
  },
});


export default connect(mapStateToProps, mapDispatchToProps)(UploadData);
