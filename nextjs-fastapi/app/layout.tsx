import './globals.css'
import { Inter } from 'next/font/google'
import NavBar from './components/NavBar'
const inter = Inter({ subsets: ['latin'] })

export const metadata = {
  title: 'A+I',
  description: 'Teacher\'s best friend'
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
    <body className={inter.className}>
      <div className="flex flex-col min-h-screen">
        <NavBar />
        <main className="flex-grow">
          {children}
        </main>
      </div>
    </body>
  </html>
  )
}
