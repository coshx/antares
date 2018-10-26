import React, { Component } from 'react';
import FileUploader from './../components/FileUploader';
import Navbar from './../components/Navbar';
import './uploadData.css'

class UploadData extends Component {

    onDrop = (accepted, rejected) => {
        console.log('ACCEPTED: ', accepted);
        console.log('REJECTED:', rejected);
    }

    render() {
        return (
        <div className="UploadData">
            <Navbar></Navbar>
            <div className="instructions">First, upload your data and we'll make some models for you.</div>
            <div className="file-uploader-wrapper">
                <FileUploader onDrop={this.onDrop} />
            </div>
        </div>
        );
    }
}

export default UploadData;
