import { useState } from 'react'
import { Button, Grid, Paper, Typography } from '@mui/material'
import MapView from './MapView'
import ComparisonTable from './ComparisonTable'

export default function RouteComparison() {
  const [showComparison, setShowComparison] = useState(false)

  return (
    <Paper sx={{ p: 3 }}>
      <Typography variant="h6" gutterBottom>Route Comparison</Typography>
      
      <Button 
        variant="contained" 
        onClick={() => setShowComparison(!showComparison)}
      >
        {showComparison ? 'Hide' : 'Show'} Comparison
      </Button>

      {showComparison && (
        <Grid container spacing={3} sx={{ mt: 2 }}>
          <Grid item xs={12} md={6}>
            <MapView />
          </Grid>
          <Grid item xs={12} md={6}>
            <ComparisonTable />
          </Grid>
        </Grid>
      )}
    </Paper>
  )
}
