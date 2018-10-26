import React, { Component } from 'react';
import {connect} from 'react-redux';
import FileUploader from './../../components/FileUploader';
import Navbar from './../../components/Navbar';
import uploadActions from './../../store/actionTypes/upload'
import './uploadData.css'

class UploadData extends Component {

    render() {
        console.log('UD PROPS', this.props);
        return (
            <div className="UploadData">
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
    console.log('MSTP', state);
    return {
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
            form.append('csv', uploadedFile, 'data.csv');
            console.log('TIME TO CALL THE API WITH THE FILE');
            // fetch('/csv', {
            //     method: 'POST',
            //     body: form
            // });
        }
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(UploadData);
