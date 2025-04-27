# ReadAble

A simple-to-use web app providing real-time educational help to students.

---

## Demo

<iframe width="560" height="315" src="https://youtu.be/z2oliS4OltY?si=n9NamQykfu4BMhUw" frameborder="0" allowfullscreen></iframe>

## Inspiration

Have you ever seen a new word and wondered what it meant? ReadAble was inspired by the struggle of students learning a new language, often needing constant translations to understand books. Our app provides real-time reading assistance to help bridge that gap.

## What It Does ❔

- Uses a camera to follow along as you read a book.
- Provides real-time reading help, including:
  - Text-to-speech (TTS) that reads the book aloud.
  - Instant word definitions when a user points at an unknown word.
- Stores scanned books for future use or sharing with other users.

## How We Built It ⚙️

- **Backend**:  
  Python (OpenCV, EasyOCR, pyttsx3, Pygame, MediaPipe, PyMultiDictionary) with Flask server.

- **Frontend**:  
  HTML, CSS/SCSS, JavaScript handling camera feed and user interaction.

## Installation

### Prerequisites

- Python 3.8+
- pip
- Virtual environment (optional but recommended)

### Setup Instructions

1. Clone the repository:
    ```bash
    git clone https://github.com/harsharan-r/ReadAble.git
    cd ReadAble
    ```

2. Create and activate a virtual environment (optional):
    ```bash
    python -m venv venv

    ### For macOS/Linux ###
    source venv/bin/activate

    ### For Windows: ###
    venv\Scripts\activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the app:
    ```bash
    python app.py
    ```

5. Access in your browser at `localhost:5001/`

## Usage

- Launch the app locally.
- Use your device’s camera to follow along while reading a book.
- Tap on a word to hear it pronounced or get a definition.

## Built With

- Python
- Flask
- OpenCV
- EasyOCR
- pyttsx3
- Pygame
- MediaPipe
- PyMultiDictionary
- HTML, CSS/SCSS, JavaScript
- Visual Studio Code

## Links

- [Devpost Project Page](https://devpost.com/software/readable-97ox4i)