import React from "react";
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Box,
  Grid,
  Card,
  CardContent,
  Container,
  CssBaseline,
} from "@mui/material";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import { Routes, Route, useNavigate } from "react-router-dom";
import GetStarted from "./friend";
import Navigate from "./Navigate";
import NavigationRoundedIcon from "@mui/icons-material/NavigationRounded";
import PersonIcon from "@mui/icons-material/Person";


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
  const navigate = useNavigate();

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />

      {/* Navbar */}
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" style={{ flexGrow: 1 }}>
            Uncrashout
          </Typography>
          <Button color="inherit">About</Button>
          <Button color="inherit">Help</Button>
          <Button color="inherit">Contact</Button>
        </Toolbar>
      </AppBar>

      {/* Routes */}
      <Routes>
        {/* Homepage */}
        <Route
          path="/"
          element={
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
              <Typography variant="h6" color="text.secondary" gutterBottom>
                Audio-guided navigation
              </Typography>

              
              <Box
                sx={{
                  display: "flex",
                  gap: 2,
                  marginTop: 2,
                  "& .MuiButton-contained:hover": {
                    backgroundColor: "#0056b3", // Darker shade of blue for the hover
                  },
                  "& .MuiButton-outlined:hover": {
                    borderColor: "#0056b3", // Highlighted border on hover
                    color: "#0056b3",
                  },
                }}
              >
                <Button
                  variant="contained"
                  color="primary"
                  startIcon={<NavigationRoundedIcon />}
                  onClick={() => navigate("/Navigate")}
                >
                  Navigate
                </Button>
                <Button
                  variant="outlined"
                  color="secondary"
                  startIcon={<PersonIcon />}
                  onClick={() => navigate("/get-started")}
                >
                  I'm a friend of a user
                </Button>
              </Box>


              {/* Feature Highlights */}
              <Grid container spacing={2} justifyContent="center" marginTop={4}>
                  <Card>
                    <CardContent>
                      <Typography variant="h6" gutterBottom>
                        Audio-guided navigation
                      </Typography>
                      <Typography variant="body2">
                        With just your voice, uncrashout can guide you across floor plans
                      </Typography>
                    </CardContent>
                  </Card>
              </Grid>
            </Container>
          }
        />

        {/* Get Started Page */}
        <Route path="/get-started" element={<GetStarted />} />

        <Route path="/navigate" element={<Navigate />} />
      </Routes>

      {/* Footer */}
      <Box mt={4} py={2} textAlign="center" bgcolor="background.default">
        <Typography variant="body2" color="text.secondary">
          © 2025 Uncrashout. All rights reserved.
        </Typography>
      </Box>
    </ThemeProvider>
  );
}

export default App;





