import React, { Component } from 'react';
import Dropzone from 'react-dropzone';

class UploadData extends Component {

    render() {
        return (
            <div className="file-uploader">
                <Dropzone onDrop={this.props.onDrop} className="dropzone">
                    Drag and drop your data file here, or click here to browse...
                </Dropzone>
            </div>
        );
    }
}

export default UploadData;
