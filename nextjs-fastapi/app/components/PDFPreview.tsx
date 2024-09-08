import React, { useState, useEffect } from 'react';

interface PDFPreviewProps {
    pdfId: string;
}

const PDFPreview: React.FC<PDFPreviewProps> = ({ pdfId }) => {
    const [pdfUrl, setPdfUrl] = useState<string>('');
    const [isLoading, setIsLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchPDF = async () => {
            setIsLoading(true);
            try {
                const response = await fetch(`/api/preview-pdf/${pdfId}`);
                if (!response.ok) {
                    throw new Error('Failed to fetch PDF');
                }
                const blob = await response.blob();
                const url = URL.createObjectURL(blob);
                setPdfUrl(url);
                setIsLoading(false);
            } catch (e: unknown) {
                if (typeof e === 'string') {
                    setError(e);
                }
                setIsLoading(false);
            }
        };

        fetchPDF();

        // Cleanup function to revoke the object URL
        return () => {
            if (pdfUrl) {
                URL.revokeObjectURL(pdfUrl);
            }
        };
    }, [pdfId]);

    if (isLoading) {
        return <div>Loading PDF...</div>;
    }

    if (error) {
        return <div>Error: {error}</div>;
    }

    return (
        <div className="w-full h-screen">
            <iframe
                src={pdfUrl}
                className="w-full h-full border-none"
                title="PDF Preview"
            />
        </div>
    );
};

export default PDFPreview;