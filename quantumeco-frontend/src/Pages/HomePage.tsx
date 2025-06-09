import React from 'react';
import { Container, Typography, Box, Button, Card, CardContent } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { PlayArrow, Dashboard, Route, Security } from '@mui/icons-material';

/**
 * HomePage - Main landing page with navigation to key MVP features
 * Purpose: Entry point for hackathon demo and daily use
 */
const HomePage: React.FC = () => {
  const navigate = useNavigate();

  const mvpFeatures = [
    {
      title: '🎬 Live Demo',
      description: '3-minute hackathon presentation with live API calls',
      path: '/demo',
      icon: <PlayArrow />,
      color: 'primary.main'
    },
    {
      title: '📊 Analytics Dashboard', 
      description: 'Real-time performance metrics and system health',
      path: '/dashboard',
      icon: <Dashboard />,
      color: 'info.main'
    },
    {
      title: '🛣️ Route Optimizer',
      description: 'Quantum-inspired optimization with before/after comparison',
      path: '/optimize',
      icon: <Route />,
      color: 'success.main'
    },
    {
      title: '🔗 Blockchain Verification',
      description: 'Live certificate generation and environmental trust tokens',
      path: '/certificates',
      icon: <Security />,
      color: 'warning.main'
    }
  ];

  return (
    <Container maxWidth="xl" sx={{ py: 4 }}>
      {/* Hero Section */}
      <Box sx={{ textAlign: 'center', mb: 6 }}>
        <Typography variant="h2" sx={{ fontWeight: 'bold', mb: 2, color: 'primary.main' }}>
          🚀 QuantumEco Intelligence
        </Typography>
        <Typography variant="h5" sx={{ mb: 3, color: 'text.secondary', maxWidth: 800, mx: 'auto' }}>
          Quantum-inspired logistics optimization with 25% cost reduction, 35% carbon savings, 
          and blockchain-verified sustainability certificates
        </Typography>
        <Typography variant="h6" sx={{ mb: 4, color: 'success.main', fontWeight: 'bold' }}>
          $4.2B Walmart Impact Potential • Built in 48 Hours • Production Ready
        </Typography>
        
        <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center', flexWrap: 'wrap' }}>
          <Button 
            variant="contained" 
            size="large" 
            startIcon={<PlayArrow />}
            onClick={() => navigate('/demo')}
            sx={{ py: 2, px: 4 }}
          >
            Watch Live Demo
          </Button>
          <Button 
            variant="outlined" 
            size="large" 
            startIcon={<Dashboard />}
            onClick={() => navigate('/dashboard')}
            sx={{ py: 2, px: 4 }}
          >
            View Dashboard
          </Button>
        </Box>
      </Box>

      {/* ✅ MVP Features - Converted to Flexbox */}
      <Box sx={{ 
        display: 'flex', 
        flexWrap: 'wrap',
        gap: 4,
        mb: 6
      }}>
        {mvpFeatures.map((feature, index) => (
          <Box 
            key={index}
            sx={{ 
              flex: { xs: '1 1 100%', md: '1 1 calc(50% - 16px)' }, // 100% on mobile, 50% on desktop (minus gap)
              minWidth: { xs: '100%', md: 'calc(50% - 16px)' }
            }}
          >
            <Card 
              sx={{ 
                height: '100%', 
                cursor: 'pointer',
                transition: 'transform 0.2s',
                '&:hover': { transform: 'translateY(-4px)' }
              }}
              onClick={() => navigate(feature.path)}
            >
              <CardContent sx={{ p: 4 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Box sx={{ color: feature.color, mr: 2 }}>
                    {feature.icon}
                  </Box>
                  <Typography variant="h5" sx={{ fontWeight: 'bold' }}>
                    {feature.title}
                  </Typography>
                </Box>
                <Typography variant="body1" color="text.secondary">
                  {feature.description}
                </Typography>
              </CardContent>
            </Card>
          </Box>
        ))}
      </Box>

      {/* Quick Stats */}
      <Box sx={{ mt: 6, textAlign: 'center' }}>
        <Typography variant="h6" sx={{ mb: 3 }}>
          🏆 Proven Impact Metrics
        </Typography>
        <Box sx={{ display: 'flex', justifyContent: 'center', gap: 4, flexWrap: 'wrap' }}>
          <Box>
            <Typography variant="h4" color="success.main" sx={{ fontWeight: 'bold' }}>25%</Typography>
            <Typography variant="body2">Cost Reduction</Typography>
          </Box>
          <Box>
            <Typography variant="h4" color="info.main" sx={{ fontWeight: 'bold' }}>35%</Typography>
            <Typography variant="body2">Carbon Savings</Typography>
          </Box>
          <Box>
            <Typography variant="h4" color="warning.main" sx={{ fontWeight: 'bold' }}>$1.58B</Typography>
            <Typography variant="body2">Walmart Annual Savings</Typography>
          </Box>
          <Box>
            <Typography variant="h4" color="primary.main" sx={{ fontWeight: 'bold' }}>48hrs</Typography>
            <Typography variant="body2">Development Time</Typography>
          </Box>
        </Box>
      </Box>
    </Container>
  );
};

export default HomePage;
