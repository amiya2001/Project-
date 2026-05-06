import type { Metadata } from 'next';
export const metadata: Metadata = {title: 'PAKS', description: 'Personal AI Knowledge System'};
export default function RootLayout({children}: {children: React.ReactNode}) {
  return (
    <html lang="en">
      <body style={{margin:0,padding:0,height:'100vh',overflow:'hidden'}}>
        {children}
      </body>
    </html>
  );
}