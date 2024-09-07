'use client';  // This is necessary for using hooks in Next.js 13 pages
import { useState } from 'react'
import PDFList from './components/PDFList';

export default function Home() {
  const [file, setFile] = useState<File | null>(null)
  const [message, setMessage] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFile(e.target.files[0])
    }
  }

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    if (!file) {
      setMessage('Please select a file')
      return
    }

    setIsLoading(true)
    setMessage('')

    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await fetch('/api/upload-pdf', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      setMessage(data.message)
    } catch (error) {
      console.error('Error:', error)
      setMessage('An error occurred while uploading the file')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">PDF Upload</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="file" className="block mb-2">Select PDF:</label>
          <input 
            type="file" 
            id="file" 
            accept=".pdf" 
            onChange={handleFileChange} 
            className="border p-2"
            disabled={isLoading}
          />
        </div>
        <button 
          type="submit" 
          className={`text-white px-4 py-2 rounded ${
            isLoading ? 'bg-gray-400 cursor-not-allowed' : 'bg-blue-500 hover:bg-blue-600'
          }`}
          disabled={isLoading}
        >
          {isLoading ? 'Uploading...' : 'Upload'}
        </button>
      </form>
      {message && <p className={`mt-4 ${message.includes('error') ? 'text-red-500' : 'text-green-500'}`}>{message}</p>}
      <PDFList />
    </div>
  )
}