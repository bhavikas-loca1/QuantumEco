import React from 'react';
import { 
  Container, 
  Typography, 
  Box, 
  Button, 
  Card, 
  CardContent,
  CardActions,
  Chip 
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { 
  PlayArrow, 
  Dashboard, 
  Route, 
  Security,
  TrendingUp,
  Speed,
  Nature,
  AttachMoney 
} from '@mui/icons-material';

/**
 * HomePage - Luxurious landing page with animated Walmart branding (Flexbox Layout)
 * Purpose: Professional entry point for hackathon demo with enhanced UX
 */
const HomePage: React.FC = () => {
  const navigate = useNavigate();

  const mvpFeatures = [
    {
      title: 'Live Demo',
      description: '3-minute hackathon presentation with live API calls and real-time optimization',
      path: '/demo',
      icon: <PlayArrow className="luxury-icon" />,
      chipLabel: 'Interactive',
      chipColor: 'primary',
      // ✅ ADDED: Demo/presentation image
      image: 'https://images.unsplash.com/photo-1551434678-e076c223a692?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80'
    },
    {
      title: 'Analytics Dashboard', 
      description: 'Real-time performance metrics, system health monitoring, and quantum insights',
      path: '/dashboard',
      icon: <Dashboard className="luxury-icon" />,
      chipLabel: 'Live Data',
      chipColor: 'success',
      // ✅ ADDED: Analytics/dashboard image
      image: 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80'
    },
    {
      title: 'Route Optimizer',
      description: 'Quantum-inspired optimization with before/after comparison and impact analysis',
      path: '/optimize',
      icon: <Route className="luxury-icon" />,
      chipLabel: 'AI Powered',
      chipColor: 'info',
      // ✅ ADDED: Supply chain/logistics image
      image: 'https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80'
    },
    {
      title: 'Blockchain Verification',
      description: 'Live certificate generation, environmental trust tokens, and carbon credit trading',
      path: '/certificates',
      icon: <Security className="luxury-icon" />,
      chipLabel: 'Verified',
      chipColor: 'success',
      // ✅ ADDED: Blockchain/security image
      image: 'https://images.unsplash.com/photo-1639762681485-074b7f938ba0?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80'
    }
  ];

  const impactMetrics = [
    { 
      value: '25%', 
      label: 'Cost Reduction', 
      icon: <AttachMoney />, 
      color: '#00A651',
      // ✅ ADDED: Cost reduction image
      image: 'https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80'
    },
    { 
      value: '35%', 
      label: 'Carbon Savings', 
      icon: <Nature />, 
      color: '#0071CE',
      // ✅ ADDED: Environmental/green image
      image: 'https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80'
    },
    { 
      value: '$4.2B', 
      label: 'Walmart Impact', 
      icon: <TrendingUp />, 
      color: '#FFC220',
      // ✅ ADDED: Financial growth image
      image: 'https://images.unsplash.com/photo-1579621970563-ebec7560ff3e?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80'
    },
    { 
      value: '48hrs', 
      label: 'Built in', 
      icon: <Speed />, 
      color: '#041f41',
      // ✅ ADDED: Speed/development image
      image: 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2015&q=80'
    }
  ];

  return (
    <Box sx={{ 
      backgroundColor: '#FFF9E6', 
      minHeight: '100vh',
      py: 4,
    }}>
      <Container maxWidth="lg">
        {/* ✅ Hero Section with Background Image */}
        <Box 
          sx={{ 
            textAlign: 'center', 
            mb: 6, 
            pt: 4,
            // ✅ ADDED: Hero background image
            backgroundImage: 'linear-gradient(rgba(255, 249, 230, 0.8), rgba(255, 249, 230, 0.9)), url(https://images.unsplash.com/photo-1558494949-ef010cbdcc31?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2134&q=80)',
            backgroundSize: 'cover',
            backgroundPosition: 'center',
            borderRadius: 4,
            py: 8,
            position: 'relative',
          }}
        >
          {/* ✅ UPDATED: Cinzel Title with Black Color */}
          <Typography 
            variant="h1" 
            className="quantum-title fade-in"
            sx={{ 
              mb: 3,
              fontFamily: '"Cinzel", "Times New Roman", serif !important',
              fontSize: { xs: '3rem', sm: '4rem', md: '4.5rem' },
              fontWeight: '400 !important', // ✅ LIGHTER weight as requested
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
            QuantumEco Intelligence
          </Typography>
          
          {/* ✅ Professional Subtitle */}
          <Typography 
            variant="h5" 
            className="quantum-subtitle fade-in"
            sx={{ 
              mb: 4, 
              maxWidth: 800, 
              mx: 'auto',
              animationDelay: '0.3s',
              color: '#808080', // ✅ Changed back to Walmart blue for better contrast
              fontFamily: '"Myriad Pro", "Whitney", "Avenir Next", sans-serif',
              fontSize: { xs: '1.2rem', sm: '1.5rem' },
              lineHeight: 1.5,
              fontWeight: 500,
            }}
          >
            Quantum-inspired logistics optimization with 25% cost reduction, 35% 
            carbon savings, and blockchain-verified sustainability certificates
          </Typography>
          
          {/* ✅ Impact Statement */}
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
            $4.2B Walmart Impact Potential • Built in 48 Hours • Production Ready
          </Typography>
          
          {/* ✅ Hero Buttons with Walmart Blue */}
          <Box sx={{ 
            display: 'flex', 
            gap: 3, 
            justifyContent: 'center',
            flexWrap: 'wrap',
            mb: 6,
            '& > *': {
              animationDelay: '0.9s'
            }
          }} className="fade-in">
            <Button
              variant="contained"
              size="large"
              startIcon={<PlayArrow />}
              onClick={() => navigate('/demo')}
              sx={{
                backgroundColor: '#041f41',
                color: '#FFFFFF',
                fontFamily: '"Myriad Pro", "Whitney", "Avenir Next", sans-serif',
                fontWeight: 600,
                fontSize: '1rem',
                borderRadius: 3,
                px: 4,
                py: 2,
                textTransform: 'none',
                boxShadow: '0 4px 20px rgba(4, 31, 65, 0.3)',
                transition: 'all 0.3s ease',
                '&:hover': {
                  backgroundColor: '#031426',
                  transform: 'translateY(-2px)',
                  boxShadow: '0 8px 32px rgba(4, 31, 65, 0.4)',
                },
              }}
            >
              WATCH LIVE DEMO
            </Button>
            
            <Button
              variant="outlined"
              size="large"
              startIcon={<Dashboard />}
              onClick={() => navigate('/dashboard')}
              sx={{
                borderColor: '#041f41',
                color: '#041f41',
                backgroundColor: 'rgba(255, 255, 255, 0.9)',
                fontFamily: '"Myriad Pro", "Whitney", "Avenir Next", sans-serif',
                fontWeight: 600,
                fontSize: '1rem',
                borderRadius: 3,
                borderWidth: '2px',
                px: 4,
                py: 2,
                textTransform: 'none',
                transition: 'all 0.3s ease',
                '&:hover': {
                  borderColor: '#031426',
                  backgroundColor: 'rgba(4, 31, 65, 0.04)',
                  borderWidth: '2px',
                  transform: 'translateY(-1px)',
                },
              }}
            >
              VIEW DASHBOARD
            </Button>
          </Box>
        </Box>

        {/* ✅ Impact Metrics with Images */}
        <Box sx={{ mb: 6 }}>
          <Typography 
            variant="h5" 
            sx={{ 
              textAlign: 'center', 
              mb: 4, 
              fontWeight: 'bold',
              color: '#041f41',
              fontFamily: '"Myriad Pro", "Whitney", "Avenir Next", sans-serif'
            }}
          >
            🏆 Proven Impact Metrics
          </Typography>
          
          <Box sx={{ 
            display: 'flex', 
            justifyContent: 'center', 
            flexWrap: 'wrap', 
            gap: 3,
            '& > *': {
              flex: '1 1 200px',
              maxWidth: '280px',
              minWidth: '200px'
            }
          }}>
            {impactMetrics.map((metric, index) => (
              <Card 
                className="card fade-in" 
                sx={{ 
                  textAlign: 'center',
                  animationDelay: `${1.2 + index * 0.2}s`,
                  cursor: 'pointer',
                  borderRadius: 4,
                  boxShadow: '0 8px 32px rgba(4, 31, 65, 0.12)',
                  transition: 'all 0.3s ease',
                  overflow: 'hidden',
                  position: 'relative',
                  '&:hover': {
                    transform: 'translateY(-4px)',
                    boxShadow: '0 16px 48px rgba(4, 31, 65, 0.16)',
                  },
                }}
                key={index}
              >
                {/* ✅ ADDED: Background image for each metric */}
                <Box
                  sx={{
                    position: 'absolute',
                    top: 0,
                    left: 0,
                    right: 0,
                    bottom: 0,
                    backgroundImage: `linear-gradient(rgba(255, 255, 255, 0.9), rgba(255, 255, 255, 0.9)), url(${metric.image})`,
                    backgroundSize: 'cover',
                    backgroundPosition: 'center',
                    zIndex: 0,
                  }}
                />
                <CardContent sx={{ py: 3, position: 'relative', zIndex: 1 }}>
                  <Box sx={{ 
                    color: metric.color, 
                    mb: 2,
                    '& svg': { fontSize: '2.5rem' }
                  }}>
                    {metric.icon}
                  </Box>
                  <Typography 
                    variant="h3" 
                    sx={{ 
                      fontWeight: 'bold',
                      color: metric.color,
                      mb: 1,
                      fontFamily: '"Myriad Pro", "Whitney", "Avenir Next", sans-serif',
                    }}
                  >
                    {metric.value}
                  </Typography>
                  <Typography 
                    variant="body1" 
                    sx={{ 
                      color: '#041f41',
                      fontWeight: 500,
                      fontFamily: '"Myriad Pro", "Whitney", "Avenir Next", sans-serif',
                    }}
                  >
                    {metric.label}
                  </Typography>
                </CardContent>
              </Card>
            ))}
          </Box>
        </Box>

        {/* ✅ MVP Features with Images */}
        <Box sx={{ mb: 6 }}>
          <Typography 
            variant="h5" 
            sx={{ 
              textAlign: 'center', 
              mb: 4, 
              fontWeight: 'bold',
              color: '#041f41',
              fontFamily: '"Myriad Pro", "Whitney", "Avenir Next", sans-serif'
            }}
          >
            🚀 Core Features
          </Typography>
          
          <Box sx={{ 
            display: 'flex', 
            flexWrap: 'wrap', 
            gap: 4, 
            justifyContent: 'center',
            '& > *': {
              flex: '1 1 400px',
              maxWidth: '500px',
              minWidth: '350px'
            }
          }}>
            {mvpFeatures.map((feature, index) => (
              <Card 
                sx={{ 
                  cursor: 'pointer',
                  animationDelay: `${1.8 + index * 0.2}s`,
                  display: 'flex',
                  flexDirection: 'column',
                  justifyContent: 'space-between',
                  borderRadius: 4,
                  boxShadow: '0 8px 32px rgba(4, 31, 65, 0.12)',
                  transition: 'all 0.3s ease',
                  overflow: 'hidden',
                  '&:hover': {
                    transform: 'translateY(-4px)',
                    boxShadow: '0 16px 48px rgba(4, 31, 65, 0.16)',
                  },
                }}
                key={index}
                onClick={() => navigate(feature.path)}
              >
                {/* ✅ ADDED: Feature image header */}
                <Box
                  sx={{
                    height: 200,
                    backgroundImage: `url(${feature.image})`,
                    backgroundSize: 'cover',
                    backgroundPosition: 'center',
                    position: 'relative',
                  }}
                >
                  <Box
                    sx={{
                      position: 'absolute',
                      top: 0,
                      left: 0,
                      right: 0,
                      bottom: 0,
                      background: 'linear-gradient(135deg, rgba(4, 31, 65, 0.7), rgba(0, 113, 206, 0.5))',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                    }}
                  >
                    <Box sx={{ 
                      color: '#FFFFFF',
                      '& svg': { fontSize: '3rem' }
                    }}>
                      {feature.icon}
                    </Box>
                  </Box>
                </Box>

                <CardContent sx={{ p: 4, flexGrow: 1 }}>
                  <Typography 
                    variant="h5" 
                    sx={{ 
                      fontWeight: 'bold',
                      color: '#041f41',
                      fontFamily: '"Myriad Pro", "Whitney", "Avenir Next", sans-serif',
                      mb: 2,
                    }}
                  >
                    {feature.title}
                  </Typography>
                  
                  <Typography 
                    variant="body1" 
                    sx={{ 
                      color: '#041f41',
                      mb: 2,
                      lineHeight: 1.6,
                      fontFamily: '"Myriad Pro", "Whitney", "Avenir Next", sans-serif',
                    }}
                  >
                    {feature.description}
                  </Typography>
                  
                  <Chip 
                    label={feature.chipLabel}
                    size="small"
                    sx={{ 
                      backgroundColor: '#FFC220',
                      color: '#041f41',
                      fontWeight: 600
                    }}
                  />
                </CardContent>
                
                <CardActions sx={{ p: 3, pt: 0 }}>
                  <Button 
                    onClick={(e) => {
                      e.stopPropagation();
                      navigate(feature.path);
                    }}
                    fullWidth
                    sx={{
                      backgroundColor: '#041f41',
                      color: '#FFFFFF',
                      fontFamily: '"Myriad Pro", "Whitney", "Avenir Next", sans-serif',
                      fontWeight: 600,
                      borderRadius: 2,
                      textTransform: 'none',
                      '&:hover': {
                        backgroundColor: '#031426',
                      },
                    }}
                  >
                    {feature.title === 'Live Demo' ? 'Start Demo' : 
                     feature.title === 'Analytics Dashboard' ? 'View Analytics' :
                     feature.title === 'Route Optimizer' ? 'Optimize Routes' :
                     'View Certificates'}
                  </Button>
                </CardActions>
              </Card>
            ))}
          </Box>
        </Box>

        {/* ✅ Call to Action Section with Background */}
        <Box sx={{ 
          textAlign: 'center', 
          py: 6,
          mt: 4,
          borderTop: '2px solid rgba(4, 31, 65, 0.1)',
          // ✅ ADDED: Subtle background pattern
          backgroundImage: 'linear-gradient(135deg, rgba(255, 194, 32, 0.05) 0%, rgba(4, 31, 65, 0.05) 100%)',
          borderRadius: 4,
        }}>
          <Typography 
            variant="h4" 
            sx={{ 
              mb: 3,
              fontWeight: 'bold',
              color: '#041f41',
              fontFamily: '"Myriad Pro", "Whitney", "Avenir Next", sans-serif'
            }}
          >
            Ready to Transform Logistics?
          </Typography>
          
          <Typography 
            variant="h6" 
            sx={{ 
              mb: 4,
              color: '#5A6C7D',
              maxWidth: 600,
              mx: 'auto',
              lineHeight: 1.6,
              fontFamily: '"Myriad Pro", "Whitney", "Avenir Next", sans-serif',
            }}
          >
            Experience quantum-inspired optimization that's already changing how 
            Walmart approaches sustainable logistics and supply chain management.
          </Typography>
          
          <Box sx={{ 
            display: 'flex', 
            gap: 3, 
            justifyContent: 'center',
            flexWrap: 'wrap'
          }}>
            <Button
              variant="contained"
              size="large"
              startIcon={<PlayArrow />}
              onClick={() => navigate('/demo')}
              sx={{
                backgroundColor: '#041f41',
                color: '#FFFFFF',
                fontFamily: '"Myriad Pro", "Whitney", "Avenir Next", sans-serif',
                fontWeight: 600,
                borderRadius: 3,
                px: 5,
                py: 2,
                textTransform: 'none',
                '&:hover': {
                  backgroundColor: '#031426',
                },
              }}
            >
              EXPERIENCE THE DEMO
            </Button>
            
            <Button
              variant="outlined"
              size="large"
              startIcon={<Route />}
              onClick={() => navigate('/optimize')}
              sx={{
                borderColor: '#041f41',
                color: '#041f41',
                fontFamily: '"Myriad Pro", "Whitney", "Avenir Next", sans-serif',
                fontWeight: 600,
                borderRadius: 3,
                borderWidth: '2px',
                px: 5,
                py: 2,
                textTransform: 'none',
                '&:hover': {
                  borderColor: '#031426',
                  backgroundColor: 'rgba(4, 31, 65, 0.04)',
                  borderWidth: '2px',
                },
              }}
            >
              TRY OPTIMIZER
            </Button>
          </Box>
        </Box>
      </Container>
    </Box>
  );
};

export default HomePage;
