// import React from 'react';
// import {
//   Box,
//   Card,
//   CardContent,
//   Typography,
//   Chip,
//   LinearProgress,
//   Avatar,
//   Skeleton,
// } from '@mui/material';
// import {
//   TrendingUp,
//   TrendingDown,
//   TrendingFlat,
//   Co2Outlined,
//   AttachMoneyOutlined,
//   AccessTimeOutlined,
//   LocalShippingOutlined,
//   SpeedOutlined,
//   AssessmentOutlined,
//   StarOutlined,
// } from '@mui/icons-material';
// import { type KPIMetric } from '../../Services/types';

// interface KPICardsProps {
//   metrics: KPIMetric[];
//   loading?: boolean;
// }

// /**
//  * KPICards Component
//  * Purpose: Displays key performance indicators from the analytics service
//  * Features: Dynamic icons, trend indicators, progress bars, responsive flexbox layout
//  */
// const KPICards: React.FC<KPICardsProps> = ({ metrics, loading = false }) => {
//   const getMetricIcon = (metricName: string) => {
//     const name = metricName.toLowerCase();
//     if (name.includes('cost') || name.includes('savings') || name.includes('usd') || name.includes('dollar')) {
//       return <AttachMoneyOutlined />;
//     }
//     if (name.includes('carbon') || name.includes('emission') || name.includes('co2') || name.includes('environmental')) {
//       return <Co2Outlined />;
//     }
//     if (name.includes('time') || name.includes('duration') || name.includes('minutes') || name.includes('hours')) {
//       return <AccessTimeOutlined />;
//     }
//     if (name.includes('route') || name.includes('delivery') || name.includes('optimization') || name.includes('vehicle')) {
//       return <LocalShippingOutlined />;
//     }
//     if (name.includes('efficiency') || name.includes('performance') || name.includes('score')) {
//       return <SpeedOutlined />;
//     }
//     if (name.includes('quantum') || name.includes('improvement')) {
//       return <StarOutlined />;
//     }
//     return <AssessmentOutlined />;
//   };

//   const getTrendIcon = (trend?: string) => {
//     switch (trend) {
//       case 'up':
//         return <TrendingUp sx={{ color: 'success.main', fontSize: 20 }} />;
//       case 'down':
//         return <TrendingDown sx={{ color: 'error.main', fontSize: 20 }} />;
//       default:
//         return <TrendingFlat sx={{ color: 'grey.500', fontSize: 20 }} />;
//     }
//   };

//   const getMetricColor = (metricName: string) => {
//     const name = metricName.toLowerCase();
//     if (name.includes('cost') || name.includes('savings')) return 'success.main';
//     if (name.includes('carbon') || name.includes('environmental')) return 'info.main';
//     if (name.includes('time') || name.includes('efficiency')) return 'warning.main';
//     if (name.includes('quantum') || name.includes('improvement')) return 'secondary.main';
//     return 'primary.main';
//   };

//   const formatMetricValue = (value: number | string) => {
//     if (typeof value === 'number') {
//       if (value >= 1000000) {
//         return `${(value / 1000000).toFixed(1)}M`;
//       }
//       if (value >= 1000) {
//         return `${(value / 1000).toFixed(1)}K`;
//       }
//       return value % 1 === 0 ? value.toString() : value.toFixed(1);
//     }
//     return value;
//   };

//   const getTrendColor = (trend?: string) => {
//     switch (trend) {
//       case 'up': return 'success';
//       case 'down': return 'error';
//       default: return 'default';
//     }
//   };

//   if (loading) {
//     return (
//       <Box
//         sx={{
//           display: 'flex',
//           flexWrap: 'wrap',
//           gap: 3,
//           width: '100%',
//         }}
//       >
//         {[1, 2, 3, 4, 5, 6].map((i) => (
//           <Card key={i} sx={{ flex: '1 1 300px', minWidth: 300 }}>
//             <CardContent>
//               <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
//                 <Skeleton variant="circular" width={48} height={48} sx={{ mr: 2 }} />
//                 <Box sx={{ flex: 1 }}>
//                   <Skeleton variant="text" width="60%" height={20} />
//                   <Skeleton variant="text" width="40%" height={16} />
//                 </Box>
//                 <Skeleton variant="rectangular" width={60} height={24} />
//               </Box>
//               <Skeleton variant="text" width="80%" height={32} sx={{ mb: 1 }} />
//               <Skeleton variant="text" width="100%" height={16} sx={{ mb: 2 }} />
//               <Skeleton variant="rectangular" width="100%" height={6} />
//             </CardContent>
//           </Card>
//         ))}
//       </Box>
//     );
//   }

