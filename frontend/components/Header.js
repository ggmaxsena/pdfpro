'use client'
import { useState } from 'react';
import Link from 'next/link';

export default function Header() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <header className="bg-sedam text-white p-4 shadow-md">
      <div className="container mx-auto flex justify-between items-center">
        <Link href="/" className="flex items-center">
          <img src="http://localhost:8000/media/logo.png" alt="Logo PDF Pro" className="h-12 mr-2 filter drop-shadow-[0_2px_2px_rgba(255,255,255,0.4)]" />
          <span className="text-xl font-bold"></span>
        </Link>
        
        {/* Desktop Navigation */}
        <nav className="hidden md:flex space-x-4">
          <Link href="/anonimizar" className="hover:bg-sedam-dark px-3 py-2 rounded">Anonimizar</Link>
          <Link href="/pdf/comprimir" className="hover:bg-sedam-dark px-3 py-2 rounded">Comprimir PDF</Link>
          <Link href="/pdf/separar" className="hover:bg-sedam-dark px-3 py-2 rounded">Separar PDF</Link>
          <Link href="/excel/anonimizar-nome" className="hover:bg-sedam-dark px-3 py-2 rounded">Anonimizar Nome</Link>
          <Link href="/login" className="hover:bg-sedam-dark px-3 py-2 rounded">Login</Link>
          <Link href="/register" className="hover:bg-sedam-dark px-3 py-2 rounded">Registrar</Link>
        </nav>

        {/* Mobile Menu Button */}
        <button 
          className="md:hidden text-white text-2xl"
          onClick={() => setIsMenuOpen(!isMenuOpen)}
        >
          &#9776; {/* Hamburger icon */}
        </button>
      </div>

      {/* Mobile Menu */}
      {isMenuOpen && (
        <nav className="md:hidden mt-4">
          <ul className="flex flex-col space-y-2">
            <li><Link href="/anonimizar" className="block hover:bg-sedam-dark px-4 py-2 rounded">Anonimizar</Link></li>
            <li><Link href="/pdf/comprimir" className="block hover:bg-sedam-dark px-4 py-2 rounded">Comprimir PDF</Link></li>
            <li><Link href="/pdf/separar" className="block hover:bg-sedam-dark px-4 py-2 rounded">Separar PDF</Link></li>
            <li><Link href="/excel/anonimizar-nome" className="block hover:bg-sedam-dark px-4 py-2 rounded">Anonimizar Nome</Link></li>
            <li><Link href="/login" className="block hover:bg-sedam-dark px-4 py-2 rounded">Login</Link></li>
            <li><Link href="/register" className="block hover:bg-sedam-dark px-4 py-2 rounded">Registrar</Link></li>
          </ul>
        </nav>
      )}
    </header>
  );
}
