import React, { useState } from 'react';
import { Typography, Box, Tabs, Tab, Alert } from '@mui/material';
import WalmartDemo from '../components/Demos/WalmartDemo';
import QuickDemo from '../components/Demos/QuickDemos';

/**
 * DemoPage - COMPLETE FIXED VERSION for full-width display
 * Purpose: 3-minute hackathon demo and quick 90-second version
 * FIXED: Removes all width constraints to ensure true full-width display
 */
const DemoPage: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);

  return (
    <Box sx={{ 
      width: '100vw', // Use full viewport width
      minHeight: '100vh',
      overflow: 'hidden', // Prevent horizontal scroll
      boxSizing: 'border-box'
    }}>
      {/* ✅ UPDATED: Hero Section with HomePage styling */}
      <Box 
        sx={{ 
          textAlign: 'center', 
          mb: 6, 
          pt: 4,
          // ✅ ADDED: Hero background image like HomePage
          backgroundImage: 'linear-gradient(rgba(255, 249, 230, 0.8), rgba(255, 249, 230, 0.9)), url(https://images.unsplash.com/photo-1558494949-ef010cbdcc31?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2134&q=80)',
          backgroundSize: 'cover',
          backgroundPosition: 'center',
          borderRadius: 4,
          py: 8,
          position: 'relative',
          px: { xs: 2, sm: 3, md: 4 },
        }}
      >
        {/* ✅ UPDATED: Cinzel Title exactly like HomePage */}
        <Typography 
          variant="h1" 
          className="quantum-title fade-in"
          sx={{ 
            mb: 3,
            fontFamily: '"Cinzel", "Times New Roman", serif !important',
            fontSize: { xs: '3rem', sm: '4rem', md: '4.5rem' },
            fontWeight: '400 !important',
            color: '#000000 !important',
            textAlign: 'center',
            letterSpacing: '3px',
            textShadow: '0 0 20px rgba(0, 0, 0, 0.3)',
            position: 'relative',
            background: 'linear-gradient(45deg, #000000, #333333, #000000)',
            backgroundSize: '300% 300%',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            backgroundClip: 'text',
            animation: 'luxuryGlow 3s ease-in-out infinite, textShimmer 4s ease-in-out infinite',
            '@media (max-width: 600px)': {
              fontSize: '2.5rem',
              letterSpacing: '2px',
            },
          }}
        >
          QuantumEco Intelligence Demo Hub
        </Typography>

        {/* ✅ UPDATED: Subtitle exactly like HomePage */}
        <Typography 
          variant="h5" 
          className="quantum-subtitle fade-in"
          sx={{ 
            mb: 4, 
            maxWidth: 800, 
            mx: 'auto',
            animationDelay: '0.3s',
            color: '#808080',
            fontFamily: '"Myriad Pro", "Whitney", "Avenir Next", sans-serif',
            fontSize: { xs: '1.2rem', sm: '1.5rem' },
            lineHeight: 1.5,
            fontWeight: 500,
          }}
        >
          Live demonstration of quantum-inspired logistics optimization with real-time API integration, 
          blockchain verification, and $4.2B Walmart impact potential
        </Typography>

        {/* ✅ UPDATED: Impact Statement like HomePage */}
        <Typography 
          variant="h6" 
          className="quantum-impact fade-in"
          sx={{ 
            mb: 5,
            animationDelay: '0.6s',
            color: '#00A651',
            fontWeight: 700,
            fontSize: { xs: '1.1rem', sm: '1.3rem' },
          }}
        >
          25% Cost Reduction • 35% Carbon Savings • Built in 48 Hours
        </Typography>
      </Box>

      {/* Demo Mode Alert */}
      <Box sx={{ px: { xs: 2, sm: 3, md: 4 }, mb: 3 }}>
        <Alert 
          severity="info" 
          sx={{ 
            width: '100%',
            p: 3,
            fontSize: '1.1rem',
            fontWeight: 500,
            borderRadius: 2
          }}
        >
          🎬 <strong>Demo Mode Active</strong> - Live API integration with real-time optimization and blockchain verification
        </Alert>
      </Box>

      {/* Demo Selection Section */}
      <Box sx={{ 
        width: '100%',
        mb: 4,
        px: { xs: 2, sm: 3, md: 4 }
      }}>
        <Typography variant="h4" sx={{ fontWeight: 'bold', textAlign: 'center', mb: 3 }}>
          📊 Select Demo Experience
        </Typography>
        
        {/* Full-width tabs */}
        <Box sx={{ width: '100%', mb: 3 }}>
          <Tabs 
            value={tabValue} 
            onChange={(_, val) => setTabValue(val)} 
            variant="fullWidth"
            sx={{ 
              width: '100%',
              '& .MuiTab-root': {
                fontSize: '1.1rem',
                fontWeight: 600,
                minHeight: 60,
                px: 4,
                textTransform: 'none'
              },
              '& .MuiTabs-indicator': {
                height: 3,
                borderRadius: '3px 3px 0 0'
              }
            }}
          >
            <Tab 
              label="🏆 FULL DEMO (3 MINUTES)" 
              sx={{ 
                border: '2px solid transparent',
                borderRadius: '8px 8px 0 0',
                mx: 0.5,
                '&.Mui-selected': {
                  border: '2px solid',
                  borderColor: 'primary.main',
                  bgcolor: 'primary.50',
                  borderBottom: 'none'
                }
              }}
            />
            <Tab 
              label="⚡ QUICK DEMO (90 SECONDS)" 
              sx={{ 
                border: '2px solid transparent',
                borderRadius: '8px 8px 0 0',
                mx: 0.5,
                '&.Mui-selected': {
                  border: '2px solid',
                  borderColor: 'secondary.main',
                  bgcolor: 'secondary.50',
                  borderBottom: 'none'
                }
              }}
            />
          </Tabs>
        </Box>

        {/* Tab Content Descriptions */}
        {tabValue === 0 && (
          <Alert severity="success" sx={{ 
            p: 3, 
            borderRadius: 2,
            bgcolor: 'success.50',
            border: '2px solid',
            borderColor: 'success.main',
            width: '100%'
          }}>
            <Typography variant="h6" sx={{ fontWeight: 'bold', mb: 1 }}>
              🎯 Complete 3-Minute Hackathon Presentation
            </Typography>
            <Typography variant="body1">
              Full demonstration including problem statement, live optimization comparison, 
              carbon impact analysis, blockchain verification, and Walmart scale projections.
              Perfect for investor presentations and technical demonstrations.
            </Typography>
          </Alert>
        )}

        {tabValue === 1 && (
          <Alert severity="warning" sx={{ 
            p: 3, 
            borderRadius: 2,
            bgcolor: 'warning.50',
            border: '2px solid',
            borderColor: 'warning.main',
            width: '100%'
          }}>
            <Typography variant="h6" sx={{ fontWeight: 'bold', mb: 1 }}>
              ⚡ Rapid 90-Second Overview
            </Typography>
            <Typography variant="body1">
              Condensed demonstration focusing on key metrics: 25% cost reduction, 
              35% carbon savings, and blockchain verification. Ideal for quick pitches 
              and technical overviews.
            </Typography>
          </Alert>
        )}
      </Box>

      {/* Demo Content - CRITICAL FIX: No Container wrapper */}
      <Box sx={{ 
        width: '100%',
        minHeight: '70vh',
        overflow: 'hidden'
      }}>
        {tabValue === 0 && <WalmartDemo />}
        {tabValue === 1 && <QuickDemo />}
      </Box>

      {/* Footer Stats */}
      <Box sx={{ mt: 6, textAlign: 'center', width: '100%', px: { xs: 2, sm: 3, md: 4 }, pb: 4 }}>
        <Typography variant="h6" sx={{ mb: 3 }}>
          🏆 Demo Performance Metrics
        </Typography>
        <Box sx={{ display: 'flex', justifyContent: 'center', gap: 4, flexWrap: 'wrap' }}>
          <Box>
            <Typography variant="h4" color="success.main" sx={{ fontWeight: 'bold' }}>3min</Typography>
            <Typography variant="body2">Full Demo Duration</Typography>
          </Box>
          <Box>
            <Typography variant="h4" color="info.main" sx={{ fontWeight: 'bold' }}>90s</Typography>
            <Typography variant="body2">Quick Demo Duration</Typography>
          </Box>
          <Box>
            <Typography variant="h4" color="warning.main" sx={{ fontWeight: 'bold' }}>Live</Typography>
            <Typography variant="body2">API Integration</Typography>
          </Box>
          <Box>
            <Typography variant="h4" color="primary.main" sx={{ fontWeight: 'bold' }}>Real</Typography>
            <Typography variant="body2">Blockchain Verification</Typography>
          </Box>
        </Box>
      </Box>
    </Box>
  );
};

export default DemoPage;
