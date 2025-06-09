import React, { useState } from 'react';
import { Box, Typography, Button } from '@mui/material';
import LiveCertificateGenerator from '../Blockchain/LiveCertificateGenerator';
import BlockchainVerification from '../Blockchain/BlockchainVerification';
import ETTDisplay from '../Blockchain/ETTDisplay';
import CarbonCreditDisplay from '../Blockchain/CarbonCreditDisplay';

interface BlockchainDemoProps {
  routeData: any;
  onDemoComplete?: () => void;
}

/**
 * BlockchainDemo Component
 * Purpose: Orchestrate 30-second blockchain demonstration
 * Features: Live certificate generation, ETT creation, verification display
 */
const BlockchainDemo: React.FC<BlockchainDemoProps> = ({ 
  routeData, 
  onDemoComplete 
}) => {
  const [certificates, setCertificates] = useState<any[]>([]);
  const [ettTokens, setEttTokens] = useState<any[]>([]);
  const [carbonCredits, setCarbonCredits] = useState<any[]>([]);

  const handleCertificateCreated = (data: any) => {
    setCertificates(prev => [...prev, data.certificate]);
    setEttTokens(prev => [...prev, data.ett]);
    
    // Simulate carbon credit creation
    const credit = {
      credit_id: Math.floor(Math.random() * 1000000),
      route_id: data.certificate.route_id,
      carbon_amount_kg: data.certificate.carbon_saved_kg,
      value_usd: data.certificate.carbon_saved_kg * 2.5, // $2.50 per kg CO₂
      created_at: new Date().toISOString(),
    };
    setCarbonCredits(prev => [...prev, credit]);
  };

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
      <Typography variant="h5" sx={{ fontWeight: 'bold', textAlign: 'center' }}>
        🔗 Blockchain Verification Demo (30 seconds)
      </Typography>

      <Box sx={{ display: 'flex', flexDirection: { xs: 'column', lg: 'row' }, gap: 3 }}>
        {/* Certificate Generation */}
        <Box sx={{ flex: 1 }}>
          <LiveCertificateGenerator 
            routeData={routeData}
            onCertificateCreated={handleCertificateCreated}
          />
        </Box>

        {/* Verification Status */}
        <Box sx={{ flex: 1 }}>
          <BlockchainVerification />
        </Box>
      </Box>

      <Box sx={{ display: 'flex', flexDirection: { xs: 'column', lg: 'row' }, gap: 3 }}>
        {/* ETT Tokens */}
        <Box sx={{ flex: 1 }}>
          <ETTDisplay tokens={ettTokens} />
        </Box>

        {/* Carbon Credits */}
        <Box sx={{ flex: 1 }}>
          <CarbonCreditDisplay credits={carbonCredits} />
        </Box>
      </Box>

      {certificates.length > 0 && (
        <Button 
          variant="contained" 
          color="success" 
          onClick={onDemoComplete}
          sx={{ alignSelf: 'center', mt: 2 }}
        >
          ✅ Blockchain Verification Complete - Continue Demo
        </Button>
      )}
    </Box>
  );
};

export default BlockchainDemo;
