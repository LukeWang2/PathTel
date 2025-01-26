import React from "react";
import { Typography, Container, Box, Button } from "@mui/material";
import { useNavigate } from "react-router-dom";
import SavePictureApp from "./face";
function GetStarted() {
  const navigate = useNavigate();

  return (
    <Container
      sx={{
        height: "calc(100vh - 64px)", // Full viewport height minus navbar height
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        textAlign: "center",
      }}
    >
      <Typography variant="h4" gutterBottom>
        Friends and Family
      </Typography>
      <Typography>
        Welcome to the Friend of a User page. Here you'll find instructions to
        begin and integrate your face into the app. With this feature, your
        friends and loved one using the app will receive audio queues that you
        are in their visual perimeter when our software recognizes your face.
      </Typography>

      <Box sx={{ display: "flex", justifyContent: "center", marginTop: 2 }}>
      <Button
        variant="outlined"
        color="primary"
        onClick={() => navigate("/face")}
      >
        Scan My Face
      </Button>
      </Box>
      
      <Box sx={{ display: "flex", justifyContent: "center", marginTop: 2 }}>
        <Button variant="outlined" color="primary" onClick={() => navigate("/")}>
          Return to Home
        </Button>
      </Box>

    
    </Container>
  );
}

export default GetStarted;