//   if (!metrics || metrics.length === 0) {
//     return (
//       <Card sx={{ p: 4, textAlign: 'center' }}>
//         <AssessmentOutlined sx={{ fontSize: 64, color: 'text.secondary', mb: 2 }} />
//         <Typography variant="h6" color="text.secondary" gutterBottom>
//           No KPI data available
//         </Typography>
//         <Typography variant="body2" color="text.secondary">
//           Key performance indicators will appear here after system initialization
//         </Typography>
//       </Card>
//     );
//   }

//   return (
//     <Box
//       sx={{
//         display: 'flex',
//         flexWrap: 'wrap',
//         gap: 3,
//         width: '100%',
//       }}
//     >
//       {metrics.map((metric, index) => (
//         <Card
//           key={`${metric.name}-${index}`}
//           sx={{
//             flex: '1 1 300px',
//             minWidth: 300,
//             transition: 'all 0.3s ease',
//             '&:hover': {
//               transform: 'translateY(-4px)',
//               boxShadow: 6,
//             },
//           }}
//         >
//           <CardContent>
//             {/* Header Section */}
//             <Box
//               sx={{
//                 display: 'flex',
//                 justifyContent: 'space-between',
//                 alignItems: 'flex-start',
//                 mb: 2,
//               }}
//             >
//               <Avatar
//                 sx={{
//                   bgcolor: getMetricColor(metric.name),
//                   width: 48,
//                   height: 48,
//                 }}
//               >
//                 {getMetricIcon(metric.name)}
//               </Avatar>
              
//               <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
//                 {metric.trend && getTrendIcon(metric.trend)}
//                 {metric.change_percent !== undefined && (
//                   <Chip
//                     label={`${metric.change_percent >= 0 ? '+' : ''}${metric.change_percent.toFixed(1)}%`}
//                     size="small"
//                     color={getTrendColor(metric.trend)}
//                     variant="outlined"
//                   />
//                 )}
//               </Box>
//             </Box>

//             {/* Value Section */}
//             <Box sx={{ mb: 2 }}>
//               <Typography
//                 variant="h4"
//                 sx={{
//                   fontWeight: 'bold',
//                   color: getMetricColor(metric.name),
//                   lineHeight: 1,
//                   mb: 0.5,
//                   display: 'flex',
//                   alignItems: 'baseline',
//                   flexWrap: 'wrap',
//                 }}
//               >
//                 {formatMetricValue(metric.value)}
//                 {metric.unit && (
//                   <Typography
//                     component="span"
//                     variant="body2"
//                     sx={{ 
//                       ml: 1, 
//                       color: 'text.secondary', 
//                       fontSize: '0.875rem',
//                       fontWeight: 'normal'
//                     }}
//                   >
//                     {metric.unit}
//                   </Typography>
//                 )}
//               </Typography>
              
//               <Typography
//                 variant="h6"
//                 sx={{
//                   color: 'text.primary',
//                   fontWeight: 500,
//                   fontSize: '1.1rem',
//                 }}
//               >
//                 {metric.name}
//               </Typography>
//             </Box>

//             {/* Description */}
//             <Typography
//               variant="body2"
//               color="text.secondary"
//               sx={{ 
//                 mb: 2, 
//                 minHeight: 40,
//                 fontSize: '0.875rem',
//                 lineHeight: 1.4
//               }}
//             >
//               {metric.description}
//             </Typography>

//             {/* Progress Section */}
//             {metric.achievement_percent !== undefined && (
//               <Box sx={{ mt: 2 }}>
//                 <Box
//                   sx={{
//                     display: 'flex',
//                     justifyContent: 'space-between',
//                     alignItems: 'center',
//                     mb: 1,
//                   }}
//                 >
//                   <Typography variant="caption" color="text.secondary">
//                     Target Achievement
//                   </Typography>
//                   <Typography variant="caption" sx={{ fontWeight: 'bold' }}>
//                     {metric.achievement_percent.toFixed(0)}%
//                   </Typography>
//                 </Box>
//                 <LinearProgress
//                   variant="determinate"
//                   value={Math.min(metric.achievement_percent, 100)}
//                   sx={{
//                     height: 6,
//                     borderRadius: 3,
//                     backgroundColor: 'grey.200',
//                     '& .MuiLinearProgress-bar': {
//                       backgroundColor: getMetricColor(metric.name),
//                       borderRadius: 3,
//                     },
//                   }}
//                 />
//                 {metric.target_value !== undefined && (
//                   <Box sx={{ mt: 1 }}>
//                     <Typography variant="caption" color="text.secondary">
//                       Target: {formatMetricValue(metric.target_value)} {metric.unit || ''}
//                     </Typography>
//                   </Box>
//                 )}
//               </Box>
//             )}
//           </CardContent>
//         </Card>
//       ))}
//     </Box>
//   );
// };

