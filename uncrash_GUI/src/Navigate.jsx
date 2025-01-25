import React, { useRef, useEffect, useState } from "react";
import { Typography, Container, Box, Button } from "@mui/material";

function Navigate() {
  const videoRef = useRef(null);
  const [error, setError] = useState("");

  // Start the video stream
  useEffect(() => {
    async function startVideo() {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({
          video: { facingMode: "environment" }, // Use the rear camera
          audio: false,
        });
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
      } catch (err) {
        setError("Unable to access the camera. Please allow camera access.");
        console.error(err);
      }
    }
    startVideo();
  }, []);

  // Dictate Instructions (Placeholder Function)
  const dictateInstructions = () => {
    const utterance = new SpeechSynthesisUtterance(
      "Stand still."
    );
    window.speechSynthesis.speak(utterance);
  };

  return (
    <Container
      sx={{
        height: "calc(100vh - 64px)",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        textAlign: "center",
      }}
    >
      <Typography variant="h4" gutterBottom>
        Audio-Guided Navigation
      </Typography>

      {error ? (
        <Typography color="error">{error}</Typography>
      ) : (
        <Box
          sx={{
            position: "relative",
            width: "100%",
            maxWidth: 400,
            aspectRatio: "3/4",
            border: "2px solid #007BFF",
            borderRadius: 4,
            overflow: "hidden",
          }}
        >
          <video
            ref={videoRef}
            autoPlay
            playsInline
            muted
            style={{
              width: "100%",
              height: "100%",
              objectFit: "cover",
            }}
          />
        </Box>
      )}

      <Box sx={{ marginTop: 2 }}>
        <Button
          variant="contained"
          color="primary"
          onClick={dictateInstructions}
        >
          Start Instructions
        </Button>
      </Box>
    </Container>
  );
}

export default Navigate;

