/*import React from "react";
import { Box, Button, Typography } from "@mui/material";

import { createTheme, ThemeProvider } from "@mui/material/styles";

const theme = createTheme({
  palette: {
    primary: {
      main: "#007BFF", // Replace with your primary color
    },
    secondary: {
      main: "#6C757D", // Replace with your secondary color
    },
    background: {
      default: "#F8F9FA", // Replace with your background color
    },
    error: {
      main: "#DC3545", // Replace with your error color
    },
  },
});

function App() {
  return (
    <>
      <Box
        sx={{
          height: "100vh", // Make the box take the full viewport height
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        <Typography variant="h4" gutterBottom align="center">
          Welcome to Uncrashout
        </Typography>

        <Box sx={{ display: "flex", gap: 2 }}>
          <Button variant="contained" color="primary">
            Login
          </Button>
          <Button variant="outlined" color="secondary">
            Continue as Guest
          </Button>
        </Box>
      </Box>
    </>
  );
}

export default App;*/

import React from "react";
import ReactDOM from "react-dom/client";
import { Button, Typography, Box, Container, CssBaseline } from "@mui/material";
import { ThemeProvider, createTheme } from "@mui/material/styles";

const theme = createTheme({
  palette: {
    primary: {
      main: "#007BFF", // Bright Blue
    },
    secondary: {
      main: "#6C757D", // Gray
    },
    background: {
      default: "#F8F9FA", // Light Gray
    },
    error: {
      main: "#DC3545", // Red
    },
    text: {
      primary: "#333333", // Dark Text
      secondary: "#555555", // Lighter Text
    },
  },
  typography: {
    fontFamily: "Arial, sans-serif",
    h4: {
      fontWeight: 700,
    },
    button: {
      textTransform: "none", // Disable uppercase for buttons
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container
        maxWidth="sm"
        sx={{
          height: "100vh",
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
          textAlign: "center",
          backgroundColor: "background.default",
        }}
      >
        <Typography variant="h4" gutterBottom color="text.primary">
          Welcome to Uncrashout
        </Typography>
        <Box sx={{ display: "flex", gap: 2 }}>
          <Button variant="contained" color="primary">
            Login
          </Button>
          <Button variant="outlined" color="secondary">
            Continue as Guest
          </Button>
        </Box>
      </Container>
    </ThemeProvider>
  );
}

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<App />);
export default App;