// export default KPICards;
import React from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Chip,
  LinearProgress,
  Avatar,
  Skeleton,
} from '@mui/material';
import {
  TrendingUp,
  TrendingDown,
  TrendingFlat,
  Co2Outlined,
  AttachMoneyOutlined,
  AccessTimeOutlined,
  LocalShippingOutlined,
  SpeedOutlined,
  AssessmentOutlined,
  StarOutlined,
} from '@mui/icons-material';
import { type KPIMetric } from '../../Services/types';

interface KPICardsProps {
  metrics: KPIMetric[];
  loading?: boolean;
}

const KPICards: React.FC<KPICardsProps> = ({ metrics, loading = false }) => {
  const getMetricIcon = (metricName: string) => {
    const name = metricName.toLowerCase();
    if (name.includes('cost') || name.includes('savings') || name.includes('usd') || name.includes('dollar')) {
      return <AttachMoneyOutlined />;
    }
    if (name.includes('carbon') || name.includes('emission') || name.includes('co2') || name.includes('environmental')) {
      return <Co2Outlined />;
    }
    if (name.includes('time') || name.includes('duration') || name.includes('minutes') || name.includes('hours')) {
      return <AccessTimeOutlined />;
    }
    if (name.includes('route') || name.includes('delivery') || name.includes('optimization') || name.includes('vehicle')) {
      return <LocalShippingOutlined />;
    }
    if (name.includes('efficiency') || name.includes('performance') || name.includes('score')) {
      return <SpeedOutlined />;
    }
    if (name.includes('quantum') || name.includes('improvement')) {
      return <StarOutlined />;
    }
    return <AssessmentOutlined />;
  };

  const getTrendIcon = (trend?: string) => {
    switch (trend) {
      case 'up':
        return <TrendingUp sx={{ color: 'success.main', fontSize: 20 }} />;
      case 'down':
        return <TrendingDown sx={{ color: 'error.main', fontSize: 20 }} />;
      default:
        return <TrendingFlat sx={{ color: 'grey.500', fontSize: 20 }} />;
    }
  };

  const getMetricColor = (metricName: string) => {
    const name = metricName.toLowerCase();
    if (name.includes('cost') || name.includes('savings')) return 'success.main';
    if (name.includes('carbon') || name.includes('environmental')) return 'info.main';
    if (name.includes('time') || name.includes('efficiency')) return 'warning.main';
    if (name.includes('quantum') || name.includes('improvement')) return 'secondary.main';
    return 'primary.main';
  };

  const formatMetricValue = (value: number | string) => {
    if (typeof value === 'number') {
      if (value >= 1000000) {
        return `${(value / 1000000).toFixed(1)}M`;
      }
      if (value >= 1000) {
        return `${(value / 1000).toFixed(1)}K`;
      }
      return value % 1 === 0 ? value.toString() : value.toFixed(1);
    }
    return value;
  };

  const getTrendColor = (trend?: string) => {
    switch (trend) {
      case 'up': return 'success';
      case 'down': return 'error';
      default: return 'default';
    }
  };

  // ✅ FIXED: Safe number formatting with null checks
  const safeToFixed = (value: number | null | undefined, decimals: number = 1): string => {
    if (value === null || value === undefined || isNaN(value)) {
      return '0';
    }
    return value.toFixed(decimals);
  };

  if (loading) {
    return (
      <Box
        sx={{
          display: 'flex',
          flexWrap: 'wrap',
          gap: 3,
          width: '100%',
        }}
      >
        {[1, 2, 3, 4, 5, 6].map((i) => (
          <Card key={i} sx={{ flex: '1 1 300px', minWidth: 300 }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Skeleton variant="circular" width={48} height={48} sx={{ mr: 2 }} />
                <Box sx={{ flex: 1 }}>
                  <Skeleton variant="text" width="60%" height={20} />
                  <Skeleton variant="text" width="40%" height={16} />
                </Box>
                <Skeleton variant="rectangular" width={60} height={24} />
              </Box>
              <Skeleton variant="text" width="80%" height={32} sx={{ mb: 1 }} />
              <Skeleton variant="text" width="100%" height={16} sx={{ mb: 2 }} />
              <Skeleton variant="rectangular" width="100%" height={6} />
            </CardContent>
          </Card>
        ))}
      </Box>
    );
  }

  if (!metrics || metrics.length === 0) {
    return (
      <Card sx={{ p: 4, textAlign: 'center' }}>
        <AssessmentOutlined sx={{ fontSize: 64, color: 'text.secondary', mb: 2 }} />
        <Typography variant="h6" color="text.secondary" gutterBottom>
          No KPI data available
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Key performance indicators will appear here after system initialization
        </Typography>
      </Card>
    );
  }

  return (
    <Box
      sx={{
        display: 'flex',
        flexWrap: 'wrap',
        gap: 3,
        width: '100%',
      }}
    >
      {metrics.map((metric, index) => (
        <Card
          key={`${metric.name}-${index}`}
          sx={{
            flex: '1 1 300px',
            minWidth: 300,
            transition: 'all 0.3s ease',
            '&:hover': {
              transform: 'translateY(-4px)',
              boxShadow: 6,
            },
          }}
        >
          <CardContent>
            {/* Header Section */}
            <Box
              sx={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'flex-start',
                mb: 2,
              }}
            >
              <Avatar
                sx={{
                  bgcolor: getMetricColor(metric.name),
                  width: 48,
                  height: 48,
                }}
              >
                {getMetricIcon(metric.name)}
              </Avatar>
              
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                {metric.trend && getTrendIcon(metric.trend)}
                {/* ✅ FIXED: Safe null check for change_percent */}
                {metric.change_percent !== undefined && metric.change_percent !== null && (
                  <Chip
                    label={`${metric.change_percent >= 0 ? '+' : ''}${safeToFixed(metric.change_percent, 1)}%`}
                    size="small"
                    color={getTrendColor(metric.trend)}
                    variant="outlined"
                  />
                )}
              </Box>
            </Box>

            {/* Value Section */}
            <Box sx={{ mb: 2 }}>
              <Typography
                variant="h4"
                sx={{
                  fontWeight: 'bold',
                  color: getMetricColor(metric.name),
                  lineHeight: 1,
                  mb: 0.5,
                  display: 'flex',
                  alignItems: 'baseline',
                  flexWrap: 'wrap',
                }}
              >
                {formatMetricValue(metric.value)}
                {metric.unit && (
                  <Typography
                    component="span"
                    variant="body2"
                    sx={{ 
                      ml: 1, 
                      color: 'text.secondary', 
                      fontSize: '0.875rem',
                      fontWeight: 'normal'
                    }}
                  >
                    {metric.unit}
                  </Typography>
                )}
              </Typography>
              
              <Typography
                variant="h6"
                sx={{
                  color: 'text.primary',
                  fontWeight: 500,
                  fontSize: '1.1rem',
                }}
              >
                {metric.name}
              </Typography>
            </Box>

            {/* Description */}
            <Typography
              variant="body2"
              color="text.secondary"
              sx={{ 
                mb: 2, 
                minHeight: 40,
                fontSize: '0.875rem',
                lineHeight: 1.4
              }}
            >
              {metric.description}
            </Typography>

            {/* ✅ FIXED: Progress Section with null checks */}
            {metric.achievement_percent !== undefined && metric.achievement_percent !== null && (
              <Box sx={{ mt: 2 }}>
                <Box
                  sx={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    mb: 1,
                  }}
                >
                  <Typography variant="caption" color="text.secondary">
                    Target Achievement
                  </Typography>
                  <Typography variant="caption" sx={{ fontWeight: 'bold' }}>
                    {safeToFixed(metric.achievement_percent, 0)}%
                  </Typography>
                </Box>
                <LinearProgress
                  variant="determinate"
                  value={Math.min(metric.achievement_percent || 0, 100)}
                  sx={{
                    height: 6,
                    borderRadius: 3,
                    backgroundColor: 'grey.200',
                    '& .MuiLinearProgress-bar': {
                      backgroundColor: getMetricColor(metric.name),
                      borderRadius: 3,
                    },
                  }}
                />
                {metric.target_value !== undefined && metric.target_value !== null && (
                  <Box sx={{ mt: 1 }}>
                    <Typography variant="caption" color="text.secondary">
                      Target: {formatMetricValue(metric.target_value)} {metric.unit || ''}
                    </Typography>
                  </Box>
                )}
              </Box>
            )}
          </CardContent>
        </Card>
      ))}
    </Box>
  );
};

export default KPICards;
