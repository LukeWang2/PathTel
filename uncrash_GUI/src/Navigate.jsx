import React, { useRef, useEffect, useState } from "react";
import { Typography, Container, Box, Button, Grid } from "@mui/material";
import { io } from "socket.io-client";
import InteractiveFloorPlan from "./components/InteractiveFloorPlan";

function Navigate() {
  const videoRef = useRef(null);
  const [error, setError] = useState("");
  const [socket, setSocket] = useState(null);

  // Previous WebSocket and video frame logic remains the same
  useEffect(() => {
    const newSocket = io("http://localhost:4000");
    setSocket(newSocket);

    newSocket.on("connect", () => {
      console.log("Connected to server");
      newSocket.emit("start_stream");
    });

    newSocket.on("video_frame", (data) => {
      if (videoRef.current) {
        const img = document.createElement("img");
        img.src = `data:image/jpeg;base64,${data.frame}`;
        const context = videoRef.current.getContext("2d");
        
        img.onload = () => {
          context.clearRect(0, 0, videoRef.current.width, videoRef.current.height);
          
          const imageAspectRatio = img.width / img.height;
          const canvasAspectRatio = videoRef.current.width / videoRef.current.height;
          
          let drawWidth, drawHeight, offsetX = 0, offsetY = 0;
          
          if (imageAspectRatio > canvasAspectRatio) {
            drawWidth = videoRef.current.width;
            drawHeight = drawWidth / imageAspectRatio;
            offsetY = (videoRef.current.height - drawHeight) / 2;
          } else {
            drawHeight = videoRef.current.height;
            drawWidth = drawHeight * imageAspectRatio;
            offsetX = (videoRef.current.width - drawWidth) / 2;
          }
          
          context.drawImage(
            img, 
            offsetX, 
            offsetY, 
            drawWidth, 
            drawHeight
          );
        };
      }
    });

    return () => {
      newSocket.close();
    };
  }, []);

  // Dictate Instructions (Placeholder Function)
  const dictateInstructions = () => {
    const utterance = new SpeechSynthesisUtterance(
      "Stand still."
    );
    window.speechSynthesis.speak(utterance);
  };

  return (
      <Container maxWidth="xl" sx={{ py: 4 }}>
        <Typography variant="h4" gutterBottom>
          Audio-Guided Navigation
        </Typography>
    
        {error ? (
          <Typography color="error">{error}</Typography>
        ) : (
          <Grid container spacing={3} sx={{ mb: 3 }}>
            <Grid item xs={12} md={6}>
              <Box
                sx={{
                  width: '100%',
                  height: '600px',
                  border: '1px solid #ccc',
                  borderRadius: 2,
                  overflow: 'hidden',
                }}
              >
                <canvas
                  ref={videoRef}
                  width={800}
                  height={600}
                  style={{
                    width: '100%',
                    height: '100%',
                    objectFit: 'contain',
                  }}
                />
              </Box>
            </Grid>
            <Grid item xs={12} md={6}>
              <Box
                sx={{
                  width: '100%',
                  height: '600px',
                  border: '1px solid #ccc',
                  borderRadius: 2,
                  overflow: 'hidden',
                }}
              >
                <InteractiveFloorPlan />
              </Box>
            </Grid>
          </Grid>
        )}
    
        <Box sx={{ textAlign: 'center' }}>
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