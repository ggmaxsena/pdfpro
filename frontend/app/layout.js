import './globals.css'

export const metadata = {
  title: 'PDF Pro',
  description: 'Anonymize and manage your PDFs',
}

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
