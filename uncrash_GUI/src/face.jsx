import React, { useRef, useState } from "react";

const SavePictureApp = () => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [image, setImage] = useState(null);
  const [imageName, setImageName] = useState("");

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
    }
  };

  // Save the image with the user-provided name
  const savePicture = () => {
    if (!imageName.trim()) {
      alert("Please enter a name for the picture.");
      return;
    }
    // Create a download link and trigger it
    const link = document.createElement("a");
    link.href = image;
    link.download = `${imageName}.png`;
    link.click();
    alert(`Picture saved as ${imageName}.png`);
    setImage(null); // Clear the image preview after saving
    setImageName(""); // Clear the input field
  };

  return (
    <div style={{ textAlign: "center", padding: "20px" }}>
      <h1>Take and Save a Picture</h1>
      {/* Live Camera Feed */}
      <video
        ref={videoRef}
        autoPlay
        playsInline
        style={{ width: "100%", maxWidth: "500px", marginBottom: "10px" }}
      />
      {/* Hidden Canvas for Capturing Picture */}
      <canvas ref={canvasRef} style={{ display: "none" }} />
      <br />
      {/* Button to Capture Picture */}
      <button
        onClick={takePicture}
        style={{ padding: "10px 20px", fontSize: "16px", marginTop: "10px", cursor: "pointer" }}
      >
        Take Picture
      </button>
      <br />
      {image && (
        <div style={{ marginTop: "20px" }}>
          <h2>Captured Image:</h2>
          {/* Display Captured Image */}
          <img
            src={image}
            alt="Captured"
            style={{ width: "100%", maxWidth: "500px", marginTop: "10px", border: "1px solid #ccc" }}
          />
          {/* Input for Picture Name */}
          <div style={{ marginTop: "10px" }}>
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
    </div>
  );
};

export default SavePictureApp;
