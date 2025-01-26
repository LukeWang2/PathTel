import qrcode

def generate_qr_code(location_id, output_path):
    """
    Generate a QR code with a location identifier.

    Args:
        location_id (str): Identifier for the location (e.g., "Location A").
        output_path (str): Path to save the generated QR code image.
    """
    qr = qrcode.QRCode(
        version=1,  # Controls the size of the QR code
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(f"{{'id': '{location_id}'}}")
    qr.make(fit=True)

    # Create and save the QR code image
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(output_path)

# Generate 8 QR codes with unique IDs
for i in range(1, 9):
    output_file = f"Location_{i}_QRCode.png"
    generate_qr_code(f"Location_{i}", output_file)