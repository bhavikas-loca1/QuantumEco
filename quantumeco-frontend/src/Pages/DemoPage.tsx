import React, { useState } from 'react';
import { Container, Typography, Box, Tabs, Tab, Alert } from '@mui/material';
import WalmartDemo from '../components/Demos/WalmartDemo';
import QuickDemo from '../components/Demos/QuickDemos';

/**
 * DemoPage - Hub for all demo presentations
 * Purpose: 3-minute hackathon demo and quick 90-second version
 */
const DemoPage: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);

  return (
    <Container maxWidth="xl" sx={{ py: 2 }}>
      <Alert severity="info" sx={{ mb: 3 }}>
        🎬 <strong>Demo Mode Active</strong> - Live API integration with real-time optimization and blockchain verification
      </Alert>

      <Tabs value={tabValue} onChange={(_, val) => setTabValue(val)} sx={{ mb: 3 }}>
        <Tab label="🏆 Full Demo (3 minutes)" />
        <Tab label="⚡ Quick Demo (90 seconds)" />
      </Tabs>

      {tabValue === 0 && <WalmartDemo />}
      {tabValue === 1 && <QuickDemo />}
    </Container>
  );
};

export default DemoPage;
