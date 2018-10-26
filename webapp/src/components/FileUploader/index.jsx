import React, { Component } from 'react';
import Dropzone from 'react-dropzone';

class UploadData extends Component {

    onDrop = file => {
        console.log(file);
        fetch("localhost:8888/csv", {
            method: "POST",
            headers: {
                "Content-Type": "application/json; charset=utf-8",
            },
            body: file,
        }).then(response => response.json());
    }

    render() {
        return (
            <div className="file-uploader">
                <Dropzone onDrop={this.onDrop} className="dropzone">
                    Drag and drop your data file here, or click here to browse...
                </Dropzone>
            </div>
        );
    }
}

export default UploadData;
