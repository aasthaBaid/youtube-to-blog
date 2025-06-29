# YouTube to Blog Post Generator

This project is a powerful command-line application that automates the process of creating a well-structured blog post from any YouTube video. It leverages LangChain and LangGraph to build a robust, multi-step workflow that fetches the video's transcript, intelligently generates a title, and then writes a complete article.

## Features

-   **Automatic Transcript Fetching**: Simply provide a YouTube URL, and the script handles the rest.
-   **AI-Powered Title Generation**: Creates a concise, engaging, and SEO-friendly title based on the video's content.
-   **Full Blog Post Creation**: Generates a comprehensive blog post, complete with an introduction, structured headings, and a concluding summary.
-   **Stateful Workflow**: Built with LangGraph to ensure a reliable and easy-to-understand generation process.
-   **Secure API Key Handling**: Uses a `.env` file to keep your Google API key safe and secure.

## Required Libraries

To run this project, you will need the following Python libraries:

```
langchain-community
langchain-google-genai
langgraph
youtube-transcript-api
python-dotenv
google-generativeai
```

## Getting Started

Follow these steps to set up and run the project on your local machine.

### 1. Download the Files

First, ensure you have the following files in the same project directory:

-   `yt_blog.py` (The main Python script)
-   `requirements.txt`

### 2. Create a Virtual Environment (Recommended)

It's a best practice to create a virtual environment to manage project-specific dependencies.

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install the Dependencies

Install all the required libraries at once using the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### 4. Set Up Your API Key

The script needs a Google AI API key to function.

1.  Create a new file in your project directory and name it `.env`.
2.  Open the `.env` file and add your API key in the following format:

    ```
    GOOGLE_API_KEY="YOUR_API_KEY_HERE"
    ```
    *(Replace `YOUR_API_KEY_HERE` with the key you generated from Google AI Studio.)*

## How to Run the Script

Once the setup is complete, running the application is simple.

1.  Open your terminal or command prompt.
2.  Make sure your virtual environment is activated.
3.  Run the following command:

    ```bash
    python yt_blog.py.py
    ```

4.  The script will then prompt you to enter a YouTube video URL. Paste the URL and press Enter. The final blog post will be printed directly to your console.
