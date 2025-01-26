import React, { useRef, useEffect, useState } from "react";
import { Typography, Container, Box, Button } from "@mui/material";
import { io } from "socket.io-client";

function Navigate() {
  const videoRef = useRef(null);
  const [error, setError] = useState("");
  const [socket, setSocket] = useState(null);

  // Initialize WebSocket connection
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
          // Clear previous frame
          context.clearRect(0, 0, videoRef.current.width, videoRef.current.height);
          
          // Calculate scaling to maintain aspect ratio
          const imageAspectRatio = img.width / img.height;
          const canvasAspectRatio = videoRef.current.width / videoRef.current.height;
          
          let drawWidth, drawHeight, offsetX = 0, offsetY = 0;
          
          if (imageAspectRatio > canvasAspectRatio) {
            // Image is wider relative to canvas
            drawWidth = videoRef.current.width;
            drawHeight = drawWidth / imageAspectRatio;
            offsetY = (videoRef.current.height - drawHeight) / 2;
          } else {
            // Image is taller relative to canvas
            drawHeight = videoRef.current.height;
            drawWidth = drawHeight * imageAspectRatio;
            offsetX = (videoRef.current.width - drawWidth) / 2;
          }
          
          // Draw the image centered and scaled
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
        //   // sx={{
        //   //   position: "relative",
        //   //   width: "100%",
        //   //   maxWidth: 400,
        //   //   aspectRatio: "3/4",
        //   //   border: "2px solid #007BFF",
        //   //   borderRadius: 4,
        //   //   overflow: "hidden",
        //   // }}
          
        >
          <canvas
            ref={videoRef}
            width={800}
            height={500}
            style={{
              width: "100%",
              height: "100%",
              // objectFit: "contain", // Changed from 'cover' to 'contain'
            }}
          />
          
        </Box>
      )}

      <Box sx={{ marginTop: 1 }}>
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