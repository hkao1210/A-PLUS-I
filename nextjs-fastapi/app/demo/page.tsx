"use client";

import React, { useState } from 'react';
import { Upload, FileText, Check, AlertCircle, X } from 'lucide-react';
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from "@/components/ui/card";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Badge } from "@/components/ui/badge";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";

interface ProcessingResult {
  score: number;
  feedback: string;
  breakdown: {
    accuracy: number;
    clarity: number;
    concepts: number;
  };
}

interface UploadStatus {
  type: 'error' | 'success';
  message: string;
}

const AIDemo = () => {
  const [file, setFile] = useState<File | null>(null);
  const [question, setQuestion] = useState<string>('');
  const [teacherAnswer, setTeacherAnswer] = useState<string>('');
  const [uploadStatus, setUploadStatus] = useState<UploadStatus | null>(null);
  const [processingResult, setProcessingResult] = useState<ProcessingResult | null>(null);
  const [isProcessing, setIsProcessing] = useState<boolean>(false);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile && (selectedFile.type === 'application/pdf' || selectedFile.type === 'text/plain')) {
      setFile(selectedFile);
      setUploadStatus(null);
      setProcessingResult(null);
    } else {
      setUploadStatus({
        type: 'error',
        message: 'Please upload a PDF or text file'
      });
    }
  };

  const handleDeleteFile = () => {
    setFile(null);
    setProcessingResult(null);
    // Reset the file input
    const fileInput = document.getElementById('file-upload') as HTMLInputElement;
    if (fileInput) {
      fileInput.value = '';
    }
  };

  const handleUpload = async () => {
    if (!file || !question || !teacherAnswer) {
      setUploadStatus({
        type: 'error',
        message: 'Please fill in all fields and select a file'
      });
      return;
    }

    setIsProcessing(true);
    
    try {
      // First, upload the PDF to the database
      const formData = new FormData();
      formData.append('file', file);
      
      const uploadResponse = await fetch('/api/upload-pdf', {
        method: 'POST',
        body: formData,
      });

      if (!uploadResponse.ok) {
        throw new Error('Failed to upload PDF');
      }

      const uploadResult = await uploadResponse.json();
      const pdfId = uploadResult.id;

      // Now process the answer using the uploaded PDF
      const processingResponse = await fetch('/api/process-answer', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          pdfId,
          question,
          teacherAnswer,
        }),
      });

      if (!processingResponse.ok) {
        throw new Error('Failed to process answer');
      }

      const result = await processingResponse.json();
      
      setUploadStatus({
        type: 'success',
        message: 'Answer processed successfully'
      });
      
      setProcessingResult(result);

    } catch (error) {
      console.error('Processing error:', error);
      setUploadStatus({
        type: 'error',
        message: error instanceof Error ? error.message : 'An error occurred during processing'
      });
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="container mx-auto p-6 max-w-4xl">
      <h1 className="text-3xl font-bold mb-2">A+I Demo</h1>
      <p className="text-gray-600 mb-8">Automated Answer Assessment System</p>
      
      <div className="grid gap-6">
        {/* Question and Answer Section */}
        <Card>
          <CardHeader>
            <CardTitle>Question and Reference Answer</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="question">Question</Label>
              <Textarea
                id="question"
                placeholder="Enter the question here..."
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                className="min-h-[100px]"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="teacher-answer">Teacher's Answer</Label>
              <Textarea
                id="teacher-answer"
                placeholder="Enter the reference answer here..."
                value={teacherAnswer}
                onChange={(e) => setTeacherAnswer(e.target.value)}
                className="min-h-[100px]"
              />
            </div>
          </CardContent>
        </Card>

        {/* Upload Section */}
        <Card>
          <CardHeader>
            <CardTitle>Upload Student Answer</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="border-2 border-dashed border-gray-200 rounded-lg p-6 text-center">
                <input
                  type="file"
                  id="file-upload"
                  className="hidden"
                  onChange={handleFileChange}
                  accept=".pdf,.txt"
                />
                <label 
                  htmlFor="file-upload"
                  className="cursor-pointer flex flex-col items-center gap-2"
                >
                  <FileText className="h-12 w-12 text-gray-400" />
                  <span className="text-sm text-gray-600">
                    Drop your file here or click to browse
                  </span>
                </label>
              </div>
              
              {file && (
                <div className="flex items-center justify-between text-sm text-gray-600 bg-gray-50 p-2 rounded">
                  <div className="flex items-center gap-2">
                    <FileText className="h-4 w-4" />
                    {file.name}
                  </div>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={handleDeleteFile}
                    className="text-red-500 hover:text-red-700"
                  >
                    <X className="h-4 w-4" />
                  </Button>
                </div>
              )}
            </div>
          </CardContent>
          <CardFooter>
            <Button 
              onClick={handleUpload} 
              disabled={!file || !question || !teacherAnswer || isProcessing}
              className="w-full"
            >
              {isProcessing ? 'Processing...' : 'Process Answer'}
            </Button>
          </CardFooter>
        </Card>

        {/* Status Messages */}
        {uploadStatus && (
          <Alert variant={uploadStatus.type === 'error' ? 'destructive' : 'default'}>
            {uploadStatus.type === 'error' ? (
              <AlertCircle className="h-4 w-4" />
            ) : (
              <Check className="h-4 w-4" />
            )}
            <AlertDescription>{uploadStatus.message}</AlertDescription>
          </Alert>
        )}

        {/* Results Section */}
        {processingResult && (
          <Card>
            <CardHeader>
              <CardTitle>Assessment Results</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-lg font-medium">Overall Score</span>
                  <span className="text-2xl font-bold">{processingResult.score}%</span>
                </div>
                
                <div className="space-y-2">
                  <h3 className="font-medium">Evaluation Breakdown:</h3>
                  <div className="grid grid-cols-3 gap-4">
                    <div className="text-center">
                      <Badge variant="secondary" className="mb-2">Accuracy</Badge>
                      <p className="text-lg">{processingResult.breakdown.accuracy}/4</p>
                    </div>
                    <div className="text-center">
                      <Badge variant="secondary" className="mb-2">Clarity</Badge>
                      <p className="text-lg">{processingResult.breakdown.clarity}/4</p>
                    </div>
                    <div className="text-center">
                      <Badge variant="secondary" className="mb-2">Concepts</Badge>
                      <p className="text-lg">{processingResult.breakdown.concepts}/4</p>
                    </div>
                  </div>
                </div>

                <div className="bg-gray-50 p-4 rounded-lg">
                  <h3 className="font-medium mb-2">Feedback</h3>
                  <p className="text-gray-700">{processingResult.feedback}</p>
                </div>
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
};

export default AIDemo;