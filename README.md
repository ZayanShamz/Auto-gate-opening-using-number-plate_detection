# Auto Gate Opening System using Number Plate Detection

This project is designed to implement an automated gate opening system based on number plate detection. It uses pytesseract for Optical Character Recognition (OCR) to read number plates.

## Requirements

To set up and run the Auto Gate Opening System, you'll need the following requirements:

- **Python:** Version 3.10.8
- **pytesseract:** Version 0.3.10
- **opencv-python:** Version 4.5.5.64 (try to install the same version as mentioned)
- **Flask**
- **tkinter**
- **pymysql**

Additionally, make sure to have the provided Haarcascade XML file for object detection.

## How It Works

The Auto Gate Opening System uses OCR (Optical Character Recognition) to recognize number plates. Here's a high-level overview of how it functions:

1. The system captures images of vehicles approaching the gate using a camera.
2. It uses pytesseract to perform OCR on the captured images and extract the text from the number plates.
3. The extracted number plate text is compared to a predefined list of authorized number plates from the database.
4. If the number plate matches an authorized entry, the gate opens automatically.


## Usage

1. Ensure that the camera is set up to capture images of vehicles approaching the gate.
2. As vehicles approach the gate, the system will capture their number plates and perform OCR.
3. Authorized number plates will trigger the gate to open automatically.

## Note

- The accuracy of number plate recognition may vary depending on factors such as camera placement, lighting conditions, and the quality of the number plates themselves.
