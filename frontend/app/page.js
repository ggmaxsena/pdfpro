'use client'

import Link from 'next/link'

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-4">
      <div className="bg-white p-6 md:p-8 rounded-lg shadow-lg w-full max-w-4xl text-center">
        <img src="http://localhost:8000/media/logo.png" alt="Logo" className="h-24 mx-auto mb-4" />
        <h1 className="text-3xl md:text-4xl font-bold mb-4 text-sedam-blue">Bem-vindo ao PDF Pro</h1>
        <p className="text-md md:text-lg text-gray-700 mb-8">Sua solução completa para gerenciamento de PDFs.</p>
        
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6">
          <Link href="/anonimizar" className="btn-primary py-3 md:py-2"> 
            Anonimizar PDF
          </Link>
          <Link href="/pdf/comprimir" className="btn-primary py-3 md:py-2">
            Comprimir PDF
          </Link>
          <Link href="/pdf/separar" className="btn-primary py-3 md:py-2">
            Separar PDF
          </Link>
          <Link href="/diarias" className="btn-primary py-3 md:py-2">
            Diárias
          </Link>
        </div>
      </div>
    </div>
  )
}
