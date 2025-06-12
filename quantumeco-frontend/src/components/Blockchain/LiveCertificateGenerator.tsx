// import React, { useState } from 'react';
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

  // ✅ FIXED: Safe data formatting to prevent 422 errors
  const formatCertificateData = (data: any) => {
    const carbon_saved = Number(parseFloat(data.carbon_saved || 0).toFixed(2));
    const cost_saved = Number(parseFloat(data.cost_saved || 0).toFixed(2));
    return {
      route_id: String(data.route_id || `route_${Date.now()}`),
      vehicle_id: String(data.vehicle_id || 'vehicle_001'),
      carbon_saved_kg: carbon_saved,
      cost_saved_usd: cost_saved,
      carbon_saved, // Add original property for API compatibility
      cost_saved,   // Add original property for API compatibility
      distance_km: Number(parseFloat(data.distance_km || 0).toFixed(1)),
      optimization_score: Math.round(Number(data.optimization_score || 0)),
    };
  };

  // ✅ FIXED: Normalize ETT token to ensure all required fields exist
  const normalizeETTToken = (ettResponse: any, routeId: string, carbonSaved: number) => {
    return {
      token_id: ettResponse?.token_id || Date.now(), // ✅ Guaranteed token_id
      route_id: routeId,
      trust_score: ettResponse?.trust_score || 90,
      carbon_impact_kg: carbonSaved, // ✅ Correct field name
      sustainability_rating: ettResponse?.sustainability_rating || 85,
      created_at: new Date().toISOString(), // ✅ Add created_at
      ...ettResponse // Spread any additional backend fields
    };
  };

  // ✅ FIXED: Normalize carbon credit to ensure all required fields exist
  const normalizeCarbonCredit = (creditResponse: any, routeId: string, carbonAmount: number, valueUsd: number) => {
    return {
      credit_id: creditResponse?.credit_id || Date.now(),
      route_id: routeId,
      carbon_amount_kg: carbonAmount,
      value_usd: valueUsd,
      vintage_year: new Date().getFullYear(),
      status: 'verified',
      created_at: new Date().toISOString(),
      ...creditResponse
    };
  };

  const generateLiveCertificate = async () => {
    try {
      setCreating(true);
      setError(null);
      setStep(1);

      // ✅ FIXED: Format data to match backend expectations
      const formattedData = formatCertificateData(routeData);
      console.log('Creating certificate with formatted data:', formattedData);

      // Validate data before sending
      if (!formattedData.route_id || !formattedData.vehicle_id) {
        throw new Error('Missing required route_id or vehicle_id');
      }

      if (formattedData.carbon_saved_kg <= 0) {
        throw new Error('Carbon saved must be greater than 0');
      }

      if (formattedData.cost_saved_usd <= 0) {
        throw new Error('Cost saved must be greater than 0');
      }

      if (formattedData.optimization_score < 0 || formattedData.optimization_score > 100) {
        throw new Error('Optimization score must be between 0 and 100');
      }

      // ✅ FIXED: Step 1: Create blockchain certificate with ONLY formatted data
      const cert = await createLiveCertificate(formattedData); // ✅ Don't overwrite formatted fields
      setCertificate(cert);
      setStep(2);

      // ✅ FIXED: Step 2: Create Environmental Trust Token with correct field names
      const ettData = {
        route_id: formattedData.route_id,
        trust_score: Math.min(100, Math.max(80, formattedData.optimization_score + Math.floor(Math.random() * 10))),
        carbon_impact: formattedData.carbon_saved_kg, // Use carbon_impact as required by the API
        sustainability_rating: Math.min(100, Math.max(80, formattedData.optimization_score + Math.floor(Math.random() * 15))),
      };

      console.log('Creating ETT with data:', ettData);
      const ettResponse = await createETTToken(ettData);
      
      // ✅ FIXED: Normalize ETT token response to ensure all required fields
      const normalizedETT = normalizeETTToken(ettResponse, formattedData.route_id, formattedData.carbon_saved_kg);
      setEttToken(normalizedETT);
      setStep(3);

      // ✅ FIXED: Step 3: Create Carbon Credit
      const carbonCreditData = {
        route_id: formattedData.route_id,
        carbon_amount_kg: formattedData.carbon_saved_kg,
        value_usd: Number((formattedData.carbon_saved_kg * 2.5).toFixed(2)),
        vintage_year: new Date().getFullYear()
      };

      console.log('Creating carbon credit with data:', carbonCreditData);
      const creditResponse = await createCarbonCredit(carbonCreditData);
      
      // ✅ FIXED: Normalize carbon credit response
      const normalizedCredit = normalizeCarbonCredit(
        creditResponse, 
        formattedData.route_id, 
        formattedData.carbon_saved_kg, 
        carbonCreditData.value_usd
      );
      setCarbonCredit(normalizedCredit);
      setStep(4);

      // ✅ FIXED: Pass normalized data structures to parent
      if (onCertificateCreated) {
        onCertificateCreated({ 
          certificate: cert, 
          ettToken: normalizedETT, // ✅ Guaranteed to have all required fields
          carbonCredit: normalizedCredit // ✅ Guaranteed to have all required fields
        });
      }
    } catch (error: any) {
      console.error('Certificate creation failed:', error);
      
      let errorMessage = 'Unknown error occurred';
      
      if (error.response?.status === 422) {
        const validationErrors = error.response?.data?.detail || [];
        if (Array.isArray(validationErrors)) {
          errorMessage = `Validation failed: ${validationErrors.map((err: any) => err.msg || err).join(', ')}`;
        } else {
          errorMessage = `Validation failed: ${error.response?.data?.detail || 'Invalid data format'}`;
        }
      } else if (error.response?.status === 400) {
        errorMessage = `Bad request: ${error.response?.data?.detail || error.message}`;
      } else if (error.response?.status === 500) {
        errorMessage = 'Server error: Please check if Ganache is running';
      } else if (error.message?.includes('Network Error')) {
        errorMessage = 'Network error: Cannot connect to backend';
      } else {
        errorMessage = error.message || 'Certificate creation failed';
      }
      
      setError(errorMessage);
    } finally {
      setCreating(false);
    }
  };

  // ✅ FIXED: Safe number display to prevent rendering errors
  const safeDisplayNumber = (value: any, decimals: number = 1): string => {
    if (value === null || value === undefined || isNaN(value)) return '0';
    return Number(value).toFixed(decimals);
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
          <Box sx={{ display: 'flex', gap: 2, mt: 1, flexWrap: 'wrap' }}>
            <Chip 
              label={`${safeDisplayNumber(routeData.carbon_saved)} kg CO₂ saved`} 
              color="success" 
              size="small" 
            />
            <Chip 
              label={`$${safeDisplayNumber(routeData.cost_saved, 2)} saved`} 
              color="primary" 
              size="small" 
            />
            <Chip 
              label={`Score: ${Math.round(routeData.optimization_score || 0)}`} 
              color="info" 
              size="small" 
            />
          </Box>
        </Box>

        {/* Error Display */}
        {error && (
          <Alert severity="error" sx={{ mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              ❌ Certificate Creation Failed
            </Typography>
            <Typography variant="body2" sx={{ mb: 2 }}>
              {error}
            </Typography>
            <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
              <Button size="small" variant="outlined" onClick={() => setError(null)}>
                Dismiss
              </Button>
              <Button size="small" variant="contained" onClick={generateLiveCertificate}>
                Retry
              </Button>
            </Box>
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
                <strong>Transaction Hash:</strong> {certificate.transaction_hash?.slice(0, 20) || 'N/A'}...
              </Typography>
              <Typography variant="body2">
                <strong>Block Number:</strong> {certificate.block_number?.toLocaleString() || 'N/A'}
              </Typography>
              <Typography variant="body2">
                <strong>Certificate ID:</strong> {certificate.certificate_id || 'N/A'}
              </Typography>
              <Typography variant="body2">
                <strong>Status:</strong> <Chip label="Verified" color="success" size="small" />
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
                <strong>Token ID:</strong> #{ettToken.token_id || 'N/A'}
              </Typography>
              <Typography variant="body2">
                <strong>Trust Score:</strong> {ettToken.trust_score || 0}%
              </Typography>
              <Typography variant="body2">
                <strong>Sustainability Rating:</strong> {ettToken.sustainability_rating || 0}%
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
                <strong>Credit ID:</strong> #{carbonCredit.credit_id || 'N/A'}
              </Typography>
              <Typography variant="body2">
                <strong>Carbon Amount:</strong> {safeDisplayNumber(carbonCredit.carbon_amount_kg)} kg CO₂
              </Typography>
              <Typography variant="body2">
                <strong>Value:</strong> ${safeDisplayNumber(carbonCredit.value_usd, 2)}
              </Typography>
            </Box>
          </Alert>
        )}
      </CardContent>
    </Card>
  );
};

export default LiveCertificateGenerator;
