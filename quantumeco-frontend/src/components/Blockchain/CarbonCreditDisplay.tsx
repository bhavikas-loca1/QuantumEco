// Components/CarbonCreditDisplay.tsx

import React, { useState, useEffect } from 'react';
import {
  Card,
  CardContent,
  Typography,
  Box,
  Chip,
  Button,
  CircularProgress,
} from '@mui/material';
import {
  AccountBalanceWalletOutlined,
  TrendingUpOutlined,
  Co2Outlined,
} from '@mui/icons-material';
import { getCarbonCredits, type CarbonCredit } from '../../Services/blockchain'; // Ensure CarbonCredit type is imported

// Define the shape of a single CarbonCredit item if not already in blockchain.ts
// If you have a CarbonCredit type in blockchain.ts that matches this, you can remove this interface.
// For demonstration, I'm defining it here if it's missing or different in your Service file.
/*
export interface CarbonCredit {
  credit_id: string; // Often IDs are strings (hashes) in blockchain contexts
  route_id: string;
  carbon_amount_kg: number;
  value_usd: number;
  created_at: string; // Or Date, if you parse it
  // Add other properties from your CarbonCredit type if available, e.g.,
  // transaction_hash?: string;
  // issuer?: string;
  // environmental_equivalents?: any;
}
*/

// CarbonCreditDisplayProps: Defines props accepted by the component.
// Removed the 'credits' prop as the component fetches its own data.
interface CarbonCreditDisplayProps {
  onTradeCredit?: (creditId: string) => void; // Changed to string based on common blockchain IDs
}

/**
 * CarbonCreditDisplay Component
 * Purpose: Display tradeable carbon credits generated from optimizations
 * Features: Credit values, trading capability, environmental equivalents
 */
const CarbonCreditDisplay: React.FC<CarbonCreditDisplayProps> = ({ onTradeCredit }) => {
  const [credits, setCredits] = useState<CarbonCredit[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // This component now manages its own data fetching
    loadCarbonCredits();
  }, []); // Empty dependency array means it runs once on mount

  const loadCarbonCredits = async () => {
    try {
      setLoading(true);
      // Assuming getCarbonCredits() returns an array of CarbonCredit
      const carbonCredits = await getCarbonCredits(5); // Fetches a limited number of credits
      setCredits(carbonCredits);
    } catch (error) {
      console.error('Failed to load carbon credits:', error);
      // Optionally set an error state here to display a message to the user
    } finally {
      setLoading(false);
    }
  };

  const totalValue = credits.reduce((sum, credit) => sum + credit.value_usd, 0);
  const totalCarbon = credits.reduce((sum, credit) => sum + credit.carbon_amount_kg, 0);

  if (loading) {
    return (
      <Card>
        <CardContent>
          <Box sx={{ display: 'flex', justifyContent: 'center', p: 3 }}>
            <CircularProgress />
          </Box>
        </CardContent>
      </Card>
    );
  }

  // Handle case where no credits are loaded after fetching
  if (credits.length === 0 && !loading) {
    return (
      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            💰 Tradeable Carbon Credits
          </Typography>
          <Typography variant="body1" color="text.secondary">
            No carbon credits found. Optimize a route to generate some!
          </Typography>
          {/* Optionally add a button to trigger optimization or refresh */}
          <Button variant="contained" sx={{ mt: 2 }} onClick={loadCarbonCredits}>
            Refresh Credits
          </Button>
        </CardContent>
      </Card>
    );
  }

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
              key={credit.credit_id} // Use credit.credit_id as key
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
                  // Assuming credit.credit_id can be passed to onTradeCredit
                  onClick={() => onTradeCredit?.(credit.credit_id.toString())}
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