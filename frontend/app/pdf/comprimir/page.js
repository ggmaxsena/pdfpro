'use client'

import { useState } from 'react'
import axios from 'axios'

export default function Compress() {
  const [file, setFile] = useState(null)
  const [status, setStatus] = useState('')

  const handleFileChange = (e) => {
    setFile(e.target.files[0])
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!file) return

    const formData = new FormData()
    formData.append('file', file)

    setStatus('Compressing...')
    try {
      const token = localStorage.getItem('token')
      const response = await axios.post('/api/pdf/compress/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          'Authorization': `Bearer ${token}`,
        },
        responseType: 'blob',
      })

      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `compressed_${file.name}`)
      document.body.appendChild(link)
      link.click()
      setStatus('Completed!')
    } catch (error) {
      console.error('Compression failed', error)
      setStatus('Failed!')
    }
  }

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-xl mx-auto bg-white p-6 rounded shadow-md">
        <h1 className="text-2xl font-bold mb-6">Compress PDF</h1>
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block text-gray-700">Upload .pdf file</label>
            <input type="file" onChange={handleFileChange} accept=".pdf" className="w-full" />
          </div>
          <button type="submit" className="w-full bg-blue-500 text-white py-2 rounded" disabled={!file}>
            Compress and Download
          </button>
        </form>
        {status && <p className="mt-4 text-center">{status}</p>}
      </div>
    </div>
  )
}
