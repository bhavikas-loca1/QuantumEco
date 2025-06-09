import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  Box,
  Chip,
  Button,
} from '@mui/material';
import {
  AccountBalanceWalletOutlined,
  TrendingUpOutlined,
  Co2Outlined,
} from '@mui/icons-material';

interface CarbonCreditDisplayProps {
  credits: Array<{
    credit_id: number;
    route_id: string;
    carbon_amount_kg: number;
    value_usd: number;
    created_at: string;
  }>;
  onTradeCredit?: (creditId: number) => void;
}

/**
 * CarbonCreditDisplay Component
 * Purpose: Display tradeable carbon credits generated from optimizations
 * Features: Credit values, trading capability, environmental equivalents
 */
const CarbonCreditDisplay: React.FC<CarbonCreditDisplayProps> = ({ 
  credits, 
  onTradeCredit 
}) => {
  const totalValue = credits.reduce((sum, credit) => sum + credit.value_usd, 0);
  const totalCarbon = credits.reduce((sum, credit) => sum + credit.carbon_amount_kg, 0);

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <AccountBalanceWalletOutlined />
          💰 Tradeable Carbon Credits
        </Typography>

        {/* Summary */}
        <Box sx={{ display: 'flex', gap: 2, mb: 3, flexWrap: 'wrap' }}>
          <Chip 
            label={`Total Value: $${totalValue.toFixed(2)}`} 
            color="success" 
            icon={<TrendingUpOutlined />}
          />
          <Chip 
            label={`Total Carbon: ${totalCarbon.toFixed(1)} kg CO₂`} 
            color="info" 
            icon={<Co2Outlined />}
          />
          <Chip 
            label={`${credits.length} Credits Available`} 
            variant="outlined"
          />
        </Box>

        {/* Recent Credits */}
        <Typography variant="subtitle2" gutterBottom>
          Recent Carbon Credits Generated
        </Typography>
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
          {credits.slice(0, 3).map((credit) => (
            <Box 
              key={credit.credit_id}
              sx={{ 
                display: 'flex', 
                justifyContent: 'space-between', 
                alignItems: 'center',
                p: 1,
                border: '1px solid',
                borderColor: 'divider',
                borderRadius: 1
              }}
            >
              <Box>
                <Typography variant="body2" sx={{ fontWeight: 'bold' }}>
                  Credit #{credit.credit_id}
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  {credit.carbon_amount_kg.toFixed(1)} kg CO₂ • Route: {credit.route_id}
                </Typography>
              </Box>
              <Box sx={{ textAlign: 'right' }}>
                <Typography variant="body2" color="success.main" sx={{ fontWeight: 'bold' }}>
                  ${credit.value_usd.toFixed(2)}
                </Typography>
                <Button 
                  size="small" 
                  variant="outlined"
                  onClick={() => onTradeCredit?.(credit.credit_id)}
                >
                  Trade
                </Button>
              </Box>
            </Box>
          ))}
        </Box>
      </CardContent>
    </Card>
  );
};

export default CarbonCreditDisplay;
