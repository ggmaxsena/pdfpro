import { useState } from 'react'

interface Props {
  endpoint: string          // ex.: "/api/excel/anonymize/name/"
  label: string             // ex.: "Anonimizar Nome"
  accept?: string           // ex.: ".xlsx"
}

export default function UploadButton({ endpoint, label, accept = '*' }: Props) {
  const [file, setFile] = useState<File | null>(null)
  const [busy, setBusy] = useState(false)

  const send = async () => {
    if (!file) return
    const fd = new FormData()
    fd.append('file', file)

    setBusy(true)
    try {
      const res = await fetch(endpoint, {
        method: 'POST',
        body: fd,
      })
      if (!res.ok) throw new Error('upload failed')

      const blob = await res.blob()
      const url  = URL.createObjectURL(blob)
      const a    = document.createElement('a')
      a.href = url
      a.download = file.name
      a.click()
      URL.revokeObjectURL(url)
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="flex gap-2">
      <input
        type="file"
        accept={accept}
        onChange={e => setFile(e.target.files?.[0] ?? null)}
      />
      <button
        onClick={send}
        disabled={!file || busy}
        className="btn-primary px-4 py-2"
      >
        {busy ? '...' : label}
      </button>
    </div>
  )
}