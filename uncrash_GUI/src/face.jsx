import React, { useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { io } from "socket.io-client";

// Connect to the WebSocket server
const socket = io("http://localhost:4000");

const SavePictureApp = () => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [image, setImage] = useState(null);
  const [imageName, setImageName] = useState("");
  const navigate = useNavigate();
  

  // Start the camera when the component mounts
  React.useEffect(() => {
    const startCamera = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
      } catch (error) {
        console.error("Error accessing the camera: ", error);
      }
    };

    startCamera();
  }, []);

  // Take a picture on button click
  const takePicture = () => {
    if (videoRef.current && canvasRef.current) {
      const context = canvasRef.current.getContext("2d");
      canvasRef.current.width = videoRef.current.videoWidth;
      canvasRef.current.height = videoRef.current.videoHeight;
      context.drawImage(videoRef.current, 0, 0);
      const dataUrl = canvasRef.current.toDataURL("image/png");
      setImage(dataUrl); // Save the image data to state

      // Stop the video stream to "pause" the camera feed
      const stream = videoRef.current.srcObject;
      if (stream) {
        const tracks = stream.getTracks();
        tracks.forEach((track) => track.stop());
        videoRef.current.srcObject = null; // Clear the video source
      }
    }
  };

  // Retake a picture: Restart the camera
  const retakePicture = async () => {
    setImage(null); // Clear the captured image
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }
    } catch (error) {
      console.error("Error restarting the camera: ", error);
    }
  };

  // Save the image with the user-provided name
  const savePicture = () => {
    if (!imageName.trim()) {
      alert("Please enter a name for the picture.");
      return;
    }
  
    // Send the image and name to the backend via WebSocket
    socket.emit("upload_image", { image, name: imageName });
  
    // Handle response from the server
    socket.on("upload_response", (response) => {
      if (response.status === "success") {
        alert(`Picture saved and processed as ${imageName}.png`);
        setImage(null); // Clear the image preview
        setImageName(""); // Clear the input field
      } else {
        alert(`Error: ${response.message}`);
      }
    });
  };
  

  return (
    <div style={{ textAlign: "center", padding: "20px" }}>
      <h1>Take and Save a Picture</h1>

      {/* Show either the camera feed or the captured image */}
      {!image ? (
        <div>
          {/* Live Camera Feed */}
          <video
            ref={videoRef}
            autoPlay
            playsInline
            style={{ width: "100%", maxWidth: "500px", marginBottom: "10px" }}
          />
          {/* Centered Button */}
          <div
            style={{
              display: "flex",
              justifyContent: "center",
              marginTop: "10px",
            }}
          >
            <button
              onClick={takePicture}
              style={{
                padding: "10px 20px",
                fontSize: "16px",
                cursor: "pointer",
              }}
            >
              Take Picture
            </button>
          </div>
        </div>
      ) : (
        <div>
          {/* Show Captured Image */}
          <h2>Captured Image:</h2>
          <img
            src={image}
            alt="Captured"
            style={{ width: "100%", maxWidth: "500px", marginTop: "10px", border: "1px solid #ccc" }}
          />
          {/* Retake/Save Options */}
          <div style={{ marginTop: "10px" }}>
            <button
              onClick={retakePicture}
              style={{
                padding: "10px 20px",
                fontSize: "16px",
                cursor: "pointer",
                marginRight: "10px",
              }}
            >
              Retake
            </button>
            <input
              type="text"
              placeholder="Enter picture name"
              value={imageName}
              onChange={(e) => setImageName(e.target.value)}
              style={{ padding: "8px", fontSize: "16px", marginRight: "10px" }}
            />
            <button
              onClick={savePicture}
              style={{ padding: "8px 20px", fontSize: "16px", cursor: "pointer" }}
            >
              Save Picture
            </button>
          </div>
        </div>
      )}

      {/* Return to Home Button */}
      <div
        style={{
          display: "flex",
          justifyContent: "center",
          marginTop: "20px",
        }}
      >
        <button
          onClick={() => navigate("/")}
          style={{
            padding: "10px 20px",
            fontSize: "16px",
            cursor: "pointer",
            backgroundColor: "#007BFF",
            color: "white",
            border: "none",
            borderRadius: "5px",
          }}
        >
          Return to Home
        </button>
      </div>

      {/* Hidden Canvas for Capturing Picture */}
      <canvas ref={canvasRef} style={{ display: "none" }} />
    </div>
  );
};

export default SavePictureApp;

