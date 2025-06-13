import { createTheme } from '@mui/material/styles';

// Simple theme without complex overrides
export const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#041f41',
    },
    secondary: {
      main: '#FFC220',
    },
    background: {
      default: '#FFF9E6',
      paper: '#f4f7f4', // ✅ CHANGED: From '#FFFFFF' to light sage green
    },
    text: {
      primary: '#041f41',
    },
  },
  typography: {
    fontFamily: '"Myriad Pro", "Whitney", "Avenir Next", "Helvetica Neue", sans-serif',
    // ✅ ONLY h1 uses Cinzel, everything else normal
    h1: {
      fontFamily: '"Cinzel", serif',
      fontWeight: 100,
      color: '#000000',
    },
  },
  components: {
    MuiCssBaseline: {
      styleOverrides: {
        body: {
          backgroundColor: '#FFF9E6 !important',
          margin: 0,
          padding: 0,
        },
        html: {
          backgroundColor: '#FFF9E6 !important',
        },
        '#root': {
          backgroundColor: '#FFF9E6 !important',
          minHeight: '100vh',
        },
      },
    },
    // ✅ ADDED: Ensure all Cards use the sage green background
    MuiCard: {
      styleOverrides: {
        root: {
          backgroundColor: '#f4f7f4', // ✅ Force sage green for all cards
        },
      },
    },
  },
});

export default theme;
