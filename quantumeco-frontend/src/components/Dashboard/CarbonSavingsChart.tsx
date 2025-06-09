import React from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Chip,
  Avatar,
  Divider,
  Button,
  IconButton,
  Tooltip,
  Skeleton,
} from '@mui/material';
import {
  VerifiedOutlined,
  LinkOutlined,
  CalendarTodayOutlined,
  NatureOutlined,
  SecurityOutlined,
  TrendingUpOutlined,
  ForestOutlined,
  DirectionsCarOutlined,
  HomeOutlined,
} from '@mui/icons-material';
import { type Certificate } from '../../Services/types';

interface CarbonSavingsCertificateProps {
  certificates: Certificate[] | any[];
  environmentalImpact?: {
    trees_planted_equivalent: number;
    cars_off_road_days: number;
    homes_powered_hours: number;
    miles_not_driven: number;
    gallons_fuel_saved: number;
  };
  loading?: boolean;
}

/**
 * CarbonSavingsCertificate Component
 * Purpose: Displays blockchain certificates and environmental impact metrics
 * Features: Certificate verification status, environmental equivalents, blockchain transaction links
 */
const CarbonSavingsCertificate: React.FC<CarbonSavingsCertificateProps> = ({
  certificates,
  environmentalImpact,
  loading = false,
}) => {
  const formatCertificateId = (id: string) => {
    if (!id) return 'Unknown';
    return `${id.slice(0, 8)}...${id.slice(-4)}`;
  };

  const formatTransactionHash = (hash: string) => {
    if (!hash) return 'Unknown';
    return `${hash.slice(0, 10)}...${hash.slice(-8)}`;
  };

  const getStatusColor = (status: string) => {
    switch (status?.toLowerCase()) {
      case 'verified':
        return 'success';
      case 'pending':
        return 'warning';
      case 'rejected':
      case 'failed':
        return 'error';
      default:
        return 'default';
    }
  };

  const formatDateTime = (dateString: string) => {
    try {
      const date = new Date(dateString);
      return date.toLocaleString('en-US', {
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
      });
    } catch {
      return 'Recent';
    }
  };

  if (loading) {
    return (
      <Card sx={{ height: '100%' }}>
        <CardContent>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 3 }}>
            <Skeleton variant="circular" width={24} height={24} />
            <Skeleton variant="text" width="60%" height={24} />
            <Skeleton variant="rectangular" width={80} height={24} />
          </Box>
          
          {/* Environmental Impact Skeleton */}
          <Skeleton variant="rectangular" width="100%" height={120} sx={{ mb: 3, borderRadius: 1 }} />
          
          {/* Certificates Skeleton */}
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            {[1, 2, 3].map((i) => (
              <Card key={i} variant="outlined">
                <CardContent sx={{ py: 2 }}>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
                    <Skeleton variant="circular" width={40} height={40} />
                    <Box sx={{ flex: 1 }}>
                      <Skeleton variant="text" width="80%" height={20} />
                      <Skeleton variant="text" width="60%" height={16} />
                    </Box>
                    <Skeleton variant="rectangular" width={60} height={24} />
                  </Box>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                    <Skeleton variant="text" width="30%" height={16} />
                    <Skeleton variant="text" width="30%" height={16} />
                    <Skeleton variant="text" width="30%" height={16} />
                  </Box>
                </CardContent>
              </Card>
            ))}
          </Box>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <CardContent sx={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
        {/* Header */}
        <Box
          sx={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            mb: 3,
          }}
        >
          <Typography variant="h6" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <SecurityOutlined color="success" />
            Blockchain Certificates
          </Typography>
          <Chip
            label={`${certificates?.length || 0} Verified`}
            color="success"
            size="small"
            icon={<VerifiedOutlined />}
          />
        </Box>

        {/* Environmental Impact Summary */}
        {environmentalImpact && (
          <Box sx={{ mb: 3 }}>
            <Card
              variant="outlined"
              sx={{
                background: 'linear-gradient(135deg, #e8f5e8 0%, #f1f8f1 100%)',
                border: '1px solid #4caf50',
              }}
            >
              <CardContent sx={{ py: 2 }}>
                <Typography 
                  variant="subtitle2" 
                  color="success.main" 
                  gutterBottom
                  sx={{ display: 'flex', alignItems: 'center', gap: 1 }}
                >
                  <NatureOutlined fontSize="small" />
                  Environmental Impact Equivalents
                </Typography>
                <Box
                  sx={{
                    display: 'flex',
                    flexWrap: 'wrap',
                    gap: 2,
                    mt: 1,
                  }}
                >
                  <Box sx={{ textAlign: 'center', minWidth: 80 }}>
                    <Typography variant="h6" color="success.main" sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 0.5 }}>
                      <ForestOutlined fontSize="small" />
                      {Math.round(environmentalImpact.trees_planted_equivalent || 0)}
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      Trees Planted
                    </Typography>
                  </Box>
                  <Divider orientation="vertical" flexItem />
                  <Box sx={{ textAlign: 'center', minWidth: 80 }}>
                    <Typography variant="h6" color="success.main" sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 0.5 }}>
                      <DirectionsCarOutlined fontSize="small" />
                      {Math.round(environmentalImpact.cars_off_road_days || 0)}
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      Car-Free Days
                    </Typography>
                  </Box>
                  <Divider orientation="vertical" flexItem />
                  <Box sx={{ textAlign: 'center', minWidth: 80 }}>
                    <Typography variant="h6" color="success.main" sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 0.5 }}>
                      <HomeOutlined fontSize="small" />
                      {Math.round(environmentalImpact.homes_powered_hours || 0)}
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      Home Hours
                    </Typography>
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Box>
        )}

        {/* Certificates List */}
        <Box sx={{ flex: 1, display: 'flex', flexDirection: 'column', gap: 2 }}>
          {!certificates || certificates.length === 0 ? (
            <Box
              sx={{
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                py: 4,
                color: 'text.secondary',
              }}
            >
              <NatureOutlined sx={{ fontSize: 48, mb: 2, opacity: 0.5 }} />
              <Typography variant="body1" sx={{ mb: 1 }}>
                No certificates available
              </Typography>
              <Typography variant="body2" sx={{ textAlign: 'center' }}>
                Blockchain certificates will appear here after route optimization with environmental impact verification
              </Typography>
            </Box>
          ) : (
            certificates.slice(0, 6).map((cert, index) => (
              <Card
                key={cert.certificate_id || index}
                variant="outlined"
                sx={{
                  transition: 'all 0.2s ease',
                  '&:hover': {
                    boxShadow: 2,
                    transform: 'translateY(-1px)',
                  },
                }}
              >
                <CardContent sx={{ py: 2 }}>
                  {/* Certificate Header */}
                  <Box
                    sx={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'flex-start',
                      mb: 2,
                    }}
                  >
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                      <Avatar
                        sx={{
                          bgcolor: 'success.main',
                          width: 40,
                          height: 40,
                        }}
                      >
                        <VerifiedOutlined />
                      </Avatar>
                      <Box>
                        <Typography variant="subtitle2" sx={{ fontWeight: 'bold' }}>
                          {formatCertificateId(cert.certificate_id)}
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          Route: {cert.route_id || 'Unknown'}
                        </Typography>
                      </Box>
                    </Box>
                    
                    <Chip
                      label={cert.certificate_status || 'verified'}
                      color={getStatusColor(cert.certificate_status || 'verified')}
                      size="small"
                    />
                  </Box>

                  {/* Metrics */}
                  <Box
                    sx={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      mb: 2,
                      flexWrap: 'wrap',
                      gap: 1,
                    }}
                  >
                    <Box sx={{ textAlign: 'center', flex: 1, minWidth: 80 }}>
                      <Typography variant="h6" color="success.main">
                        {(cert.carbon_saved_kg || 0).toFixed(1)}
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        kg CO₂ Saved
                      </Typography>
                    </Box>
                    <Box sx={{ textAlign: 'center', flex: 1, minWidth: 80 }}>
                      <Typography variant="h6" color="primary.main">
                        ${(cert.cost_saved_usd || 0).toFixed(2)}
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        Cost Saved
                      </Typography>
                    </Box>
                    <Box sx={{ textAlign: 'center', flex: 1, minWidth: 80 }}>
                      <Typography variant="h6" color="info.main">
                        {cert.optimization_score || 0}
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        Score
                      </Typography>
                    </Box>
                  </Box>

                  {/* Blockchain Info */}
                  <Box
                    sx={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center',
                      pt: 1,
                      borderTop: '1px solid',
                      borderColor: 'divider',
                      flexWrap: 'wrap',
                      gap: 1,
                    }}
                  >
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <CalendarTodayOutlined sx={{ fontSize: 16, color: 'text.secondary' }} />
                      <Typography variant="caption" color="text.secondary">
                        {formatDateTime(cert.created_at)}
                      </Typography>
                    </Box>
                    
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <Tooltip title={cert.transaction_hash || 'Transaction Hash'}>
                        <IconButton size="small" color="primary">
                          <LinkOutlined sx={{ fontSize: 16 }} />
                        </IconButton>
                      </Tooltip>
                      <Typography variant="caption" color="text.secondary">
                        {cert.transaction_hash
                          ? formatTransactionHash(cert.transaction_hash)
                          : `Block #${cert.block_number || 'Unknown'}`}
                      </Typography>
                    </Box>
                  </Box>
                </CardContent>
              </Card>
            ))
          )}
        </Box>

        {/* View All Button */}
        {certificates && certificates.length > 6 && (
          <Box sx={{ mt: 2, textAlign: 'center' }}>
            <Button 
              variant="outlined" 
              size="small" 
              startIcon={<TrendingUpOutlined />}
              sx={{ minWidth: 160 }}
            >
              View All {certificates.length} Certificates
            </Button>
          </Box>
        )}
      </CardContent>
    </Card>
  );
};

export default CarbonSavingsCertificate;
