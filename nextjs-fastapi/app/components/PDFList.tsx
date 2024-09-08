import { useState, useEffect } from 'react';

interface PDF {
  id: string;
  filename: string;
  upload_date: string;
}

export default function PDFList() {
  const [pdfs, setPdfs] = useState<PDF[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);

  useEffect(() => {
    fetchPDFs();
  }, []);

  const fetchPDFs = async () => {
    try {
      const response = await fetch('/api/pdfs');
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data: PDF[] = await response.json();
      setPdfs(data);
    } catch (error) {
      console.error('Error fetching PDFs:', error);
      setError('Failed to load PDFs');
    } finally {
      setIsLoading(false);
    }
  };

  const handlePreview = (pdfId: string) => {
    setPreviewUrl(`/api/preview-pdf/${pdfId}`);
  };

  const handleDownload = (pdfId: string, filename: string) => {
    window.open(`/api/download-pdf/${pdfId}`, '_blank');
  };

  if (isLoading) return <div>Loading PDFs...</div>;
  if (error) return <div className="text-red-500">{error}</div>;

  return (
    <div className="mt-8">
      <h2 className="text-xl font-semibold mb-4">Uploaded PDFs</h2>
      {pdfs.length === 0 ? (
        <p>No PDFs uploaded yet.</p>
      ) : (
        <div className="space-y-4">
          {pdfs.map((pdf) => (
            <div key={pdf.id} className="border p-4 rounded flex justify-between items-center">
              <span>{pdf.filename}</span>
              <div>
                <button
                  onClick={() => handlePreview(pdf.id)}
                  className="bg-blue-500 text-white px-3 py-1 rounded mr-2 hover:bg-blue-600"
                >
                  Preview
                </button>
                <button
                  onClick={() => handleDownload(pdf.id, pdf.filename)}
                  className="bg-green-500 text-white px-3 py-1 rounded hover:bg-green-600"
                >
                  Download
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
      {previewUrl && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center">
          <div className="bg-white p-4 rounded-lg w-4/5 h-4/5">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-semibold">PDF Preview</h3>
              <button
                onClick={() => setPreviewUrl(null)}
                className="text-gray-500 hover:text-gray-700"
              >
                Close
              </button>
            </div>
            <iframe src={previewUrl} className="w-full h-full" />
          </div>
        </div>
      )}
    </div>
  );
}