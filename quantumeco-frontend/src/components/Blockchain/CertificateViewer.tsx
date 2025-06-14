import React, { useState, useEffect } from 'react';
import {
  Typography,
  Box,
  Card,
  CardContent,
  Tabs,
  Tab,
  Button,
  Alert,
  Chip,
} from '@mui/material';
import {
  SecurityOutlined,
  VerifiedOutlined,
  NatureOutlined,
  AccountBalanceWalletOutlined,
  ExploreOutlined,
  PlayArrowOutlined,
} from '@mui/icons-material';
import LiveCertificateGenerator from './LiveCertificateGenerator';
import BlockchainVerification from './BlockchainVerification';
import ETTDisplay from './ETTDisplay';
import CarbonCreditDisplay from './CarbonCreditDisplay';
import { getRecentCertificates } from '../../Services/api';
import type { ETTToken } from './ETTDisplay';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;
  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`blockchain-tabpanel-${index}`}
      aria-labelledby={`blockchain-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

const CertificateViewer: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  // ✅ FIXED: Ensure proper array initialization
  const [certificates, setCertificates] = useState<any[]>([]);
  const [ettTokens, setEttTokens] = useState<ETTToken[]>([]);
  const [carbonCredits, setCarbonCredits] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadCertificateData();
  }, []);

  const loadCertificateData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const certs = await getRecentCertificates(10);
      // ✅ FIXED: Ensure we always set an array
      setCertificates(Array.isArray(certs) ? certs : []);
      
      // Sample ETT tokens
      setEttTokens([
        {
          token_id: 1001,
          route_id: 'walmart_nyc_demo_2025',
          trust_score: 94,
          carbon_impact_kg: 44.7,
          sustainability_rating: 91,
          created_at: new Date().toISOString(),
          token_status: 'active',
          is_valid: true,
          owner: 'demo_user_1',
        },
        {
          token_id: 1002,
          route_id: 'demo_route_002',
          trust_score: 87,
          carbon_impact_kg: 35.7,
          sustainability_rating: 88,
          created_at: new Date().toISOString(),
          token_status: 'active',
          is_valid: true,
          owner: 'demo_user_2',
        },
        {
          token_id: 1003,
          route_id: 'demo_route_003',
          trust_score: 92,
          carbon_impact_kg: 52.1,
          sustainability_rating: 95,
          created_at: new Date().toISOString(),
          token_status: 'active',
          is_valid: true,
          owner: 'demo_user_3',
        }
      ]);

      setCarbonCredits([
        {
          credit_id: 5001,
          route_id: 'walmart_nyc_demo_2025',
          carbon_amount_kg: 44.7,
          value_usd: 111.75,
          vintage_year: 2025,
          status: 'verified',
          created_at: new Date().toISOString(),
        },
        {
          credit_id: 5002,
          route_id: 'demo_route_002',
          carbon_amount_kg: 35.7,
          value_usd: 89.25,
          vintage_year: 2025,
          status: 'verified',
          created_at: new Date().toISOString(),
        }
      ]);
    } catch (error: any) {
      console.error('Failed to load certificate data:', error);
      setError(`Failed to load data: ${error.message || 'Unknown error'}`);
      
      // Always set empty arrays as fallback
      setCertificates([]);
      setEttTokens([]);
      setCarbonCredits([]);
    } finally {
      setLoading(false);
    }
  };

  const handleTabChange = (_event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  // ✅ FIXED: Completely rewritten to prevent glitches and auto-tab switching
  const handleCertificateCreated = (newCertificate: any) => {
    console.log('New certificate created:', newCertificate);
    
    try {
      // ✅ FIXED: Safe array updates with proper validation
      if (newCertificate?.certificate) {
        setCertificates(currentCerts => {
          const validCerts = Array.isArray(currentCerts) ? currentCerts : [];
          return [newCertificate.certificate, ...validCerts];
        });
      }
      
      // Add corresponding ETT token
      if (newCertificate?.ettToken) {
        setEttTokens(currentTokens => {
          const validTokens = Array.isArray(currentTokens) ? currentTokens : [];
          return [newCertificate.ettToken, ...validTokens];
        });
      }

      // Add corresponding carbon credit
      if (newCertificate?.carbonCredit) {
        setCarbonCredits(currentCredits => {
          const validCredits = Array.isArray(currentCredits) ? currentCredits : [];
          return [newCertificate.carbonCredit, ...validCredits];
        });
      }

      // ✅ FIXED: REMOVED auto tab switching - let user stay on current tab
      // setTabValue(1); // <-- This was causing the unwanted tab switch!
      
      console.log('✅ Certificate added successfully without switching tabs');
      
    } catch (err) {
      console.error('Error handling certificate creation:', err);
      setError('Failed to add new certificate to display');
    }
  };

  const generateSampleRouteData = () => {
    const timestamp = Date.now();
    return {
      route_id: `walmart_nyc_demo_${timestamp}`,
      vehicle_id: 'walmart_truck_001',
      carbon_saved: 44.7,
      cost_saved: 131.79,
      distance_km: 125.4,
      optimization_score: 94,
    };
  };

  const sampleRouteData = generateSampleRouteData();

  return (
    
    <Box sx={{ 
      width: '100vw',
      minHeight: '100vh',
      overflow: 'hidden',
      boxSizing: 'border-box'
    }}>
      <Box sx={{ height: 24 }} ></Box>
      <Box sx={{ px: { xs: 2, sm: 3, md: 4 }, py: 3 }}>
        {/* Header */}
        <Box sx={{ mb: 4 }}>
          <Typography variant="h4" component="h1" sx={{ fontWeight: 'bold', mb: 1 }}>
            🔗 Blockchain Certificate Management
          </Typography>
          {/* <Typography variant="body1" color="text.secondary">
            Manage blockchain certificates, Environmental Trust Tokens, and carbon credits with live demo capabilities
          </Typography> */}
          <Typography 
  variant="body1" 
  color="text.secondary"
  align="center"
>
   Manage blockchain certificates, Environmental Trust Tokens, and carbon credits with live demo capabilities
</Typography>
          <Box sx={{ height: 24 }} ></Box>
          
          <Box sx={{ mt: 2, display: 'flex', gap: 2, flexWrap: 'wrap' }}>
            <Chip 
              label={`${Array.isArray(certificates) ? certificates.length : 0} Certificates`} 
              color="primary" 
              icon={<VerifiedOutlined />}
            />
            <Chip 
              label={`${Array.isArray(ettTokens) ? ettTokens.length : 0} ETT Tokens`} 
              color="success" 
              icon={<NatureOutlined />}
            />
            <Chip 
              label={`${Array.isArray(carbonCredits) ? carbonCredits.length : 0} Carbon Credits`} 
              color="info" 
              icon={<AccountBalanceWalletOutlined />}
            />
          </Box>
        </Box>

        {/* Error Alert */}
        {error && (
          <Alert severity="error" sx={{ mb: 3 }} onClose={() => setError(null)}>
            {error}
          </Alert>
        )}

        {/* Demo Alert */}
        <Alert severity="info" sx={{ mb: 3 }}>
          <Typography variant="h6" gutterBottom>
            🎬 Live Demo Mode Active
          </Typography>
          <Typography variant="body2">
            Generate live blockchain certificates and watch real-time verification in action. 
            Perfect for demonstrating quantum-inspired optimization with blockchain verification.
          </Typography>
        </Alert>

        {/* Tabs Navigation */}
        <Card sx={{ mb: 3 }}>
          <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
            <Tabs value={tabValue} onChange={handleTabChange} aria-label="blockchain tabs">
              <Tab 
                label="Live Generator" 
                icon={<PlayArrowOutlined />} 
                iconPosition="start"
              />
              <Tab 
                label="Network Status" 
                icon={<ExploreOutlined />} 
                iconPosition="start"
              />
              <Tab 
                label="ETT Tokens" 
                icon={<NatureOutlined />} 
                iconPosition="start"
              />
              <Tab 
                label="Carbon Credits" 
                icon={<AccountBalanceWalletOutlined />} 
                iconPosition="start"
              />
            </Tabs>
          </Box>

          {/* Tab 0: Live Certificate Generation */}
          <TabPanel value={tabValue} index={0}>
            <Typography variant="h6" gutterBottom>
              🚀 Live Certificate Generation for Demo
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
              Generate blockchain certificates in real-time during your presentation. 
              Perfect for the 30-second blockchain segment of your demo.
            </Typography>
            
            <Alert severity="info" sx={{ mb: 3 }}>
              <Typography variant="body2">
                <strong>Demo Route Data:</strong> {sampleRouteData.route_id} | 
                Carbon: {sampleRouteData.carbon_saved} kg CO₂ | 
                Cost: ${sampleRouteData.cost_saved} | 
                Score: {sampleRouteData.optimization_score}
              </Typography>
            </Alert>
            
            {/* ✅ FIXED: Success message will now show without switching tabs */}
            <LiveCertificateGenerator 
              routeData={sampleRouteData}
              onCertificateCreated={handleCertificateCreated}
            />
            
            {/* ✅ ADDED: Success indicator when certificate is created */}
            {certificates.length > 0 && (
              <Alert severity="success" sx={{ mt: 3 }}>
                <Typography variant="body2">
                  ✅ Latest certificate generated! View it in the Network Status tab or continue generating more certificates here.
                </Typography>
              </Alert>
            )}
          </TabPanel>

          {/* Tab 1: Blockchain Network Status */}
          <TabPanel value={tabValue} index={1}>
            <Typography variant="h6" gutterBottom>
              🌐 Blockchain Network Verification
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
              Real-time blockchain network status and transaction verification.
            </Typography>
            
            <BlockchainVerification />
          </TabPanel>

          {/* Tab 2: Environmental Trust Tokens */}
          <TabPanel value={tabValue} index={2}>
            <Typography variant="h6" gutterBottom>
              🌱 Environmental Trust Tokens (ETT)
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
              Blockchain-verified sustainability scoring with transparent environmental impact metrics.
            </Typography>
            
            <ETTDisplay tokens={ettTokens} />
          </TabPanel>

          {/* Tab 3: Carbon Credits */}
          <TabPanel value={tabValue} index={3}>
            <Typography variant="h6" gutterBottom>
              💰 Tradeable Carbon Credits
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
              Monetize environmental impact through blockchain-verified carbon offset certificates.
            </Typography>
            
            <CarbonCreditDisplay 
              carbonCredits={carbonCredits}
              onTradeCredit={(creditId) => console.log(`Trading credit ${creditId}`)}
            />
          </TabPanel>
        </Card>

        {/* Quick Actions */}
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              🎯 Quick Demo Actions
            </Typography>
            <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
              <Button 
                variant="contained" 
                startIcon={<SecurityOutlined />}
                onClick={() => setTabValue(0)}
              >
                Generate Live Certificate
              </Button>
              <Button 
                variant="outlined" 
                startIcon={<ExploreOutlined />}
                onClick={() => setTabValue(1)}
              >
                Check Network Status
              </Button>
              <Button 
                variant="outlined" 
                startIcon={<NatureOutlined />}
                onClick={() => setTabValue(2)}
              >
                View ETT Tokens
              </Button>
              <Button 
                variant="outlined" 
                startIcon={<AccountBalanceWalletOutlined />}
                onClick={() => setTabValue(3)}
              >
                View Carbon Credits
              </Button>
              <Button 
                variant="text" 
                onClick={loadCertificateData}
                disabled={loading}
              >
                {loading ? 'Refreshing...' : 'Refresh Data'}
              </Button>
            </Box>
          </CardContent>
        </Card>
      </Box>
    </Box>
  );
};

export default CertificateViewer;
