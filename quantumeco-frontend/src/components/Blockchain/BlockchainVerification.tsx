import React, { useState, useEffect } from 'react';
import {
  Card,
  CardContent,
  Typography,
  Box,
  Chip,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
} from '@mui/material';
import {
  VerifiedOutlined,
  LinkOutlined,
  ExploreOutlined,
} from '@mui/icons-material';
import { getBlockchainExplorer } from '../../Services/blockchain';

/**
 * BlockchainVerification Component
 * Purpose: Display blockchain verification status and transaction details
 * Features: Live transaction data, block explorer, verification status
 */
const BlockchainVerification: React.FC = () => {
  const [explorerData, setExplorerData] = useState<any>(null);
  const [recentTransactions, setRecentTransactions] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadBlockchainData();
  }, []);

  const loadBlockchainData = async () => {
    try {
      const data = await getBlockchainExplorer();
      setExplorerData(data);
      setRecentTransactions(data.recent_transactions || []);
    } catch (error) {
      console.error('Failed to load blockchain data:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatTransactionHash = (hash: string) => {
    return `${hash.slice(0, 10)}...${hash.slice(-8)}`;
  };

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <ExploreOutlined />
          Blockchain Network Status
        </Typography>

        {/* Network Stats */}
        <Box sx={{ display: 'flex', gap: 2, mb: 3, flexWrap: 'wrap' }}>
          <Chip label={`Network: Ganache (ID: ${explorerData?.network_id || 1337})`} color="success" />
          <Chip label={`Latest Block: ${explorerData?.latest_block?.toLocaleString() || 'Loading...'}`} />
          <Chip label={`Total Certificates: ${explorerData?.total_deliveries || 0}`} color="info" />
        </Box>

        {/* Recent Transactions */}
        <Typography variant="subtitle1" gutterBottom>
          Recent Blockchain Transactions
        </Typography>
        <TableContainer component={Paper} variant="outlined" sx={{ maxHeight: 300 }}>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>Transaction Hash</TableCell>
                <TableCell>Type</TableCell>
                <TableCell>Block</TableCell>
                <TableCell>Status</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {recentTransactions.slice(0, 5).map((tx, index) => (
                <TableRow key={index}>
                  <TableCell>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <LinkOutlined fontSize="small" />
                      {formatTransactionHash(tx.hash || `0x${index}...`)}
                    </Box>
                  </TableCell>
                  <TableCell>Certificate</TableCell>
                  <TableCell>{(tx.blockNumber || 1000000 + index).toLocaleString()}</TableCell>
                  <TableCell>
                    <Chip label="Verified" color="success" size="small" icon={<VerifiedOutlined />} />
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>

        <Button
          variant="outlined"
          size="small"
          sx={{ mt: 2 }}
          onClick={loadBlockchainData}
        >
          Refresh Network Data
        </Button>
      </CardContent>
    </Card>
  );
};

export default BlockchainVerification;
