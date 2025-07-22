'use client'

import { useState } from 'react'
import fetcher from '../../../lib/api'

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

    setStatus('Comprimindo...')
    try {
      const response = await fetcher('/pdf/compress/', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        throw new Error('Falha na requisição de compressão');
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `comprimido_${file.name}`)
      document.body.appendChild(link)
      link.click()
      link.remove()
      setStatus('Concluído!')
    } catch (error) {
      console.error('Falha na compressão', error)
      setStatus('Falhou!')
    }
  }

  return (
    <div className="min-h-screen p-4 md:p-8">
      <div className="max-w-2xl mx-auto bg-white p-6 rounded-lg shadow-lg">
        <h1 className="text-2xl md:text-3xl font-bold mb-6 text-sedam-blue">Comprimir PDF</h1>
        <form onSubmit={handleSubmit}>
          <div className="mb-6">
            <label className="block text-gray-700 mb-2 font-semibold">1. Envie seu arquivo .pdf</label>
            <input 
              type="file" 
              onChange={handleFileChange} 
              accept=".pdf" 
              className="w-full px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-sedam-blue bg-gray-50"
            />
          </div>
          <button 
            type="submit" 
            className="w-full btn-primary py-3"
            disabled={!file || status === 'Comprimindo...'}
          >
            {status === 'Comprimindo...' ? 'Processando...' : '2. Comprimir e Baixar'}
          </button>
        </form>
        {status && status !== 'Comprimindo...' && <p className="mt-6 text-center text-gray-700 font-medium">{status}</p>}
      </div>
    </div>
  )
}