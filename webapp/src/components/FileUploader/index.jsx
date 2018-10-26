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
        console.log('FU props', this.props);
        return (
            <div className="file-uploader">
                {this.props.pending &&
                    <div className="dropzone">
                        Please wait while your file is uploaded...
                    </div>
                }
                {!this.props.pending && 
                    <Dropzone onDrop={this.props.onDrop} className="dropzone">
                        Drag and drop your data file here, or click here to browse...
                    </Dropzone>
                }
            </div>
        );
    }
}

export default UploadData;
