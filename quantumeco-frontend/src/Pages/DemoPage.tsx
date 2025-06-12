// import React, { useState } from 'react';
// import { Container, Typography, Box, Tabs, Tab, Alert } from '@mui/material';
// import WalmartDemo from '../components/Demos/WalmartDemo'; // ✅ Your exact path preserved
// import QuickDemo from '../components/Demos/QuickDemos'; // ✅ Your exact path preserved

// /**
//  * DemoPage - Hub for all demo presentations
//  * Purpose: 3-minute hackathon demo and quick 90-second version
//  * FIXED: Now matches HomePage full-width behavior
//  */
// const DemoPage: React.FC = () => {
//   const [tabValue, setTabValue] = useState(0);

//   return (
//     <Container maxWidth="xl" sx={{ py: 4 }}> {/* ✅ Matches HomePage padding */}
//       {/* Header Section - Matches HomePage dense content structure */}
//       <Box sx={{ textAlign: 'center', mb: 6 }}>
//         <Typography variant="h2" sx={{ fontWeight: 'bold', mb: 2, color: 'primary.main' }}>
//           🚀 QuantumEco Intelligence Demo Hub
//         </Typography>
//         <Typography variant="h5" sx={{ mb: 3, color: 'text.secondary', maxWidth: 800, mx: 'auto' }}>
//           Live demonstration of quantum-inspired logistics optimization with real-time API integration, 
//           blockchain verification, and $4.2B Walmart impact potential
//         </Typography>
//         <Typography variant="h6" sx={{ mb: 4, color: 'success.main', fontWeight: 'bold' }}>
//           25% Cost Reduction • 35% Carbon Savings • Built in 48 Hours
//         </Typography>
//       </Box>

//       {/* Demo Mode Alert - Full width like HomePage content */}
//       <Alert 
//         severity="info" 
//         sx={{ 
//           mb: 4, 
//           width: '100%',
//           p: 3,
//           fontSize: '1.1rem',
//           fontWeight: 500,
//           borderRadius: 2
//         }}
//       >
//         🎬 <strong>Demo Mode Active</strong> - Live API integration with real-time optimization and blockchain verification
//       </Alert>

//       {/* Demo Selection Tabs - Enhanced to match HomePage style */}
//       <Box sx={{ 
//         display: 'flex', 
//         flexDirection: 'column',
//         gap: 4,
//         mb: 6
//       }}>
//         <Typography variant="h4" sx={{ fontWeight: 'bold', textAlign: 'center', mb: 2 }}>
//           📊 Select Demo Experience
//         </Typography>
        
//         <Tabs 
//           value={tabValue} 
//           onChange={(_, val) => setTabValue(val)} 
//           sx={{ 
//             mb: 3, 
//             width: '100%',
//             '& .MuiTab-root': {
//               fontSize: '1.1rem',
//               fontWeight: 600,
//               minHeight: 60,
//               px: 4
//             }
//           }}
//           centered
//           variant="fullWidth"
//         >
//           <Tab 
//             label="🏆 Full Demo (3 minutes)" 
//             sx={{ 
//               border: '2px solid transparent',
//               borderRadius: 2,
//               mx: 1,
//               '&.Mui-selected': {
//                 border: '2px solid',
//                 borderColor: 'primary.main',
//                 bgcolor: 'primary.50'
//               }
//             }}
//           />
//           <Tab 
//             label="⚡ Quick Demo (90 seconds)" 
//             sx={{ 
//               border: '2px solid transparent',
//               borderRadius: 2,
//               mx: 1,
//               '&.Mui-selected': {
//                 border: '2px solid',
//                 borderColor: 'secondary.main',
//                 bgcolor: 'secondary.50'
//               }
//             }}
//           />
//         </Tabs>

