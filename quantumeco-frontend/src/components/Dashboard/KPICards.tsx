import React from 'react'
import { Paper, Typography, Box, LinearProgress } from '@mui/material'
import {
  TrendingUp,
  Nature,
  LocalShipping,
  AttachMoney,
} from '@mui/icons-material'
import { type DashboardData } from '../../Services/types'

interface KPICardsProps {
  data: DashboardData | null
}

const KPICards: React.FC<KPICardsProps> = ({ data }) => {
  const defaultKPIs = [
    {
      title: 'Cost Savings',
      value: data?.totalSavings ? `$${data.totalSavings.cost.toLocaleString()}` : '$0',
      subtitle: 'Total saved today',
      icon: <AttachMoney />,
      color: '#4caf50',
      progress: 75,
    },
    {
      title: 'Carbon Reduced',
      value: data?.totalSavings ? `${data.totalSavings.carbon.toFixed(1)} kg` : '0 kg',
      subtitle: 'CO² emissions saved',
      icon: <Nature />,
      color: '#2e7d32',
      progress: 85,
    },
    {
      title: 'Routes Optimized',
      value: data?.recentOptimizations?.length || 0,
      subtitle: 'Quantum-inspired optimization',
      icon: <LocalShipping />,
      color: '#1976d2',
      progress: 60,
    },
    {
      title: 'Efficiency Gain',
      value: '32%',
      subtitle: 'vs traditional routing',
      icon: <TrendingUp />,
      color: '#7b1fa2',
      progress: 90,
    },
  ]

  return (
    <Box 
      sx={{
        display: 'flex',
        flexWrap: 'wrap',
        gap: 3,
        '& > *': {
          flex: {
            xs: '1 1 100%',    // Mobile: full width
            sm: '1 1 calc(50% - 12px)',  // Tablet: 2 per row
            md: '1 1 calc(25% - 18px)',  // Desktop: 4 per row
          },
          minWidth: '250px',  // Minimum width for each card
        }
      }}
    >
      {defaultKPIs.map((kpi, index) => (
        <Paper
          key={index}
          sx={{
            p: 2,
            display: 'flex',
            flexDirection: 'column',
            height: 160,
            position: 'relative',
            overflow: 'hidden',
          }}
        >
          {/* Background gradient */}
          <Box
            sx={{
              position: 'absolute',
              top: 0,
              right: 0,
              width: 80,
              height: 80,
              borderRadius: '50%',
              backgroundColor: kpi.color,
              opacity: 0.1,
              transform: 'translate(30px, -30px)',
            }}
          />
          
          {/* Content */}
          <Box display="flex" alignItems="center" mb={1}>
            <Box
              sx={{
                color: kpi.color,
                mr: 1,
                display: 'flex',
                alignItems: 'center',
              }}
            >
              {kpi.icon}
            </Box>
            <Typography variant="h6" component="div" sx={{ fontSize: '0.9rem' }}>
              {kpi.title}
            </Typography>
          </Box>
          
          <Typography variant="h4" component="div" sx={{ fontWeight: 'bold', mb: 1 }}>
            {kpi.value}
          </Typography>
          
          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
            {kpi.subtitle}
          </Typography>
          
          {/* Progress indicator */}
          <Box mt="auto">
            <LinearProgress
              variant="determinate"
              value={kpi.progress}
              sx={{
                backgroundColor: 'rgba(0,0,0,0.1)',
                '& .MuiLinearProgress-bar': {
                  backgroundColor: kpi.color,
                },
              }}
            />
          </Box>
        </Paper>
      ))}
    </Box>
  )
}

export default KPICards
