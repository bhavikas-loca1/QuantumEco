import React, { useEffect, useState } from 'react';
import { Routes, Route, BrowserRouter } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { Alert, Snackbar } from '@mui/material';
import ErrorBoundary from './components/Common/ErrorBoundary';
import MainLayout from './components/Layout/MainLayout'; // ✅ Fixed path
import LoadingSpinner from './components/Common/LoadingSpinner';

// ✅ Page Components (Essential MVP Pages)
import HomePage from './Pages/HomePage';
import DemoPage from './Pages/DemoPage';
import DashboardPage from './Pages/DashboardAnalytics'
import OptimizationPage from './Pages/OptimizationPage';
import CertificatesPage from './Pages/CertificatePage';

// ✅ Direct component imports for backward compatibility
import Dashboard from './components/Dashboard/Dashboard';
import RouteOptimizer from './components/Routes/RouteOptimizer';
import WalmartDemo from './components/Demos/WalmartDemo'; // ✅ Fixed path
import QuickDemo from './components/Demos/QuickDemos'
import CertificateViewer from './components/Blockchain/CertificateViewer';

import { getHealthCheck, isApiAvailable } from './Services/api'; // Fixed path (lowercase)

// ✅ Enhanced theme for demo presentation
const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#4caf50',
    },
    success: {
      main: '#4caf50',
    },
    info: {
      main: '#2196f3',
    },
    warning: {
      main: '#ff9800',
    },
    error: {
      main: '#f44336',
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    h4: {
      fontWeight: 600,
    },
    h5: {
      fontWeight: 600,
    },
    h6: {
      fontWeight: 500,
    },
  },
  components: {
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 12,
          boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
          transition: 'all 0.3s ease',
          '&:hover': {
            boxShadow: '0 4px 16px rgba(0,0,0,0.15)',
          },
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          textTransform: 'none',
          fontWeight: 500,
          transition: 'all 0.2s ease',
        },
      },
    },
  },
});

function App() {
  // ✅ System status monitoring for demo
  const [systemStatus, setSystemStatus] = useState<'loading' | 'healthy' | 'error'>('loading');
  const [statusMessage, setStatusMessage] = useState<string>('');
  const [showStatusAlert, setShowStatusAlert] = useState(false);

  // ✅ Check system health on startup
  useEffect(() => {
    checkSystemHealth();
  }, []);

  const checkSystemHealth = async () => {
    try {
      // Check API availability
      const apiAvailable = await isApiAvailable();
      
      if (apiAvailable) {
        // Get detailed health check
        const healthData = await getHealthCheck();
        
        if (healthData.status === 'healthy') {
          setSystemStatus('healthy');
          setStatusMessage('✅ All systems operational - Ready for demo!');
        } else {
          setSystemStatus('error');
          setStatusMessage(`⚠️ System status: ${healthData.status}`);
        }
      } else {
        setSystemStatus('error');
        setStatusMessage('❌ Backend API not available - Using demo mode');
      }
      
      setShowStatusAlert(true);
    } catch (error) {
      setSystemStatus('error');
      setStatusMessage('❌ System check failed - Demo mode active');
      setShowStatusAlert(true);
      console.warn('System health check failed:', error);
    }
  };

  // ✅ Show loading screen during system check
  if (systemStatus === 'loading') {
    return (
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <LoadingSpinner message="Initializing QuantumEco Intelligence..." />
      </ThemeProvider>
    );
  }

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <ErrorBoundary>
          <MainLayout>
            <React.Suspense fallback={<LoadingSpinner message="Loading page..." />}>
              <Routes>
                {/* ✅ Main Landing Page */}
                <Route path="/" element={<HomePage />} />
                
                {/* ✅ Demo Hub - Primary demo presentation */}
                <Route path="/demo" element={<DemoPage />} />
                <Route path="/api/demo/walmart-nyc" element={<WalmartDemo />} />
                <Route path="/api/demo/quick" element={<QuickDemo />} />
                
                {/* ✅ Core Dashboard */}
                <Route path="/dashboard" element={<DashboardPage />} />
                
                {/* ✅ Route Optimization */}
                <Route path="/optimize" element={<OptimizationPage />} />
                <Route path="/routes" element={<RouteOptimizer />} />
                
                {/* ✅ Blockchain Verification */}
                <Route path="/certificates" element={<CertificatesPage />} />
                <Route path="/blockchain" element={<CertificateViewer />} />
                
                {/* ✅ Legacy/Alias Routes for Backward Compatibility */}
                <Route path="/analytics" element={<Dashboard />} />
                <Route path="/route-optimizer" element={<RouteOptimizer />} />
                
                {/* ✅ Direct Component Access (for development/testing) */}
                <Route path="/components/dashboard" element={<Dashboard />} />
                <Route path="/components/optimizer" element={<RouteOptimizer />} />
                <Route path="/components/certificates" element={<CertificateViewer />} />
                
                {/* ✅ Demo Components Access */}
                <Route path="/demos/walmart" element={<WalmartDemo />} />
                <Route path="/demos/quick" element={<QuickDemo />} />
                
                {/* ✅ Fallback to HomePage (better UX than dashboard) */}
                <Route path="*" element={<HomePage />} />
              </Routes>
            </React.Suspense>
          </MainLayout>

          {/* ✅ System Status Notification for Demo */}
          <Snackbar
            open={showStatusAlert}
            autoHideDuration={6000}
            onClose={() => setShowStatusAlert(false)}
            anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
          >
            <Alert 
              onClose={() => setShowStatusAlert(false)} 
              severity={systemStatus === 'healthy' ? 'success' : 'warning'}
              variant="filled"
              sx={{ 
                minWidth: 400,
                '& .MuiAlert-message': {
                  fontSize: '1rem',
                  fontWeight: 500,
                }
              }}
            >
              {statusMessage}
            </Alert>
          </Snackbar>
      </ErrorBoundary>
    </ThemeProvider>
  );
}

export default App;
