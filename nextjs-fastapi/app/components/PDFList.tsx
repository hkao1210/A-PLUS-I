import React, { useState, useEffect } from 'react';

interface PDFInfo {
  id: number;
  filename: string;
  path: string;
  upload_date: string;
}

export default function PDFList() {
  const [pdfs, setPdfs] = useState<PDFInfo[]>([]);

  useEffect(() => {
    async function fetchPDFs() {
      try {
        const response = await fetch('/api/pdfs');
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setPdfs(data);
      } catch (error) {
        console.error('Error fetching PDFs:', error);
      }
    }

    fetchPDFs();
  }, []);

  return (
    <div>
      <h2>Uploaded PDFs</h2>
      <ul>
        {pdfs.map((pdf) => (
          <li key={pdf.id}>
            {pdf.filename} (Uploaded on: {new Date(pdf.upload_date).toLocaleString()})
          </li>
        ))}
      </ul>
    </div>
  );
}