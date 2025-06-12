import React, { useState, useEffect } from 'react';
import {
  Container,
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
      setCertificates(certs || []);
      
      // ✅ FIXED: Sample ETT tokens with proper data structure
      setEttTokens([
        {
          token_id: 1001,
          route_id: 'walmart_nyc_demo_2025',
          trust_score: 94,
          carbon_impact_kg: 44.7,
          sustainability_rating: 91,
          created_at: new Date().toISOString(),
        },
        {
          token_id: 1002,
          route_id: 'demo_route_002',
          trust_score: 87,
          carbon_impact_kg: 35.7,
          sustainability_rating: 88,
          created_at: new Date().toISOString(),
        },
        {
          token_id: 1003,
          route_id: 'demo_route_003',
          trust_score: 92,
          carbon_impact_kg: 52.1,
          sustainability_rating: 95,
          created_at: new Date().toISOString(),
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
      
      // ✅ FIXED: Set empty arrays as fallback
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

  const handleCertificateCreated = (newCertificate: any) => {
    console.log('New certificate created:', newCertificate);
    
    // ✅ FIXED: Safe certificate handling
    if (newCertificate.certificate) {
      setCertificates(prev => [newCertificate.certificate, ...prev]);
    }
    
    // Add corresponding ETT token
    if (newCertificate.ettToken) {
      setEttTokens(prev => [newCertificate.ettToken, ...prev]);
    }

    // Add corresponding carbon credit
    if (newCertificate.carbonCredit) {
      setCarbonCredits(prev => [newCertificate.carbonCredit, ...prev]);
    }

    // ✅ FIXED: Auto-switch to Network Status tab to show the new certificate
    setTabValue(1);
  };

  // ✅ FIXED: Better route data with validation
  const generateSampleRouteData = () => {
    const timestamp = Date.now();
    return {
      route_id: `walmart_nyc_demo_${timestamp}`,
      vehicle_id: 'walmart_truck_001',
      carbon_saved: 44.7,
      cost_saved: 131.79,
      distance_km: 125.4,
      optimization_score: 94, // Integer value to prevent 422 errors
    };
  };

  const sampleRouteData = generateSampleRouteData();

  return (
    <Container maxWidth="xl" sx={{ py: 3 }}>
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" sx={{ fontWeight: 'bold', mb: 1 }}>
          🔗 Blockchain Certificate Management
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Manage blockchain certificates, Environmental Trust Tokens, and carbon credits with live demo capabilities
        </Typography>
        
        <Box sx={{ mt: 2, display: 'flex', gap: 2, flexWrap: 'wrap' }}>
          <Chip 
            label={`${certificates.length} Certificates`} 
            color="primary" 
            icon={<VerifiedOutlined />}
          />
          <Chip 
            label={`${ettTokens.length} ETT Tokens`} 
            color="success" 
            icon={<NatureOutlined />}
          />
          <Chip 
            label={`${carbonCredits.length} Carbon Credits`} 
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
          
          {/* ✅ FIXED: Show current route data being used */}
          <Alert severity="info" sx={{ mb: 3 }}>
            <Typography variant="body2">
              <strong>Demo Route Data:</strong> {sampleRouteData.route_id} | 
              Carbon: {sampleRouteData.carbon_saved} kg CO₂ | 
              Cost: ${sampleRouteData.cost_saved} | 
              Score: {sampleRouteData.optimization_score}
            </Typography>
          </Alert>
          
          <LiveCertificateGenerator 
            routeData={sampleRouteData}
            onCertificateCreated={handleCertificateCreated}
          />
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
    </Container>
  );
};

export default CertificateViewer;
