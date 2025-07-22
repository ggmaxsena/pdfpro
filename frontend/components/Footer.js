// components/Footer.js
import Link from 'next/link';
import { Github, Facebook, FileText, Heart } from 'lucide-react';

/**
 * Rodapé com animações leves, links úteis e sem endereço físico.
 * Tailwind + lucide-react (já utilizado no projeto).
 */
export default function Footer() {
  const year = new Date().getFullYear();

  // Lista de links exibidos como ícones
  const links = [
    { href: 'https://facebook.com/your-page', icon: Facebook, label: 'Facebook' },
    { href: '/docs', icon: FileText, label: 'Documentação' },
  ];

  return (
    <footer className="bg-gradient-to-r from-sedam-dark to-sedam-light text-white py-10 mt-12">
      <div className="container mx-auto flex flex-col items-center gap-6">
        {/* Direitos autorais */}
        <p className="text-sm">
          &copy; {year} Box Things. Todos os direitos reservados.
        </p>

        {/* Ícones sociais/documentação */}
        <ul className="flex gap-6">
          {links.map(({ href, icon: Icon, label }) => (
            <li key={label}>
              <Link
                href={href}
                aria-label={label}
                className="transition-transform hover:-translate-y-1 focus:outline-none"
                target={href.startsWith('http') ? '_blank' : undefined}
                rel={href.startsWith('http') ? 'noopener noreferrer' : undefined}
              >
                <Icon className="h-5 w-5" />
              </Link>
            </li>
          ))}
        </ul>

        {/* Assinatura sutil */}
        <p className="flex items-center gap-1 text-xs">
          Feito com <Heart className="h-3 w-3 animate-pulse" /> por Box Things
        </p>
      </div>
    </footer>
  );
}