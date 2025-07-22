import './globals.css'
import Header from '../components/Header'
import Footer from '../components/Footer'

export const metadata = {
  title: 'PDF Pro - Anonimize e Gerencie seus PDFs',
  description: 'Anonimize e gerencie seus documentos PDF de forma fácil e segura.',
}

export default function RootLayout({ children }) {
  return (
    <html lang="pt-br">
      <body>
        <Header />
        <main className="container mx-auto p-4">
          {children}
        </main>
        <Footer />
      </body>
    </html>
  )
}