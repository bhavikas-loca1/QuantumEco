import React, { type ReactNode } from 'react';
import {
  Box,
  AppBar,
  Toolbar,
  Typography,
  Container,
  Chip,
  Drawer,
  List,
  ListItemIcon,
  ListItemText,
  useMediaQuery,
  useTheme,
  IconButton,
  ListItemButton,
} from '@mui/material';
import {
  Dashboard as DashboardIcon,
  Route as RouteIcon,
  PlayArrow as DemoIcon,
  Security as CertificateIcon,
  Menu as MenuIcon,
  Analytics as AnalyticsIcon,
} from '@mui/icons-material';
import { useNavigate, useLocation, Link } from 'react-router-dom';

interface MainLayoutProps {
  children: ReactNode;
}

const MainLayout: React.FC<MainLayoutProps> = ({ children }) => {
  const navigate = useNavigate();
  const location = useLocation();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const [mobileOpen, setMobileOpen] = React.useState(false);

  const navigation = [
    { label: 'Live Demo', path: '/demo', icon: <DemoIcon /> },
    { label: 'Dashboard', path: '/dashboard', icon: <DashboardIcon /> },
    { label: 'Route Optimizer', path: '/optimize', icon: <RouteIcon /> },
    { label: 'Certificates', path: '/certificates', icon: <CertificateIcon /> },
    // { label: 'Analytics', path: '/analytics', icon: <AnalyticsIcon /> },
  ];

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const isActivePath = (path: string) => {
    return location.pathname === path || location.pathname.startsWith(path + '/');
  };

  const drawer = (
    <Box sx={{ width: 250, pt: 2 }}>
      <List>
        {navigation.map((item) => (
          <ListItemButton
            key={item.path}
            onClick={() => {
              navigate(item.path);
              if (isMobile) setMobileOpen(false);
            }}
            selected={isActivePath(item.path)}
            sx={{
              '&.Mui-selected': {
                backgroundColor: 'rgba(0, 113, 206, 0.1)',
                '& .MuiListItemIcon-root': {
                  color: '#0071CE',
                },
                '& .MuiListItemText-primary': {
                  fontWeight: 'bold',
                  color: '#041f41',
                },
              },
              '&:hover': {
                backgroundColor: 'rgba(0, 113, 206, 0.05)',
              },
            }}
          >
            <ListItemIcon sx={{ color: '#041f41' }}>{item.icon}</ListItemIcon>
            <ListItemText 
              primary={item.label}
              sx={{
                '& .MuiListItemText-primary': {
                  fontFamily: '"Myriad Pro", "Whitney", "Avenir Next", sans-serif',
                  fontSize: '1rem',
                }
              }}
            />
          </ListItemButton>
        ))}
      </List>
    </Box>
  );

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      {/* ✅ UPDATED: Smaller header with reduced font sizes */}
      <AppBar 
        position="sticky" 
        elevation={0}
        sx={{
          backgroundColor: '#041f41', // Walmart Bentonville Blue
          borderBottom: '3px solid #FFC220', // Walmart Spark Yellow accent
          minHeight: '60px', // ✅ EVEN SMALLER: Reduced from 70px
        }}
      >
        <Toolbar
          sx={{
            minHeight: '60px !important', // ✅ SMALLER: Match AppBar height
            paddingLeft: '24px',
            paddingRight: '24px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
          }}
        >
          {/* Mobile Menu Button */}
          {isMobile && (
            <IconButton
              color="inherit"
              aria-label="open drawer"
              edge="start"
              onClick={handleDrawerToggle}
              sx={{ 
                mr: 2,
                color: '#FFFFFF',
                '&:hover': {
                  backgroundColor: 'rgba(255, 194, 32, 0.1)',
                },
              }}
            >
              <MenuIcon />
            </IconButton>
          )}
          
          {/* ✅ REDUCED: Walmart Logo + Smaller Brand Name */}
          <Box
            component={Link}
            to="/"
            sx={{
              display: 'flex',
              alignItems: 'center',
              gap: 1.5, // ✅ REDUCED: Smaller gap
              textDecoration: 'none',
              color: '#FFFFFF',
              flexGrow: isMobile ? 1 : 0,
              '&:hover': {
                color: '#FFC220',
                transition: 'color 0.3s ease',
              },
            }}
          >
            {/* ✅ SMALLER: Walmart Logo */}
            <Box
              sx={{
                width: 32,  // ✅ REDUCED: From 40px to 32px
                height: 32, // ✅ REDUCED: From 40px to 32px
                borderRadius: '50%',
                background: 'linear-gradient(135deg, #FFC220 0%, #FFD666 100%)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontWeight: 900,
                fontSize: '1rem', // ✅ REDUCED: From 1.2rem to 1rem
                color: '#041f41',
                border: '2px solid #FFFFFF',
                boxShadow: '0 2px 8px rgba(255, 194, 32, 0.3)',
              }}
            >
              W
            </Box>
            
            {/* ✅ SMALLER: Brand Name */}
            <Typography
              variant="h6"
              sx={{
                fontWeight: 400, // ✅ REDUCED: From 700 to 600
                fontSize: '1.1rem', // ✅ REDUCED: From 1.4rem to 1.1rem
                fontFamily: '"Myriad Pro", "Whitney", "Avenir Next", sans-serif',
              }}
            >
              QuantumEco Intelligence
            </Typography>
          </Box>
          
          {/* ✅ MUCH SMALLER: Desktop Navigation */}
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5 }}> {/* Reduced gap */}
            {/* Live Demo Chip - Made smaller */}
            <Chip
              label="Live Demo"
              size="small"
              sx={{
                backgroundColor: '#FFC220',
                color: '#041f41',
                fontWeight: 300, // ✅ REDUCED: From 600 to 500
                fontSize: '0.7rem', // ✅ REDUCED: From 0.8rem to 0.7rem
                height: '15px', // ✅ SMALLER: Explicit height
                '&:hover': {
                  backgroundColor: '#FFD666',
                },
              }}
            />
            
            {/* ✅ MUCH SMALLER: Navigation Options */}
            {!isMobile && (
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}> {/* Reduced gap */}
                {navigation.map((item) => (
                  <Typography
                    key={item.path}
                    component={Link}
                    to={item.path}
                    variant="caption" // ✅ SMALLER: Changed from body2 to caption
                    sx={{
                      color: isActivePath(item.path) ? '#FFC220' : '#FFFFFF',
                      textDecoration: 'none',
                      fontWeight: isActivePath(item.path) ? 600 : 400, // ✅ REDUCED: From 500 to 400
                      fontSize: '0.75rem', // ✅ MUCH SMALLER: From 0.95rem to 0.75rem
                      fontFamily: '"Myriad Pro", "Whitney", "Avenir Next", sans-serif',
                      position: 'relative',
                      padding: '4px 8px', // ✅ SMALLER: Reduced padding
                      borderRadius: '4px',
                      transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
                      textTransform: 'uppercase', // ✅ ADDED: Makes small text more readable
                      letterSpacing: '0.5px', // ✅ ADDED: Better readability for small text
                      '&:hover': {
                        color: '#FFC220',
                        backgroundColor: 'rgba(255, 194, 32, 0.08)',
                        transform: 'translateY(-1px)',
                      },
                      // ✅ SMALLER: Underline indicator
                      '&::after': {
                        content: '""',
                        position: 'absolute',
                        bottom: 0,
                        left: '50%',
                        transform: 'translateX(-50%)',
                        width: isActivePath(item.path) ? '70%' : '0%', // ✅ SMALLER: From 80% to 70%
                        height: '1px', // ✅ THINNER: From 2px to 1px
                        backgroundColor: '#FFC220',
                        transition: 'width 0.3s ease',
                      },
                      '&:hover::after': {
                        width: '70%',
                      },
                    }}
                  >
                    {item.label}
                  </Typography>
                ))}
              </Box>
            )}
          </Box>
        </Toolbar>
      </AppBar>

      {/* Mobile Drawer */}
      {isMobile && (
        <Drawer
          variant="temporary"
          anchor="left"
          open={mobileOpen}
          onClose={handleDrawerToggle}
          ModalProps={{
            keepMounted: true,
          }}
          sx={{
            '& .MuiDrawer-paper': {
              backgroundColor: '#FFFFFF',
              borderRight: '3px solid #FFC220',
            },
          }}
        >
          {drawer}
        </Drawer>
      )}

      {/* ✅ UPDATED: Main Content with adjusted spacing */}
      <Box 
        component="main" 
        sx={{ 
          flexGrow: 1, 
          pt: 0, // Remove extra padding since AppBar is sticky
          minHeight: '100vh',
          backgroundColor: '#FFF9E6', // Pastel yellow background
        }}
      >
        {children}
      </Box>

      {/* ✅ UPDATED: Footer with smaller text */}
      <Box
        component="footer"
        sx={{
          mt: 'auto',
          py: 2, // ✅ REDUCED: From 3 to 2
          px: 3,
          backgroundColor: '#041f41', // Match header
          borderTop: '3px solid #FFC220',
          color: '#FFFFFF',
        }}
      >
        <Container maxWidth="xl">
          <Box
            sx={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              flexWrap: 'wrap',
              gap: 2,
            }}
          >
            <Typography 
              variant="caption" // ✅ SMALLER: From body2 to caption
              sx={{
                color: '#FFFFFF',
                fontFamily: '"Myriad Pro", "Whitney", "Avenir Next", sans-serif',
                fontSize: '0.75rem', // ✅ SMALLER: From 0.9rem to 0.75rem
              }}
            >
              © 2025 QuantumEco Intelligence - Quantum-Inspired Logistics Optimization
            </Typography>
            <Box sx={{ display: 'flex', gap: 1 }}> {/* Reduced gap */}
              <Chip 
                label="FastAPI Backend" 
                size="small" 
                sx={{
                  backgroundColor: 'rgba(255, 194, 32, 0.2)',
                  color: '#FFC220',
                  border: '1px solid #FFC220',
                  fontSize: '0.6rem', // ✅ SMALLER: Chip text
                  height: '20px', // ✅ SMALLER: Chip height
                }}
              />
              <Chip 
                label="React Frontend" 
                size="small" 
                sx={{
                  backgroundColor: 'rgba(255, 194, 32, 0.2)',
                  color: '#FFC220',
                  border: '1px solid #FFC220',
                  fontSize: '0.6rem', // ✅ SMALLER: Chip text
                  height: '20px', // ✅ SMALLER: Chip height
                }}
              />
              <Chip 
                label="Blockchain Verified" 
                size="small" 
                sx={{
                  backgroundColor: 'rgba(76, 175, 80, 0.2)',
                  color: '#4CAF50',
                  border: '1px solid #4CAF50',
                  fontSize: '0.6rem', // ✅ SMALLER: Chip text
                  height: '20px', // ✅ SMALLER: Chip height
                }}
              />
            </Box>
          </Box>
        </Container>
      </Box>
    </Box>
  );
};

export default MainLayout;
