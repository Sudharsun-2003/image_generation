# AI Automation - API Processing Pipeline

A production-style Python automation project for processing video scene data and preparing local storage for generated images.

## Project Goal

This system automates the fetching, filtering, and processing of video scene data from a backend API. It specifically targets `IMAGE_SLIDE` scenes, determines their orientation based on templates, and prepares the local directory structure for future AI-generated images.

## Features

- **API Integration:** Reusable client with bearer authentication and persistent sessions.
- **Scene Filtering:** Extracts and filters `IMAGE_SLIDE` types.
- **Orientation Detection:** Logic to determine "square" or "landscape" orientation.
- **Structured Data:** Uses Python `dataclasses` for clean, type-safe data handling.
- **Local Storage Architecture:** Automatically prepares output directories for images.
- **Logging:** Comprehensive logging using `loguru`.

## Tech Stack

- Python 3.12+
- `requests` (API Calls)
- `python-dotenv` (Environment Config)
- `loguru` (Structured Logging)
- `pathlib` (File System Ops)
- `dataclasses` & `typing` (Data Modeling)

## Setup

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment:**
   Copy `.env.example` to `.env` and fill in your credentials:
   ```bash
   API_URL=https://2rsazlrzod.execute-api.us-west-2.amazonaws.com/dev/va/videos
   BEARER_TOKEN=your_token_here
   ```

## Usage

Run the main automation script:
```bash
python main.py
```

## Project Structure

```
ai_automation/
├── main.py              # Application entry point
├── api/                 # API Client and Services
├── services/            # Business logic (filtering, orientation, storage)
├── models/              # Dataclasses
├── utils/               # Logger and constants
├── output/              # Processed data and future images
└── logs/                # Application logs
```

## Engineering Standards

- Modular architecture with dependency injection.
- Robust exception handling and structured logging.
- Type hints throughout the codebase.
- Scalable design for future AI image generation integration.
