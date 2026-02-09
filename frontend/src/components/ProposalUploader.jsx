import React, { useState } from 'react';
import api from '../services/api';
import './ProposalUploader.css';

function ProposalUploader({ onProposalUploaded }) {
    const [file, setFile] = useState(null);
    const [uploading, setUploading] = useState(false);
    const [error, setError] = useState('');
    const [dragActive, setDragActive] = useState(false);

    const handleDrag = (e) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === 'dragenter' || e.type === 'dragover') {
            setDragActive(true);
        } else if (e.type === 'dragleave') {
            setDragActive(false);
        }
    };

    const handleDrop = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(false);

        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            setFile(e.dataTransfer.files[0]);
        }
    };

    const handleFileChange = (e) => {
        if (e.target.files && e.target.files[0]) {
            setFile(e.target.files[0]);
        }
    };

    const handleUpload = async () => {
        if (!file) {
            setError('Please select a file');
            return;
        }

        setUploading(true);
        setError('');

        try {
            const response = await api.uploadProposal(file);
            if (response.success) {
                onProposalUploaded(response.proposal);
                setFile(null);
            } else {
                setError(response.error || 'Upload failed');
            }
        } catch (err) {
            setError(err.message || 'Upload failed');
        } finally {
            setUploading(false);
        }
    };

    return (
        <div className="proposal-uploader glass-card">
            <h2>Upload Research Proposal</h2>
            <p className="text-secondary mb-2">
                Upload a PDF or text file containing the research proposal to be reviewed.
            </p>

            {error && (
                <div className="error-message">
                    {error}
                </div>
            )}

            <div
                className={`dropzone ${dragActive ? 'active' : ''} ${file ? 'has-file' : ''}`}
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
            >
                <input
                    type="file"
                    id="file-input"
                    accept=".pdf,.txt,.doc,.docx"
                    onChange={handleFileChange}
                    style={{ display: 'none' }}
                />

                {file ? (
                    <div className="file-info">
                        <div className="file-icon">📄</div>
                        <div className="file-details">
                            <p className="file-name">{file.name}</p>
                            <p className="file-size">{(file.size / 1024).toFixed(2)} KB</p>
                        </div>
                        <button
                            className="remove-file-btn"
                            onClick={() => setFile(null)}
                        >
                            ×
                        </button>
                    </div>
                ) : (
                    <label htmlFor="file-input" className="dropzone-label">
                        <div className="upload-icon">📤</div>
                        <p className="dropzone-text">
                            Drag and drop your file here, or click to browse
                        </p>
                        <p className="dropzone-hint">
                            Supported formats: PDF, TXT, DOC, DOCX (Max 16MB)
                        </p>
                    </label>
                )}
            </div>

            <button
                className="btn btn-primary btn-full"
                onClick={handleUpload}
                disabled={!file || uploading}
            >
                {uploading ? (
                    <>
                        <span className="spinner-small"></span>
                        Uploading...
                    </>
                ) : (
                    'Upload Proposal'
                )}
            </button>
        </div>
    );
}

export default ProposalUploader;