//         {/* Demo Description Cards - Matches HomePage card structure */}
//         <Box sx={{ 
//           display: 'flex', 
//           flexWrap: 'wrap',
//           gap: 4,
//           mb: 4
//         }}>
//           {tabValue === 0 && (
//             <Box sx={{ 
//               flex: { xs: '1 1 100%', md: '1 1 100%' }, // Full width like HomePage
//               width: '100%'
//             }}>
//               <Alert severity="success" sx={{ 
//                 p: 3, 
//                 borderRadius: 2,
//                 bgcolor: 'success.50',
//                 border: '2px solid',
//                 borderColor: 'success.main'
//               }}>
//                 <Typography variant="h6" sx={{ fontWeight: 'bold', mb: 1 }}>
//                   🎯 Complete 3-Minute Hackathon Presentation
//                 </Typography>
//                 <Typography variant="body1">
//                   Full demonstration including problem statement, live optimization comparison, 
//                   carbon impact analysis, blockchain verification, and Walmart scale projections.
//                   Perfect for investor presentations and technical demonstrations.
//                 </Typography>
//               </Alert>
//             </Box>
//           )}

//           {tabValue === 1 && (
//             <Box sx={{ 
//               flex: { xs: '1 1 100%', md: '1 1 100%' }, // Full width like HomePage
//               width: '100%'
//             }}>
//               <Alert severity="warning" sx={{ 
//                 p: 3, 
//                 borderRadius: 2,
//                 bgcolor: 'warning.50',
//                 border: '2px solid',
//                 borderColor: 'warning.main'
//               }}>
//                 <Typography variant="h6" sx={{ fontWeight: 'bold', mb: 1 }}>
//                   ⚡ Rapid 90-Second Overview
//                 </Typography>
//                 <Typography variant="body1">
//                   Condensed demonstration focusing on key metrics: 25% cost reduction, 
//                   35% carbon savings, and blockchain verification. Ideal for quick pitches 
//                   and technical overviews.
//                 </Typography>
//               </Alert>
//             </Box>
//           )}
//         </Box>
//       </Box>

//       {/* Demo Content - Full width container */}
//       <Box sx={{ 
//         width: '100%',
//         minHeight: '70vh',
//         display: 'flex',
//         flexDirection: 'column'
//       }}>
//         {tabValue === 0 && <WalmartDemo />}
//         {tabValue === 1 && <QuickDemo />}
//       </Box>

//       {/* Footer Stats - Matches HomePage stats section */}
//       <Box sx={{ mt: 8, textAlign: 'center' }}>
//         <Typography variant="h6" sx={{ mb: 3 }}>
//           🏆 Demo Performance Metrics
//         </Typography>
//         <Box sx={{ display: 'flex', justifyContent: 'center', gap: 4, flexWrap: 'wrap' }}>
//           <Box>
//             <Typography variant="h4" color="success.main" sx={{ fontWeight: 'bold' }}>3min</Typography>
//             <Typography variant="body2">Full Demo Duration</Typography>
//           </Box>
//           <Box>
//             <Typography variant="h4" color="info.main" sx={{ fontWeight: 'bold' }}>90s</Typography>
//             <Typography variant="body2">Quick Demo Duration</Typography>
//           </Box>
//           <Box>
//             <Typography variant="h4" color="warning.main" sx={{ fontWeight: 'bold' }}>Live</Typography>
//             <Typography variant="body2">API Integration</Typography>
//           </Box>
//           <Box>
//             <Typography variant="h4" color="primary.main" sx={{ fontWeight: 'bold' }}>Real</Typography>
//             <Typography variant="body2">Blockchain Verification</Typography>
//           </Box>
//         </Box>
//       </Box>
//     </Container>
//   );
// };

// export default DemoPage;
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
      {/* Hero Section */}
      <Box sx={{ 
        textAlign: 'center', 
        mb: 4, 
        px: { xs: 2, sm: 3, md: 4 },
        py: 3
      }}>
        <Typography variant="h2" sx={{ fontWeight: 'bold', mb: 2, color: 'primary.main' }}>
          🚀 QuantumEco Intelligence Demo Hub
        </Typography>
        <Typography variant="h5" sx={{ mb: 3, color: 'text.secondary', maxWidth: 800, mx: 'auto' }}>
          Live demonstration of quantum-inspired logistics optimization with real-time API integration, 
          blockchain verification, and $4.2B Walmart impact potential
        </Typography>
        <Typography variant="h6" sx={{ mb: 4, color: 'success.main', fontWeight: 'bold' }}>
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
