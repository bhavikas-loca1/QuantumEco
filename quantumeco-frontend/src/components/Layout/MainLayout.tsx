import React, { type ReactNode } from 'react';
import {
  Box,
  AppBar,
  Toolbar,
  Typography,
  Button,
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
import { useNavigate, useLocation } from 'react-router-dom';

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
    { label: 'Dashboard', path: '/', icon: <DashboardIcon /> },
    { label: 'Route Optimizer', path: '/optimize', icon: <RouteIcon /> },
    { label: 'Demo', path: '/demo', icon: <DemoIcon /> },
    { label: 'Certificates', path: '/certificates', icon: <CertificateIcon /> },
    { label: 'Analytics', path: '/analytics', icon: <AnalyticsIcon /> },
  ];

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const drawer = (
    <Box sx={{ width: 250 }}>
      <List>
        {navigation.map((item) => (
          <ListItemButton
            key={item.path}
            onClick={() => {
              navigate(item.path);
              if (isMobile) setMobileOpen(false);
            }}
            selected={location.pathname === item.path}
            sx={{
              '&.Mui-selected': {
                backgroundColor: 'primary.light',
                '& .MuiListItemIcon-root': {
                  color: 'primary.main',
                },
                '& .MuiListItemText-primary': {
                  fontWeight: 'bold',
                },
              },
            }}
          >
            <ListItemIcon>{item.icon}</ListItemIcon>
            <ListItemText primary={item.label} />
          </ListItemButton>
        ))}
      </List>
    </Box>
  );

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      {/* Header */}
      <AppBar position="sticky" elevation={1}>
        <Toolbar>
          {isMobile && (
            <IconButton
              color="inherit"
              aria-label="open drawer"
              edge="start"
              onClick={handleDrawerToggle}
              sx={{ mr: 2 }}
            >
              <MenuIcon />
            </IconButton>
          )}
          
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            🚀 QuantumEco Intelligence
          </Typography>
          
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <Chip
              label="Live Demo"
              color="secondary"
              size="small"
              variant="outlined"
            />
            
            {!isMobile && (
              <Box sx={{ display: 'flex', gap: 1 }}>
                {navigation.map((item) => (
                  <Button
                    key={item.path}
                    color="inherit"
                    onClick={() => navigate(item.path)}
                    variant={location.pathname === item.path ? 'outlined' : 'text'}
                    startIcon={item.icon}
                    sx={{
                      borderColor: location.pathname === item.path ? 'white' : 'transparent',
                    }}
                  >
                    {item.label}
                  </Button>
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
            keepMounted: true, // Better open performance on mobile.
          }}
        >
          {drawer}
        </Drawer>
      )}

      {/* Main Content */}
      <Box component="main" sx={{ flexGrow: 1, py: 0 }}>
        {children}
      </Box>

      {/* Footer */}
      <Box
        component="footer"
        sx={{
          mt: 'auto',
          py: 2,
          px: 3,
          backgroundColor: 'grey.100',
          borderTop: '1px solid',
          borderColor: 'divider',
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
            <Typography variant="body2" color="text.secondary">
              © 2025 QuantumEco Intelligence - Quantum-Inspired Logistics Optimization
            </Typography>
            <Box sx={{ display: 'flex', gap: 2 }}>
              <Chip label="FastAPI Backend" size="small" variant="outlined" />
              <Chip label="React Frontend" size="small" variant="outlined" />
              <Chip label="Blockchain Verified" size="small" color="success" variant="outlined" />
            </Box>
          </Box>
        </Container>
      </Box>
    </Box>
  );
};

export default MainLayout;
