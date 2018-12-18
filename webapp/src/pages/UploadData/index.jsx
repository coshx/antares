import React, { Component } from 'react';
import {connect} from 'react-redux';
import FileUploader from './../../components/FileUploader';
import Navbar from './../../components/Navbar';
import uploadActions from './../../store/actionTypes/upload'
import Registration from '../../components/Registration/registration'
import './uploadData.css'

class UploadData extends Component {

    render() {
        const isAuthenticated = this.props.isAuthenticated;
        console.log('Is authenticated', this.props.isAuthenticated);
        return (
            <div className="UploadData">
                { !isAuthenticated &&
                <Registration />
                }
                <Navbar></Navbar>
                <div className="instructions">First, upload your data and we'll make some models for you.</div>
                <div className="file-uploader-wrapper">
                    <FileUploader pending={this.props.pending} onDrop={this.props.onDrop} />
                </div>
            </div>
        );
    }
}

const mapStateToProps = (state) => {
    return {
        isAuthenticated: !!state.authenticationReducer.email,
        pending: state.uploadReducer.pending
    }
}

const mapDispatchToProps = (dispatch) => {
    return {
        onDrop: (acceptedFiles) => {
            let uploadedFile = acceptedFiles[0];
            dispatch({
                type: uploadActions.UPLOAD,
                file: uploadedFile
            });
            let form = new FormData();
            form.append('csv', uploadedFile);
            console.log('TIME TO CALL THE API WITH THE FILE', form);
            fetch('http://localhost:8888/csv', {
                method: 'POST',
                body: form
            });
        }
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(UploadData);
