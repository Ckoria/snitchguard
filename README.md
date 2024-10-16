SnitchGuard - AI-Based Unauthorized Access Detection System
Project Overview
SnitchGuard is an AI-powered security system that integrates with camera systems in cars to detect unauthorized access. The system uses facial recognition to identify individuals and alerts the owner if an unrecognized person enters the vehicle. It can also be adapted for use in other environments, such as homes or offices. The prototype is developed using Python, OpenCV, and DeepFace for facial recognition, with Twilio integrated to send notifications via WhatsApp.

Key Features
Face Identification: Detects and identifies individuals using facial recognition.
Unauthorized Access Detection: Recognizes unauthorized individuals based on a pre-registered list of authorized faces.
Live Camera Feed: Uses a webcam to stream and analyze live video feed.
WhatsApp Notifications: Alerts the owner via WhatsApp if an unauthorized person is detected in the vehicle.
Technology Stack
Programming Language: Python
Libraries & Frameworks:
OpenCV: For capturing and processing video from the webcam.
DeepFace: For facial recognition and verification.
Twilio: For sending WhatsApp notifications in real-time.
Hardware Requirements: Webcam (for live video capture)

Usage
The system will continuously stream video from the webcam.
If an unauthorized face is detected, a WhatsApp message will be sent to notify the owner.
Press q to stop the webcam feed.
Known Issues
The detection accuracy depends on the quality and resolution of the camera feed.
The application may take longer to start on the first run due to model downloads.
Future Improvements
Integrate more robust notifications (email, SMS).
Support for other environments like home or office surveillance.
Improve detection speed and performance optimization.

Contributing
Contributions are welcome! Please create a new issue or submit a pull request.

Contact
For any inquiries or support, reach out to:

Sindiso Christopher Ndlovu
Email: sindiso.chris@gmil.com
