import { Routes, Route } from 'react-router-dom'
import MainLayout from './components/Layout/MainLayout'
import Dashboard from './components/Dashboard/Dashboard'
import RouteComparison from './components/RouteComparison/RouteComparison'
import CertificateViewer from './components/Blockchain/CertificateViewer'
import ErrorBoundary from './components/Common/ErrorBoundary'

function App() {
  return (
    <ErrorBoundary>
      <MainLayout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/route-comparison" element={<RouteComparison />} />
          <Route path="/blockchain" element={<CertificateViewer />} />
        </Routes>
      </MainLayout>
    </ErrorBoundary>
  )
}

export default App

