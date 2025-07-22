'use client'

import { useState } from 'react'

export default function Split() {
  const [file, setFile] = useState(null)
  const [splitOption, setSplitOption] = useState('pages')
  const [pages, setPages] = useState('')
  const [size, setSize] = useState(20)
  const [status, setStatus] = useState('')

  const handleFileChange = (e) => {
    setFile(e.target.files[0])
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!file) return

    const formData = new FormData()
    formData.append('file', file)
    formData.append('split_option', splitOption)

    if (splitOption === 'pages') {
      formData.append('pages', pages)
    }

    if (splitOption === 'size') {
      formData.append('size', size)
    }

    setStatus('Separando...')
    try {
      const response = await fetch('http://localhost:8000/api/pdf/split/', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        throw new Error('Falha na requisição de separação');
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `separado_${file.name}.zip`)
      document.body.appendChild(link)
      link.click()
      link.remove()
      setStatus('Concluído!')
    } catch (error) {
      console.error('Falha na separação', error)
      setStatus('Falhou!')
    }
  }

  return (
    <div className="min-h-screen p-4 md:p-8">
      <div className="max-w-2xl mx-auto bg-white p-6 rounded-lg shadow-lg">
        <h1 className="text-2xl md:text-3xl font-bold mb-6 text-sedam-blue">Separar PDF</h1>
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

          <div className="mb-6">
            <label className="block text-gray-700 mb-2 font-semibold">2. Escolha como separar</label>
            <div className="flex flex-col sm:flex-row gap-4">
              <div 
                className={`flex-1 p-4 border rounded-lg cursor-pointer ${splitOption === 'pages' ? 'border-sedam-blue ring-2 ring-sedam-blue' : 'border-gray-300'}`}
                onClick={() => setSplitOption('pages')}
              >
                <input 
                  type="radio" 
                  id="pages" 
                  name="splitOption" 
                  value="pages" 
                  checked={splitOption === 'pages'} 
                  onChange={() => {}} 
                  className="form-radio h-5 w-5 text-sedam-blue"
                />
                <label htmlFor="pages" className="ml-3 text-lg font-medium text-gray-800">Por Páginas</label>
                <p className="text-sm text-gray-600 mt-1">Extraia um intervalo de páginas (ex: 1-5, 8, 10).</p>
              </div>
              <div 
                className={`flex-1 p-4 border rounded-lg cursor-pointer ${splitOption === 'size' ? 'border-sedam-blue ring-2 ring-sedam-blue' : 'border-gray-300'}`}
                onClick={() => setSplitOption('size')}
              >
                <input 
                  type="radio" 
                  id="size" 
                  name="splitOption" 
                  value="size" 
                  checked={splitOption === 'size'} 
                  onChange={() => {}} 
                  className="form-radio h-5 w-5 text-sedam-blue"
                />
                <label htmlFor="size" className="ml-3 text-lg font-medium text-gray-800">Por Tamanho</label>
                <p className="text-sm text-gray-600 mt-1">Divida o PDF em arquivos menores que um certo tamanho.</p>
              </div>
            </div>
          </div>

          {splitOption === 'pages' ? (
            <div className="mb-6">
              <label className="block text-gray-700 mb-2 font-semibold">Páginas a extrair</label>
              <input
                type="text"
                value={pages}
                onChange={(e) => setPages(e.target.value)}
                className="w-full px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-sedam-blue"
                placeholder="Ex: 1-3, 5, 7-9"
                required
              />
            </div>
          ) : (
            <div className="mb-6">
              <label className="block text-gray-700 mb-2 font-semibold">Tamanho máximo por arquivo (MB)</label>
              <input
                type="number"
                value={size}
                onChange={(e) => setSize(e.target.value)}
                className="w-full px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-sedam-blue"
                placeholder="20"
                required
              />
            </div>
          )}

          <button 
            type="submit" 
            className="w-full btn-primary py-3"
            disabled={!file || status === 'Separando...'}
          >
            {status === 'Separando...' ? 'Processando...' : '3. Separar e Baixar'}
          </button>
        </form>
        {status && status !== 'Separando...' && <p className="mt-6 text-center text-gray-700 font-medium">{status}</p>}
      </div>
    </div>
  )
}
