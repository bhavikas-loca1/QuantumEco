import {  Component,  type ErrorInfo,  type ReactNode } from 'react';
import {
  Box,
  Alert,
  Button,
  Typography,
  Container,
  Card,
  CardContent,
} from '@mui/material';
import { RefreshOutlined, BugReportOutlined } from '@mui/icons-material';

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
  errorInfo?: ErrorInfo;
}

class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false
  };

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Uncaught error:', error, errorInfo);
    this.setState({
      error,
      errorInfo
    });
  }

  private handleRefresh = () => {
    window.location.reload();
  };

  private handleReset = () => {
    this.setState({ hasError: false, error: undefined, errorInfo: undefined });
  };

  public render() {
    if (this.state.hasError) {
      return (
        <Container maxWidth="md" sx={{ py: 4 }}>
          <Card>
            <CardContent>
              <Box
                sx={{
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center',
                  textAlign: 'center',
                  gap: 3,
                }}
              >
                <BugReportOutlined sx={{ fontSize: 64, color: 'error.main' }} />
                
                <Typography variant="h4" color="error.main" gutterBottom>
                  Oops! Something went wrong
                </Typography>
                
                <Alert severity="error" sx={{ width: '100%' }}>
                  <Typography variant="h6" gutterBottom>
                    Application Error
                  </Typography>
                  <Typography variant="body2">
                    {this.state.error?.message || 'An unexpected error occurred'}
                  </Typography>
                </Alert>

                <Typography variant="body1" color="text.secondary">
                  We apologize for the inconvenience. This error has been logged and our team will investigate.
                </Typography>

                <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap', justifyContent: 'center' }}>
                  <Button
                    variant="contained"
                    startIcon={<RefreshOutlined />}
                    onClick={this.handleRefresh}
                    size="large"
                  >
                    Refresh Page
                  </Button>
                  
                  <Button
                    variant="outlined"
                    onClick={this.handleReset}
                    size="large"
                  >
                    Try Again
                  </Button>
                </Box>

                {process.env.NODE_ENV === 'development' && this.state.error && (
                  <Box sx={{ mt: 3, width: '100%' }}>
                    <Typography variant="h6" gutterBottom>
                      Development Details:
                    </Typography>
                    <Box
                      sx={{
                        backgroundColor: 'grey.100',
                        p: 2,
                        borderRadius: 1,
                        fontFamily: 'monospace',
                        fontSize: '0.875rem',
                        textAlign: 'left',
                        overflow: 'auto',
                        maxHeight: 300,
                      }}
                    >
                      <pre>{this.state.error.stack}</pre>
                    </Box>
                  </Box>
                )}
              </Box>
            </CardContent>
          </Card>
        </Container>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
