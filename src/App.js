import React, { useState } from 'react';
import { Document, Page, pdfjs } from 'react-pdf';
import { PDFDocument } from 'pdf-lib';
import './App.css';

pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.js`;

function App() {
  const [numPages, setNumPages] = useState(null);
  const [pageNumber, setPageNumber] = useState(1);
  const [pdfBytes, setPdfBytes] = useState(null);

  function onDocumentLoadSuccess({ numPages }) {
    setNumPages(numPages);
  }

  async function handleFileChange(event) {
    const file = event.target.files[0];
    if (file) {
      const arrayBuffer = await file.arrayBuffer();
      setPdfBytes(new Uint8Array(arrayBuffer));
    }
  }

  async function addTextToPdf() {
    if (!pdfBytes) {
      return;
    }

    const pdfDoc = await PDFDocument.load(pdfBytes);
    const pages = pdfDoc.getPages();
    const firstPage = pages[0];

    firstPage.drawText('Hello, PDF!', {
      x: 5,
      y: firstPage.getHeight() / 2 + 250,
      size: 50,
    });

    const modifiedPdfBytes = await pdfDoc.save();
    setPdfBytes(modifiedPdfBytes);
  }

  function downloadPdf() {
    if (!pdfBytes) {
      return;
    }
    const blob = new Blob([pdfBytes], { type: 'application/pdf' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'modified-pdf.pdf';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }

  return (
    <div className="App">
      <h1>PDF Editor</h1>
      <input type="file" onChange={handleFileChange} />
      <div style={{ display: 'flex', marginTop: '20px' }}>
        <div style={{ border: '1px solid black', marginRight: '20px' }}>
          {pdfBytes && (
            <Document
              file={{ data: pdfBytes }}
              onLoadSuccess={onDocumentLoadSuccess}
            >
              <Page pageNumber={pageNumber} />
            </Document>
          )}
        </div>
        <div>
          {numPages && (
            <p>
              Page {pageNumber} of {numPages}
            </p>
          )}
          <button onClick={addTextToPdf} disabled={!pdfBytes}>
            Add Text
          </button>
          <button onClick={downloadPdf} disabled={!pdfBytes}>
            Download PDF
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;