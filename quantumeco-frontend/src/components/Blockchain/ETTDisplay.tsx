// import React from 'react';
// import {
//   Card,
//   CardContent,
//   Typography,
//   Box,
//   Chip,
//   LinearProgress,
//   Avatar,
// } from '@mui/material';
// import {
//   NatureOutlined,
//   StarOutlined,
//   Co2Outlined,
// } from '@mui/icons-material';

// // ✅ Moved interface to shared types file (if needed) or keep here
// export interface ETTToken {
//   token_id: number;
//   route_id: string;
//   trust_score: number;
//   carbon_impact_kg: number;
//   sustainability_rating: number;
//   created_at: string;
// }

// interface ETTDisplayProps {
//   tokens: ETTToken[]; // ✅ Added prop interface
// }

// /**
//  * ETTDisplay Component
//  * Purpose: Display Environmental Trust Tokens with sustainability metrics
//  * Features: Trust scores, sustainability ratings, carbon impact visualization
//  */
// const ETTDisplay: React.FC<ETTDisplayProps> = ({ tokens }) => {
//   const getTrustScoreColor = (score: number) => {
//     if (score >= 90) return 'success';
//     if (score >= 75) return 'info';
//     if (score >= 60) return 'warning';
//     return 'error';
//   };

//   return (
//     <Card>
//       <CardContent>
//         <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
//           <NatureOutlined />
//           🪙 Environmental Trust Tokens (ETT)
//         </Typography> 
//         <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
//           Blockchain-verified sustainability scoring for transparent environmental impact
//         </Typography>

//         {tokens.length === 0 ? (
//           <Typography variant="body2" color="text.secondary" sx={{ textAlign: 'center', py: 3 }}>
//             0 Credits Available
//           </Typography>
//         ) : (
//           <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
//             {tokens.slice(0, 3).map((token) => (
//               <Card key={token.token_id} variant="outlined" sx={{ bgcolor: 'success.50' }}>
//                 <CardContent sx={{ py: 2 }}>
//                   <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
//                     <Avatar sx={{ bgcolor: 'success.main', width: 32, height: 32 }}>
//                       <StarOutlined fontSize="small" />
//                     </Avatar>
//                     <Box>
//                       <Typography variant="subtitle2" sx={{ fontWeight: 'bold' }}>
//                         ETT Token #{token.token_id}
//                       </Typography>
//                       <Typography variant="caption" color="text.secondary">
//                         Route: {token.route_id}
//                       </Typography>
//                     </Box>
//                     <Chip 
//                       label={`${token.carbon_impact_kg.toFixed(1)} kg CO₂`} 
//                       color="success" 
//                       size="small"
//                       icon={<Co2Outlined />}
//                     />
//                   </Box>

//                   {/* Trust Score */}
//                   <Box sx={{ mb: 2 }}>
//                     <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
//                       <Typography variant="body2">Trust Score</Typography>
//                       <Typography variant="body2" sx={{ fontWeight: 'bold' }}>
//                         {token.trust_score}%
//                       </Typography>
//                     </Box>
//                     <LinearProgress 
//                       variant="determinate" 
//                       value={token.trust_score} 
//                       color={getTrustScoreColor(token.trust_score)}
//                       sx={{ height: 6, borderRadius: 3 }}
//                     />
//                   </Box>

//                   {/* Sustainability Rating */}
//                   <Box>
//                     <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
//                       <Typography variant="body2">Sustainability Rating</Typography>
//                       <Typography variant="body2" sx={{ fontWeight: 'bold' }}>
//                         {token.sustainability_rating}%
//                       </Typography>
//                     </Box>
//                     <LinearProgress 
//                       variant="determinate" 
//                       value={token.sustainability_rating} 
//                       color="success"
//                       sx={{ height: 6, borderRadius: 3 }}
//                     />
//                   </Box>
//                 </CardContent>
//               </Card>
//             ))}
//           </Box>
//         )}
//       </CardContent>
//     </Card>
//   );
// };

// export default ETTDisplay;
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

// ✅ Interface definition
export interface ETTToken {
  token_id: number;
  route_id: string;
  trust_score: number;
  carbon_impact_kg: number;
  sustainability_rating: number;
  created_at: string;
}

interface ETTDisplayProps {
  tokens: ETTToken[];
}

/**
 * ETTDisplay Component - FIXED to handle undefined tokens
 * Purpose: Display Environmental Trust Tokens with sustainability metrics
 * Features: Trust scores, sustainability ratings, carbon impact visualization
 */
