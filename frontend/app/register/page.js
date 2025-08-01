'use client'

import { useAuth } from '../../hooks/_useAuth'
import { useState } from 'react'
import Link from 'next/link'

export default function Register() {
  const { register } = useAuth({
    middleware: 'guest',
    redirectIfAuthenticated: '/_login',
  })

  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [errors, setErrors] = useState([])

  const handleSubmit = async (e) => {
    e.preventDefault()
    register({ name, email, password, setErrors })
  }

  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="bg-white p-8 rounded shadow-md w-full max-w-md">
        <h1 className="text-2xl font-bold mb-6 text-sedam-blue">Cadastre-se</h1>
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block text-gray-700">Nome</label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="w-full px-3 py-2 border rounded"
              required
            />
          </div>
          <div className="mb-4">
            <label className="block text-gray-700">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-3 py-2 border rounded"
              required
            />
          </div>
          <div className="mb-6">
            <label className="block text-gray-700">Senha</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-3 py-2 border rounded"
              required
            />
          </div>
          <button type="submit" className="w-full btn-primary">
            Registrar
          </button>
          <p className="text-center mt-4">
            Já tem uma conta?{" "}
            <Link href="/_login" className="text-sedam-blue hover:underline">
              Faça login
            </Link>
          </p>
        </form>
      </div>
    </div>
  )
}