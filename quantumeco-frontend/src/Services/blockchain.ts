// Frontend blockchain service integration
import { api } from './api';

export interface BlockchainCertificate {
  certificate_id: string;
  route_id: string;
  vehicle_id: string;
  carbon_saved_kg: number;
  cost_saved_usd: number;
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
}): Promise<BlockchainCertificate> => {
  const response = await api.post('/api/blockchain/certificate', certData);
  return response.data;
};

// Live ETT creation for demo
export const createETTToken = async (ettData: {
  route_id: string;
  trust_score: number;
  carbon_impact: number;
  sustainability_rating: number;
}): Promise<EnvironmentalTrustToken> => {
  const response = await api.post('/api/blockchain/ett/create', ettData);
  return response.data;
};

// Create carbon credit
export const createCarbonCredit = async (creditData: {
  route_id: string;
  carbon_amount_kg: number;
  value_usd: number;
  vintage_year: number;
}): Promise<CarbonCredit> => {
  const response = await api.post('/api/blockchain/carbon-credit', creditData);
  return response.data;
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
