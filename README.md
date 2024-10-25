# Podcast Intelligence

**Ever wished you could have a conversation with your favorite podcast? Now you can!** This project transforms podcast episodes into interactive, AI-driven experiences, allowing users to dive deeper into the content and ask questions directly about the episode.

Using the popular RAG (**Retrieval-Augmented Generation**) technique, this project brings podcasts to life.


## Table of Contents

- [Podcast Intelligence](#podcast-intelligence)
  - [Table of Contents](#table-of-contents)
  - [Project Context](#project-context)
    - [Key Steps in the Process:](#key-steps-in-the-process)
  - [Installation](#installation)
    - [Prerequisites](#prerequisites)
    - [Setup](#setup)
  - [Usage](#usage)
    - [Running the Application](#running-the-application)
  - [Features](#features)
  - [Configuration](#configuration)
  - [License](#license)
  - [Acknowledgments](#acknowledgments)


## Project Context

This project leverages AI to interact with podcast episodes using a Retrieval-Augmented Generation (RAG) process. The script allows users to ask questions about a specific podcast episode and receive natural-sounding responses based on the episode content.

### Key Steps in the Process:

1. **Audio Retrieval**: 
   - A script is used to fetch podcast episodes from RSS feeds.
   
2. **Transcription**: 
   - The audio is converted into text using OpenAI's Whisper model, ensuring high-quality transcription.

3. **Text Chunking and Diarization**: 
   - The transcribed text is split into manageable chunks, and speaker diarization is performed to identify different speakers and their corresponding timestamps.

4. **Embedding Creation**: 
   - Only the transcribed text (without diarization metadata) is converted into embeddings using a pre-trained language model for efficient similarity searches.

5. **Database Storage**: 
   - Both the text embeddings and diarization results are stored in an optimized PostgreSQL database, designed for fast retrieval based on cosine similarity.

6. **Question-Answering**: 
   - When a user asks a question, it is converted into embeddings. Using cosine similarity, relevant chunks of the podcast are retrieved from the database. The retrieved text is inserted into a prompt for a Large Language Model (LLM), which generates a natural response based on the podcast content.

## Installation

### Prerequisites

- Python version (e.g., `>= 3.7`)
- ffmpeg library installed in computer. There are a bunch of Youtube videos of how to do this. I followed [this one](https://www.youtube.com/watch?v=JR36oH35Fgg)
- All the python packages are in the `requirements.txt` file.

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/germarr/podcastaiproject.git
   cd project-name
   ```

2. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   .venv\Scripts\activate     # Windows
   ```

3. **Install the required packages**:
   ```bash
   pip install -r requirements.txt
   ```


## Usage
Once the python libraries are installed in the python environment we can start running the code. 


### Running the Application

To start the project, run:

```bash
cd audioFiles
python audioInfo.py --input "https://feeds.megaphone.fm/examplepod"
```

## Features
The project has several libraries that process audio, video, embeddings and some extra things.

- Example:
  - Get the Audio From an RSS Feed
  - Get the Audio from a Youtube video.
  - Turn the audio into Embeddings.
  - Send the embeddings to a Postgresql database

## Configuration
The file requires a .env file with the keys and endpoints necessary to run the project.

Example:
1. **Set environment variables**:
   Create a `.env` file in the root directory:
   ```
   API_KEY=yourapikey
   DATABASE_URL=yourdatabaseurl
   ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Any libraries, tools, or resources that helped with the project.
- People or organizations that inspired the work.