const ETTDisplay: React.FC<ETTDisplayProps> = ({ tokens }) => {
  
  // ✅ FIXED: Safe number formatting to prevent toFixed errors
  const safeToFixed = (value: any, decimals: number = 1): string => {
    if (value === null || value === undefined || isNaN(value)) {
      return '0';
    }
    return Number(value).toFixed(decimals);
  };

  // ✅ FIXED: Validate and filter tokens to remove undefined/null values
  const validTokens = React.useMemo(() => {
    if (!Array.isArray(tokens)) {
      console.warn('ETTDisplay: tokens is not an array:', tokens);
      return [];
    }
    
    return tokens.filter((token) => {
      // Filter out null, undefined, or invalid tokens
      if (!token || typeof token !== 'object') {
        console.warn('ETTDisplay: Invalid token found:', token);
        return false;
      }
      
      // Ensure required properties exist
      if (!token.token_id && token.token_id !== 0) {
        console.warn('ETTDisplay: Token missing token_id:', token);
        return false;
      }
      
      return true;
    }).map((token) => {
      // ✅ FIXED: Normalize token structure with safe defaults
      return {
        token_id: token.token_id || Date.now(),
        route_id: token.route_id || 'unknown',
        trust_score: Number(token.trust_score) || 0,
        carbon_impact_kg: Number(token.carbon_impact_kg) || 0,
        sustainability_rating: Number(token.sustainability_rating) || 0,
        created_at: token.created_at || new Date().toISOString(),
      };
    });
  }, [tokens]);

  const getTrustScoreColor = (score: number) => {
    if (score >= 90) return 'success';
    if (score >= 75) return 'info';
    if (score >= 60) return 'warning';
    return 'error';
  };

  // ✅ FIXED: Better loading/empty state handling
  if (!tokens) {
    return (
      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <NatureOutlined />
            🪙 Environmental Trust Tokens (ETT)
          </Typography> 
          <Typography variant="body2" color="text.secondary" sx={{ textAlign: 'center', py: 3 }}>
            Loading tokens...
          </Typography>
        </CardContent>
      </Card>
    );
  }

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

        {validTokens.length === 0 ? (
          <Typography variant="body2" color="text.secondary" sx={{ textAlign: 'center', py: 3 }}>
            {tokens.length === 0 ? '0 Credits Available' : 'No valid tokens found'}
          </Typography>
        ) : (
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            {validTokens.slice(0, 3).map((token, index) => (
              <Card 
                key={`ett-token-${token.token_id}-${index}`} // ✅ FIXED: Safer key generation
                variant="outlined" 
                sx={{ bgcolor: 'success.50' }}
              >
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
                      label={`${safeToFixed(token.carbon_impact_kg)} kg CO₂`} 
                      color="success" 
                      size="small"
                      icon={<Co2Outlined />}
                    />
                  </Box>

                  {/* Trust Score with safe value handling */}
                  <Box sx={{ mb: 2 }}>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                      <Typography variant="body2">Trust Score</Typography>
                      <Typography variant="body2" sx={{ fontWeight: 'bold' }}>
                        {Math.round(token.trust_score || 0)}%
                      </Typography>
                    </Box>
                    <LinearProgress 
                      variant="determinate" 
                      value={Math.min(100, Math.max(0, token.trust_score || 0))} // ✅ FIXED: Clamp value between 0-100
                      color={getTrustScoreColor(token.trust_score || 0)}
                      sx={{ height: 6, borderRadius: 3 }}
                    />
                  </Box>

                  {/* Sustainability Rating with safe value handling */}
                  <Box>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                      <Typography variant="body2">Sustainability Rating</Typography>
                      <Typography variant="body2" sx={{ fontWeight: 'bold' }}>
                        {Math.round(token.sustainability_rating || 0)}%
                      </Typography>
                    </Box>
                    <LinearProgress 
                      variant="determinate" 
                      value={Math.min(100, Math.max(0, token.sustainability_rating || 0))} // ✅ FIXED: Clamp value between 0-100
                      color="success"
                      sx={{ height: 6, borderRadius: 3 }}
                    />
                  </Box>
                </CardContent>
              </Card>
            ))}
          </Box>
        )}

        {/* ✅ FIXED: Debug info for development */}
        {process.env.NODE_ENV === 'development' && (
          <Box sx={{ mt: 2, p: 1, bgcolor: 'grey.100', borderRadius: 1 }}>
            <Typography variant="caption" color="text.secondary">
              Debug: {tokens?.length || 0} total tokens, {validTokens.length} valid tokens
            </Typography>
          </Box>
        )}
      </CardContent>
    </Card>
  );
};

export default ETTDisplay;
