'use client'

import { useState } from 'react'

const DIRECT_IDENTIFIERS = [
  "nome", "cpf", "rg", "cnh", "passport", "titulo_eleitor", "pis_pasep",
  "email", "telefone", "endereco", "cep", "ip", "mac", "imei", "geoloc", "placa"
]
const SENSITIVE_IDENTIFIERS = [
  "saude", "religiao", "opiniao_politica", "sindicato", "biometria"
]

export default function Anonymize() {
  const [file, setFile] = useState(null)
  const [status, setStatus] = useState('')
  const [preview, setPreview] = useState(null)
  const [rules, setRules] = useState({})

  const handleFileChange = (e) => {
    setFile(e.target.files[0])
    setPreview(null)
    setRules({})
  }

  const handlePreview = async () => {
    if (!file) return

    const formData = new FormData()
    formData.append('file', file)

    setStatus('Gerando pré-visualização...')
    try {
      const response = await fetch('http://localhost:8000/api/anonimize/preview/', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) throw new Error('Falha na requisição de pré-visualização')

      const data = await response.json()
      setPreview(data)

      const initialRules = data.tokens_detected.reduce((acc, token) => {
        const isSensitive = SENSITIVE_IDENTIFIERS.includes(token)
        const isDirect    = DIRECT_IDENTIFIERS.includes(token)
        acc[token] = isSensitive || isDirect
        return acc
      }, {})
      setRules(initialRules)
      setStatus('')
    } catch (error) {
      console.error('Pré-visualização falhou', error)
      setStatus('Falha ao gerar pré-visualização!')
    }
  }

  const handleAnonymize = async () => {
    if (!file) return

    const formData = new FormData()
    formData.append('file', file)
    formData.append('rules', JSON.stringify(rules))

    setStatus('Anonimizando...')
    try {
      const response = await fetch('http://localhost:8000/api/anonimize/', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) throw new Error('Falha na solicitação de anonimização')

      const blob = await response.blob()
      const url  = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href  = url
      link.setAttribute('download', `anonimizado_${file.name}`)
      document.body.appendChild(link)
      link.click()
      link.remove()
      setStatus('Concluído!')
    } catch (error) {
      console.error('Anonimização falhou', error)
      setStatus('Falhou!')
    }
  }

  const renderTokenCheckboxes = (tokenList) => (
    tokenList.map(token => (
      <div key={token} className="mr-4 mb-2">
        <input
          type="checkbox"
          id={token}
          checked={rules[token] || false}
          onChange={(e) => setRules({ ...rules, [token]: e.target.checked })}
          className="form-checkbox h-5 w-5 text-sedam-blue"
        />
        <label htmlFor={token} className="ml-2 text-gray-700">{token}</label>
      </div>
    ))
  )

  return (
    <div className="min-h-screen p-4 md:p-8">
      <div className="max-w-2xl mx-auto bg-white p-6 rounded-lg shadow-lg">
        <h1 className="text-2xl md:text-3xl font-bold mb-6 text-sedam-blue">Anonimizar Planilha</h1>

        <div className="mb-4">
          <label className="block text-gray-700 mb-2 font-semibold">1. Envie seu arquivo .xlsx</label>
          <input
            type="file"
            onChange={handleFileChange}
            accept=".xlsx"
            className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-sedam-blue"
          />
        </div>

        <button
          onClick={handlePreview}
          className="w-full btn-primary py-2.5 mb-4"
          disabled={!file}
        >
          2. Pré-visualizar Dados
        </button>

        {preview && (
          <div>
            <h2 className="text-xl md:text-2xl font-bold mb-4 text-sedam-blue">3. Regras de Anonimização</h2>

            <div className="bg-gray-50 p-4 rounded-lg">
              <h3 className="text-lg font-semibold mb-3 text-gray-800">
                Identificadores Comuns (pré-selecionados)
              </h3>
              <div className="flex flex-wrap">
                {renderTokenCheckboxes(
                  preview.tokens_detected.filter(
                    t => DIRECT_IDENTIFIERS.includes(t) || SENSITIVE_IDENTIFIERS.includes(t)
                  )
                )}
              </div>

              <h3 className="text-lg font-semibold mt-4 mb-3 text-gray-800">Outros Tokens Detectados</h3>
              <div className="flex flex-wrap">
                {renderTokenCheckboxes(
                  preview.tokens_detected.filter(
                    t => !DIRECT_IDENTIFIERS.includes(t) && !SENSITIVE_IDENTIFIERS.includes(t)
                  )
                )}
              </div>
            </div>

            <button
              onClick={handleAnonymize}
              className="w-full btn-primary mt-6 py-2.5"
            >
              4. Anonimizar e Baixar
            </button>
          </div>
        )}

        {status && <p className="mt-6 text-center text-gray-700 font-medium">{status}</p>}
      </div>
    </div>
  )
}
