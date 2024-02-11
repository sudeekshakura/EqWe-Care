import React, { useState } from 'react';
import { FaUpload, FaTrash, FaSpinner } from 'react-icons/fa'; // Import FaSpinner for loading icon
import docImg from './doc2.jpg';
import './card.css';

function ImageUpload({ data }) {
  const [links, setLinks] = useState([]);
  const [pdfs, setPdfs] = useState([]); // Change state variable name to pdfs
  const [error, setError] = useState(null);
  const [disease, setDisease] = useState('acute');
  const [loading, setLoading] = useState(false);

  const handlePdfChange = (e) => { // Rename function to handlePdfChange
    const fileList = e.target.files;
    const pdfArray = [];

    for (let i = 0; i < fileList.length; i++) {
      const file = fileList[i];
      const reader = new FileReader();
      reader.onload = (e) => {
        pdfArray.push(e.target.result);
        if (pdfArray.length === fileList.length) {
          setPdfs([...pdfs, ...pdfArray]);
        }
      };
      reader.readAsDataURL(file);
    }
    setError(null);
  };

  const handleSubmit = () => {
    setLoading(true);
    // Assuming you are sending the PDF files to the server in a similar way as images
    // Adjust the request body accordingly
    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ data: JSON.stringify({ pdfs:pdfs, users: data }) })
    };

    fetch('http://localhost:5000/send_report', requestOptions)
      .then((response) => response.blob())
      .then((blob) => {
        // Create blob link to download
        const url = window.URL.createObjectURL(
          new Blob([blob]),
        );
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute(
          'download',
          `report.pdf`,
        );

    // Append to html link element page
    document.body.appendChild(link);

    // Start download
    link.click();

    // Clean up and remove the link
    link.parentNode.removeChild(link);
  })
  .catch((error) => {
    console.error('Error:', error);
    setError('Error sending report. Please try again.');
  })
  .finally(() => setLoading(false));
  };

  const handleDelete = (index) => {
    const newPdfs = pdfs.filter((_, i) => i !== index);
    setPdfs(newPdfs);
  };

  return (
    <div>
      <div style={{ display: 'flex' }}>
        <div style={{ width: '50%' }}>
          <img src={docImg} style={{ width: '600px', height: '700px' }} alt="Document" />
        </div>
        <div style={{ width: '600px', paddingRight: '300px', paddingTop: '100px' }}>
          <div style={{ textAlign: 'center', width: '800px', minHeight: '200px', display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
            <div style={{ border: '2px dashed #ccc', padding: '20px', borderRadius: '10px', marginBottom: '20px', display: 'flex', flexWrap: 'wrap', justifyContent: 'center' }}>
              <label htmlFor="pdfInput" style={{ cursor: 'pointer', marginBottom: '20px' }}>
                <FaUpload style={{ fontSize: '3em', marginBottom: '10px', color: '#007bff' }} />
                <div style={{ color: '#007bff' }}>Click to upload PDF files</div>
              </label>
              <input
                type="file"
                accept="application/pdf" // Accept PDF files only
                onChange={handlePdfChange}
                style={{ display: 'none' }}
                id="pdfInput"
                multiple
              />
              {pdfs.map((pdf, index) => (
                <div key={index} style={{ position: 'relative', margin: '10px', width: 'calc(50% - 30px)', textAlign: 'center' }}>
                  <embed src={pdf} type="application/pdf" width="200" height="200" />
                  <button onClick={() => handleDelete(index)} style={{ position: 'absolute', top: '5px', right: '5px', background: 'none', border: 'none', cursor: 'pointer' }}>
                    <FaTrash style={{ color: 'red' }} />
                  </button>
                </div>
              ))}
              <button
                onClick={() => handleSubmit()}
                style={{ textAlign: 'center', backgroundColor: '#1976d2', color: 'white', border: 'none', padding: '10px 20px', fontSize: '16px', cursor: 'pointer', borderRadius: '5px', marginLeft: '670px', top: '20px' }}
              >
                {loading ? <FaSpinner className="spinner" /> : 'Submit'}
              </button>
            </div>
            {error && <div style={{ color: 'red' }}>{error}</div>}
          </div>
          <div className="card-container">
            {links.map((link, index) => (
              <div key={index} className="card">
                <a href={link.url} target="_blank" rel="noopener noreferrer">
                  <h3>{link.name}</h3>
                </a>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default ImageUpload;
