import { CircularProgress, Box, Typography } from '@mui/material'

interface LoadingSpinnerProps {
  message?: string;
}

export default function LoadingSpinner({ message = 'Loading...' }: LoadingSpinnerProps) {
  return (
    <Box sx={{ 
      display: 'flex', 
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center', 
      p: 4,
      gap: 2
    }}>
      <CircularProgress />
      <Typography variant="body2" color="text.secondary">
        {message}
      </Typography>
    </Box>
  )
}
