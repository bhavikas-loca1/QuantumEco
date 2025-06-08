import { Box, List, ListItem, ListItemText, Typography } from '@mui/material'
import { OptimizationResult } from '../../services/types'

export default function RecentActivity({ optimizations }: { optimizations: OptimizationResult[] }) {
  return (
    <Box sx={{ p: 2 }}>
      <Typography variant="h6" gutterBottom>Recent Optimizations</Typography>
      <List>
        {optimizations.map((optimization) => (
          <ListItem key={optimization.optimization_id} divider>
            <ListItemText
              primary={`Optimization #${optimization.optimization_id.slice(0, 6)}`}
              secondary={
                `Saved $${optimization.total_savings.cost.toFixed(2)} • 
                ${optimization.total_savings.carbon.toFixed(2)}kg CO₂`
              }
            />
          </ListItem>
        ))}
      </List>
    </Box>
  )
}
