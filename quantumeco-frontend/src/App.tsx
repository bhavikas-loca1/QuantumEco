import React, { useEffect, useState } from 'react';
import { Routes, Route } from 'react-router-dom';
import { Box } from '@mui/material';
import ErrorBoundary from './components/Common/ErrorBoundary';
import MainLayout from './components/Layout/MainLayout';
import LoadingSpinner from './components/Common/LoadingSpinner';

// Page Components
import HomePage from './Pages/HomePage';
import DemoPage from './Pages/DemoPage';
import DashboardPage from './Pages/DashboardAnalytics'
import OptimizationPage from './Pages/OptimizationPage';
import CertificatesPage from './Pages/CertificatePage';

// Direct component imports
import Dashboard from './components/Dashboard/Dashboard';
import RouteOptimizer from './components/Routes/RouteOptimizer';
import WalmartDemo from './components/Demos/WalmartDemo';
import QuickDemo from './components/Demos/QuickDemos'
import CertificateViewer from './components/Blockchain/CertificateViewer';

import { getHealthCheck, isApiAvailable } from './Services/api';

function App() {
  const [systemStatus, setSystemStatus] = useState<'loading' | 'healthy' | 'error'>('loading');

  useEffect(() => {
    checkSystemHealth();
  }, []);

  const checkSystemHealth = async () => {
    try {
      const apiAvailable = await isApiAvailable();
      setSystemStatus(apiAvailable ? 'healthy' : 'error');
    } catch (error) {
      setSystemStatus('error');
    }
  };

  if (systemStatus === 'loading') {
    return (
      <Box sx={{ 
        backgroundColor: '#FFF9E6', 
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center'
      }}>
        <LoadingSpinner message="Loading..." />
      </Box>
    );
  }

  return (
    <Box sx={{ 
      backgroundColor: '#FFF9E6', 
      minHeight: '100vh', 
      width: '100%',
    }}>
      <ErrorBoundary>
        <MainLayout>
          <React.Suspense fallback={<LoadingSpinner message="Loading page..." />}>
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/demo" element={<DemoPage />} />
              <Route path="/dashboard" element={<DashboardPage />} />
              <Route path="/optimize" element={<OptimizationPage />} />
              <Route path="/certificates" element={<CertificatesPage />} />
              <Route path="/analytics" element={<Dashboard />} />
              <Route path="*" element={<HomePage />} />
            </Routes>
          </React.Suspense>
        </MainLayout>
      </ErrorBoundary>
    </Box>
  );
}

export default App;
