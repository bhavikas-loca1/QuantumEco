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
import { createLiveCertificate, createETTToken } from '../../Services/blockchain';

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
  const [step, setStep] = useState(0);

  const generateLiveCertificate = async () => {
    try {
      setCreating(true);
      setStep(1);

      // Step 1: Create blockchain certificate
      const cert = await createLiveCertificate(routeData);
      setCertificate(cert);
      setStep(2);

      const ettData = {
      route_id: certificate.route_id,
      trust_score: Math.floor(Math.random() * 20) + 80, // 80-100
      carbon_impact: certificate.carbon_saved_kg,
      sustainability_rating: Math.floor(Math.random() * 20) + 80, // 80-100
      };

      // // Step 2: Create Environmental Trust Token
      // const ett = await createETTToken({
      //   route_id: routeData.route_id,
      //   trust_score: routeData.optimization_score,
      //   carbon_impact: routeData.carbon_saved,
      //   sustainability_rating: Math.min(routeData.optimization_score + 2, 100),
      // });

      await createETTToken(ettData);

      setEttToken(ettData);
      setStep(3);

      if (onCertificateCreated) {
        onCertificateCreated({ certificate: cert, ettData });
      }
    } catch (error) {
      console.error('Certificate creation failed:', error);
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

        {/* Generation Progress */}
        {creating && (
          <Box sx={{ mb: 3 }}>
            <Typography variant="body2" gutterBottom>
              {step === 1 && '🔄 Creating blockchain certificate...'}
              {step === 2 && '🪙 Minting Environmental Trust Token...'}
              {step === 3 && '✅ Verification complete!'}
            </Typography>
            <LinearProgress 
              variant="determinate" 
              value={(step / 3) * 100} 
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
                <strong>Transaction Hash:</strong> {certificate.transaction_hash.slice(0, 20)}...
              </Typography>
              <Typography variant="body2">
                <strong>Block Number:</strong> {certificate.block_number.toLocaleString()}
              </Typography>
              <Typography variant="body2">
                <strong>Certificate ID:</strong> {certificate.certificate_id}
              </Typography>
            </Box>
          </Alert>
        )}

        {/* ETT Token Results */}
        {ettToken && (
          <Alert severity="info">
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
      </CardContent>
    </Card>
  );
};

export default LiveCertificateGenerator;
