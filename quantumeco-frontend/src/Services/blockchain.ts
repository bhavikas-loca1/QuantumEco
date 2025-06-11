// Services/blockchain.ts - Updated with better error handling

import { api } from './api';

export interface BlockchainCertificate {
  certificate_id: string;
  route_id: string;
  vehicle_id: string;
  carbon_saved: number;
  cost_saved: number;
  optimization_score: number;
  verification_hash: string;
  transaction_hash: string;
  block_number: number;
  verified: boolean;
  created_at: string;
}

export interface EnvironmentalTrustToken {
  token_id: number;
  route_id: string;
  trust_score: number;
  carbon_impact_kg: number;
  sustainability_rating: number;
  transaction_hash: string;
  block_number: number;
  created_at: string;
}

export interface CarbonCredit {
  credit_id: number;
  route_id: string;
  carbon_amount_kg: number;
  value_usd: number;
  transaction_hash: string;
  block_number: number;
  created_at: string;
}

// Live certificate creation for demo
export const createLiveCertificate = async (certData: {
  route_id: string;
  vehicle_id: string;
  carbon_saved: number;
  cost_saved: number;
  distance_km: number;
  optimization_score: number;
  delivery_count?: number;
  time_saved_minutes?: number;
  metadata?: any;
  issuer?: string;
}): Promise<BlockchainCertificate> => {
  try {
    const response = await api.post('/api/blockchain/certificate', {
      route_id: certData.route_id,
      vehicle_id: certData.vehicle_id,
      carbon_saved: certData.carbon_saved,
      cost_saved: certData.cost_saved,
      distance_km: certData.distance_km,
      optimization_score: certData.optimization_score,
      delivery_count: certData.delivery_count || 1,
      time_saved_minutes: certData.time_saved_minutes || 0,
      metadata: certData.metadata || {},
      issuer: certData.issuer || 'QuantumEco Intelligence',
    });
    return response.data;
  } catch (error) {
    console.error('Certificate creation failed:', error);
    throw error;
  }
};

// Live ETT creation for demo
export const createETTToken = async (ettData: {
  route_id: string;
  trust_score: number;
  carbon_impact: number;
  sustainability_rating: number;
}): Promise<EnvironmentalTrustToken> => {
  try {
    const response = await api.post('/api/blockchain/ett/create', ettData);
    return response.data;
  } catch (error) {
    console.error('ETT creation failed:', error);
    throw error;
  }
};

// Create carbon credit
export const createCarbonCredit = async (creditData: {
  route_id: string;
  carbon_amount_kg: number;
  value_usd: number;
  vintage_year: number;
}): Promise<CarbonCredit> => {
  try {
    const response = await api.post('/api/blockchain/carbon-credit', creditData);
    return response.data;
  } catch (error) {
    console.error('Carbon credit creation failed:', error);
    throw error;
  }
};

// Get ETT tokens
export const getETTTokens = async (limit: number = 10): Promise<EnvironmentalTrustToken[]> => {
  try {
    const response = await api.get(`/api/blockchain/ett/tokens?limit=${limit}`);
    return response.data.tokens || [];
  } catch (error) {
    console.error('Failed to get ETT tokens:', error);
    return [];
  }
};

// Get carbon credits
export const getCarbonCredits = async (limit: number = 10): Promise<CarbonCredit[]> => {
  try {
    const response = await api.get(`/api/blockchain/carbon-credits?limit=${limit}`);
    return response.data.credits || [];
  } catch (error) {
    console.error('Failed to get carbon credits:', error);
    return [];
  }
};

// Verify certificate
export const verifyCertificate = async (certificateId: string) => {
  const response = await api.post('/api/blockchain/verify', { certificate_id: certificateId });
  return response.data;
};

// Get transaction details
export const getTransactionDetails = async (txHash: string) => {
  const response = await api.get(`/api/blockchain/transaction/${txHash}`);
  return response.data;
};

// Get blockchain explorer data
export const getBlockchainExplorer = async () => {
  const response = await api.get('/api/blockchain/explorer');
  return response.data;
};
