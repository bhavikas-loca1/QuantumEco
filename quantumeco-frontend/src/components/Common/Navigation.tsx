import React from 'react'
import { AppBar, Toolbar, Typography, Button, Box } from '@mui/material'
import { useNavigate, useLocation } from 'react-router-dom'
import { Dashboard, Route, Security } from '@mui/icons-material'

const Navigation: React.FC = () => {
  const navigate = useNavigate()
  const location = useLocation()

  const navItems = [
    { path: '/', label: 'Dashboard', icon: <Dashboard /> },
    { path: '/route-comparison', label: 'Route Comparison', icon: <Route /> },
    { path: '/blockchain', label: 'Blockchain', icon: <Security /> },
  ]

  return (
    <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          QuantumEco Intelligence
        </Typography>
        <Box sx={{ display: 'flex', gap: 1 }}>
          {navItems.map((item) => (
            <Button
              key={item.path}
              color="inherit"
              startIcon={item.icon}
              onClick={() => navigate(item.path)}
              sx={{
                backgroundColor: location.pathname === item.path ? 'rgba(255, 255, 255, 0.1)' : 'transparent',
              }}
            >
              {item.label}
            </Button>
          ))}
        </Box>
      </Toolbar>
    </AppBar>
  )
}

export default Navigation
