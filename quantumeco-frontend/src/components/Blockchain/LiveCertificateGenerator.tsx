// Components/LiveCertificateGenerator.tsx - Fixed version

import React, { useState } from 'react';
import {
  Card,
  CardContent,
  Typography,
  Button,
  Box,
  LinearProgress,
  Chip,
  Alert,
} from '@mui/material';
import {
  SecurityOutlined,
  PlayArrowOutlined,
} from '@mui/icons-material';
import { createLiveCertificate, createETTToken, createCarbonCredit } from '../../Services/blockchain';

interface LiveCertificateGeneratorProps {
  routeData: {
    route_id: string;
    vehicle_id: string;
    carbon_saved: number;
    cost_saved: number;
    distance_km: number;
    optimization_score: number;
  };
  onCertificateCreated?: (certificate: any) => void;
}

/**
 * LiveCertificateGenerator Component
 * Purpose: Demo live blockchain certificate creation (30 seconds of demo)
 * Features: Real-time certificate generation, transaction hash display, ETT creation
 */
const LiveCertificateGenerator: React.FC<LiveCertificateGeneratorProps> = ({
  routeData,
  onCertificateCreated,
}) => {
  const [creating, setCreating] = useState(false);
  const [certificate, setCertificate] = useState<any>(null);
  const [ettToken, setEttToken] = useState<any>(null);
  const [carbonCredit, setCarbonCredit] = useState<any>(null);
  const [step, setStep] = useState(0);
  const [error, setError] = useState<string | null>(null);

  const generateLiveCertificate = async () => {
    try {
      setCreating(true);
      setError(null);
      setStep(1);

      // Step 1: Create blockchain certificate
      console.log('Creating certificate with data:', routeData);
      const cert = await createLiveCertificate({
        route_id: routeData.route_id,
        vehicle_id: routeData.vehicle_id,
        carbon_saved: routeData.carbon_saved,
        cost_saved: routeData.cost_saved,
        distance_km: routeData.distance_km,
        optimization_score: routeData.optimization_score,
      });
      
      setCertificate(cert);
      setStep(2);

      // Step 2: Create Environmental Trust Token
      const ettData = {
        route_id: routeData.route_id,
        trust_score: Math.floor(Math.random() * 20) + 80, // 80-100
        carbon_impact: routeData.carbon_saved,
        sustainability_rating: Math.floor(Math.random() * 20) + 80, // 80-100
      };

      console.log('Creating ETT with data:', ettData);
      const ett = await createETTToken(ettData);
      setEttToken(ett);
      setStep(3);

      // Step 3: Create Carbon Credit
      const carbonCreditData = {
        route_id: routeData.route_id,
        carbon_amount_kg: routeData.carbon_saved,
        value_usd: routeData.carbon_saved * 2.5, // $2.5 per kg CO2
        vintage_year: new Date().getFullYear()
      };

      console.log('Creating carbon credit with data:', carbonCreditData);
      const credit = await createCarbonCredit(carbonCreditData);
      setCarbonCredit(credit);
      setStep(4);

      if (onCertificateCreated) {
        onCertificateCreated({ 
          certificate: cert, 
          ettToken: ett, 
          carbonCredit: credit 
        });
      }
    } catch (error) {
      console.error('Certificate creation failed:', error);
      setError(`Creation failed: ${error instanceof Error ? error.message : 'Unknown error'}`);
    } finally {
      setCreating(false);
    }
  };

  return (
    <Card sx={{ bgcolor: 'primary.50', border: '2px solid', borderColor: 'primary.main' }}>
      <CardContent>
        <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <SecurityOutlined />
          🔗 Live Blockchain Certificate Generation
        </Typography>

        {/* Route Summary */}
        <Box sx={{ mb: 3, p: 2, bgcolor: 'background.paper', borderRadius: 1 }}>
          <Typography variant="body2" color="text.secondary">
            Route: {routeData.route_id} | Vehicle: {routeData.vehicle_id}
          </Typography>
          <Box sx={{ display: 'flex', gap: 2, mt: 1 }}>
            <Chip label={`${routeData.carbon_saved.toFixed(1)} kg CO₂ saved`} color="success" size="small" />
            <Chip label={`$${routeData.cost_saved.toFixed(2)} saved`} color="primary" size="small" />
            <Chip label={`Score: ${routeData.optimization_score}`} color="info" size="small" />
          </Box>
        </Box>

        {/* Error Display */}
        {error && (
          <Alert severity="error" sx={{ mb: 3 }}>
            {error}
          </Alert>
        )}

        {/* Generation Progress */}
        {creating && (
          <Box sx={{ mb: 3 }}>
            <Typography variant="body2" gutterBottom>
              {step === 1 && '🔄 Creating blockchain certificate...'}
              {step === 2 && '🪙 Minting Environmental Trust Token...'}
              {step === 3 && '💰 Generating Carbon Credits...'}
              {step === 4 && '✅ Verification complete!'}
            </Typography>
            <LinearProgress 
              variant="determinate" 
              value={(step / 4) * 100} 
              sx={{ height: 8, borderRadius: 4 }}
            />
          </Box>
        )}

        {/* Generate Button */}
        <Button
          variant="contained"
          size="large"
          fullWidth
          startIcon={creating ? <PlayArrowOutlined /> : <SecurityOutlined />}
          onClick={generateLiveCertificate}
          disabled={creating}
          sx={{ mb: 3 }}
        >
          {creating ? 'Generating Certificate...' : 'Generate Live Certificate'}
        </Button>

        {/* Certificate Results */}
        {certificate && (
          <Alert severity="success" sx={{ mb: 2 }}>
            <Typography variant="h6" gutterBottom>
              ✅ Certificate Generated Successfully!
            </Typography>
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
              <Typography variant="body2">
                <strong>Transaction Hash:</strong> {certificate.transaction_hash?.slice(0, 20)}...
              </Typography>
              <Typography variant="body2">
                <strong>Block Number:</strong> {certificate.block_number?.toLocaleString()}
              </Typography>
              <Typography variant="body2">
                <strong>Certificate ID:</strong> {certificate.certificate_id}
              </Typography>
            </Box>
          </Alert>
        )}

        {/* ETT Token Results */}
        {ettToken && (
          <Alert severity="info" sx={{ mb: 2 }}>
            <Typography variant="h6" gutterBottom>
              🪙 Environmental Trust Token Minted!
            </Typography>
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
              <Typography variant="body2">
                <strong>Token ID:</strong> #{ettToken.token_id}
              </Typography>
              <Typography variant="body2">
                <strong>Trust Score:</strong> {ettToken.trust_score}%
              </Typography>
              <Typography variant="body2">
                <strong>Sustainability Rating:</strong> {ettToken.sustainability_rating}%
              </Typography>
            </Box>
          </Alert>
        )}

        {/* Carbon Credit Results */}
        {carbonCredit && (
          <Alert severity="warning">
            <Typography variant="h6" gutterBottom>
              💰 Carbon Credits Generated!
            </Typography>
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
              <Typography variant="body2">
                <strong>Credit ID:</strong> #{carbonCredit.credit_id}
              </Typography>
              <Typography variant="body2">
                <strong>Carbon Amount:</strong> {carbonCredit.carbon_amount_kg} kg CO₂
              </Typography>
              <Typography variant="body2">
                <strong>Value:</strong> ${carbonCredit.value_usd.toFixed(2)}
              </Typography>
            </Box>
          </Alert>
        )}
      </CardContent>
    </Card>
  );
};

export default LiveCertificateGenerator;
