# Podcast Intelligence

**Ever wished you could have a conversation with your favorite podcast? Now you can!** This project transforms podcast episodes into interactive, AI-driven experiences, allowing users to dive deeper into the content and ask questions directly about the episode.

Using the popular RAG (**Retrieval-Augmented Generation**) technique, this project brings podcasts to life.


## Table of Contents

- [Project Context](#project-context)
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Configuration](#configuration)
- [Contributing](#contributing)
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
   git clone https://github.com/germarr/podcastintelligence.git
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
Once the python libraries are installed on the python environment we can start running the code. 


### Running the Application

To start the project, run:

```bash
python main.py
```

### Command Line Arguments (if applicable)

Explain how to run the project with various arguments, if necessary.

```bash
python main.py --input data.csv --output results.json
```

### Examples

You can include example commands or usage cases:

```bash
python main.py example
```

## Features

- List the main features of the project
- Example:
  - Data processing
  - Visualization of results
  - Automated reports generation

## Configuration

If there are any configuration files (like `.env` or settings), explain how to configure them here.

Example:

1. **Set environment variables**:
   Create a `.env` file in the root directory:
   ```
   API_KEY=yourapikey
   DATABASE_URL=yourdatabaseurl
   ```

2. **Modify configuration files**:
   Describe any configuration settings that may need adjustment.

## Contributing

Guidelines for contributing to the project:

1. Fork the repository
2. Create a new branch (`git checkout -b feature-name`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature-name`)
5. Open a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Any libraries, tools, or resources that helped with the project.
- People or organizations that inspired the work.
