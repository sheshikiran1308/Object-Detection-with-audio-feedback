# Object Detection with Audio Feedback

A browser-based object-detection project built with Django, OpenCV, and cvlib. It captures an image from the user's webcam, detects objects in the captured frame, displays the annotated image and object names, and reads the detected names aloud using the browser's speech synthesis.

## Features

- Opens the webcam from the browser.
- Captures an image when **Take Snapshot** is clicked.
- Detects common objects with the YOLOv3 model provided by cvlib.
- Displays the captured frame with detection boxes and labels.
- Shows and speaks the detected object names.
- Shows a status message if the camera is unavailable or no objects are detected.

This is a snapshot-based application: detection runs after clicking the button, not continuously on every video frame.

## Technology

- Python 3.9 (64-bit recommended)
- Django 3.2.10
- OpenCV 4.5.3.56
- cvlib 0.2.6
- NumPy 1.19.5
- Webcam.js, jQuery, and the browser Web Speech API

The app uses OpenCV's DNN object detector through cvlib; TensorFlow is not needed to run this project's detection endpoint.

## Project layout

```text
.
|-- requirements.txt
|-- webapp/
|   |-- manage.py
|   |-- webapp/                 # Django project configuration
|   |-- home/
|       |-- views.py            # Snapshot upload and object detection
|       |-- urls.py
|       |-- templates/
|       |-- static/home/
|           |-- js/             # Webcam startup and snapshot UI
|           |-- css/
|           |-- images/         # UI assets and generated snapshot
|-- code/                       # Standalone/example detection code
```

The YOLO weights are intentionally excluded from Git because the full YOLOv3 weights file is larger than GitHub's 100 MB file limit. On the first detection, cvlib downloads the model configuration, class labels, and weights into its local cache under:

```text
%USERPROFILE%\.cvlib\object_detection\yolo\yolov3\
```

An internet connection is therefore required for the first detection. The weights are reused from the cache on later runs.

## Requirements

- Windows 10/11 (instructions below use PowerShell).
- Python 3.9, 64-bit. The pinned legacy OpenCV/NumPy stack is intended for this Python version; newer Python versions may not have compatible wheels for these pins.
- A working webcam and permission to use it in the browser.
- Internet access on the first object-detection request, so cvlib can download the YOLOv3 model.
- A current browser such as Chrome or Edge. Camera access is allowed on `localhost`; a deployed site must use HTTPS.

## Setup and run (Windows PowerShell)

Run these commands from the repository root (the folder containing `requirements.txt`):

1. Create a virtual environment with Python 3.9:

   ```powershell
   py -3.9 -m venv .venv
   ```

   If the Python launcher is not installed, use the full path to your Python 3.9 executable to create the environment.

2. Activate the environment:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation for this session, run:

   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   .\.venv\Scripts\Activate.ps1
   ```

3. Install the project dependencies:

   ```powershell
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```

4. Change to the Django project directory and initialize its local database:

   ```powershell
   Set-Location .\webapp
   python manage.py migrate
   ```

5. Check the Django configuration:

   ```powershell
   python manage.py check
   ```

6. Start the development server:

   ```powershell
   python manage.py runserver
   ```

7. Open the application in a browser:

   ```text
   http://127.0.0.1:8000/
   ```

Keep the terminal running while using the app. Stop the development server with `Ctrl+C`.

## Use the application

1. Open the **Prediction** section of the page.
2. Allow the browser to access the webcam when prompted.
3. Wait for the status to say the camera is ready.
4. Point the camera at a clear, well-lit, recognizable object.
5. Click **Take Snapshot** and wait for detection to finish.
6. The annotated snapshot and detected labels appear below the camera. When labels are detected, the browser reads them aloud.

The model recognizes common object categories from the COCO dataset. Detection is not guaranteed for every object, particularly when the object is small, obscured, poorly lit, or outside the model's supported categories. If no object is found, adjust the camera and try again.

## Troubleshooting

### `py -3.9` cannot find Python

Install a 64-bit Python 3.9 release, then reopen PowerShell and repeat the setup steps. Confirm the launcher sees it with:

```powershell
py -0p
```

### Camera does not start or the snapshot button cannot be used

- Allow camera access for `http://127.0.0.1:8000/` in the browser.
- Check that another application is not exclusively using the webcam.
- Reload the page after changing camera permissions.
- Try a current Chrome or Edge browser.
- Check the camera status message on the page and the Django terminal for errors.

### The first detection is slow or fails to download the model

The first request downloads the YOLOv3 files. Verify that internet access is available, then click **Take Snapshot** again. Once downloaded, the files are cached under `%USERPROFILE%\.cvlib\object_detection\yolo\yolov3\`.

### No objects are detected

Place a supported object in clear view, improve lighting, move closer if the object is small, and take another snapshot. A successful request with an empty label list means the model did not recognize an object in that frame.

### No speech is heard

Check the browser and operating-system volume. Speech uses the browser's built-in Web Speech API and may depend on installed voices and browser support.

## Notes

- The Django development server is for local development only; do not expose it as a production server.
- The current Django settings use development defaults. Before deploying, configure a secure `SECRET_KEY`, `DEBUG = False`, appropriate `ALLOWED_HOSTS`, HTTPS, static-file serving, upload validation/limits, and a production-grade server.
- The snapshot endpoint writes to a fixed image path under `home/static/home/images/`; this simple demo layout is not designed for concurrent users or production storage.
- Webcam access on a public website requires HTTPS. `localhost` is treated as a secure context by modern browsers.
