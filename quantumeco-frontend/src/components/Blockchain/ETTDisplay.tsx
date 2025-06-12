import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  Box,
  Chip,
  LinearProgress,
  Avatar,
} from '@mui/material';
import {
  NatureOutlined,
  StarOutlined,
  Co2Outlined,
} from '@mui/icons-material';

// ✅ Moved interface to shared types file (if needed) or keep here
export interface ETTToken {
  token_id: number;
  route_id: string;
  trust_score: number;
  carbon_impact_kg: number;
  sustainability_rating: number;
  created_at: string;
}

interface ETTDisplayProps {
  tokens: ETTToken[]; // ✅ Added prop interface
}

/**
 * ETTDisplay Component
 * Purpose: Display Environmental Trust Tokens with sustainability metrics
 * Features: Trust scores, sustainability ratings, carbon impact visualization
 */
const ETTDisplay: React.FC<ETTDisplayProps> = ({ tokens }) => {
  const getTrustScoreColor = (score: number) => {
    if (score >= 90) return 'success';
    if (score >= 75) return 'info';
    if (score >= 60) return 'warning';
    return 'error';
  };

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <NatureOutlined />
          🪙 Environmental Trust Tokens (ETT)
        </Typography> 
        <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
          Blockchain-verified sustainability scoring for transparent environmental impact
        </Typography>

        {tokens.length === 0 ? (
          <Typography variant="body2" color="text.secondary" sx={{ textAlign: 'center', py: 3 }}>
            0 Credits Available
          </Typography>
        ) : (
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            {tokens.slice(0, 3).map((token) => (
              <Card key={token.token_id} variant="outlined" sx={{ bgcolor: 'success.50' }}>
                <CardContent sx={{ py: 2 }}>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
                    <Avatar sx={{ bgcolor: 'success.main', width: 32, height: 32 }}>
                      <StarOutlined fontSize="small" />
                    </Avatar>
                    <Box>
                      <Typography variant="subtitle2" sx={{ fontWeight: 'bold' }}>
                        ETT Token #{token.token_id}
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        Route: {token.route_id}
                      </Typography>
                    </Box>
                    <Chip 
                      label={`${token.carbon_impact_kg.toFixed(1)} kg CO₂`} 
                      color="success" 
                      size="small"
                      icon={<Co2Outlined />}
                    />
                  </Box>

                  {/* Trust Score */}
                  <Box sx={{ mb: 2 }}>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                      <Typography variant="body2">Trust Score</Typography>
                      <Typography variant="body2" sx={{ fontWeight: 'bold' }}>
                        {token.trust_score}%
                      </Typography>
                    </Box>
                    <LinearProgress 
                      variant="determinate" 
                      value={token.trust_score} 
                      color={getTrustScoreColor(token.trust_score)}
                      sx={{ height: 6, borderRadius: 3 }}
                    />
                  </Box>

                  {/* Sustainability Rating */}
                  <Box>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                      <Typography variant="body2">Sustainability Rating</Typography>
                      <Typography variant="body2" sx={{ fontWeight: 'bold' }}>
                        {token.sustainability_rating}%
                      </Typography>
                    </Box>
                    <LinearProgress 
                      variant="determinate" 
                      value={token.sustainability_rating} 
                      color="success"
                      sx={{ height: 6, borderRadius: 3 }}
                    />
                  </Box>
                </CardContent>
              </Card>
            ))}
          </Box>
        )}
      </CardContent>
    </Card>
  );
};

export default ETTDisplay;
