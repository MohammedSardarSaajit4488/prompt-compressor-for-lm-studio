# Caveman LM Studio

A Python-based prompt and context compressor for local LLM workflows in LM Studio.

## What this project does

This project helps reduce the size of markdown or text context before sending it to a local language model in LM Studio. It rewrites natural-language text into a shorter, more direct style while preserving important technical content such as code blocks, URLs, headings, file paths, and inline code.

## Why I built it

Local LLMs are useful, but they often have smaller context windows than cloud models. Long prompts, notes, and project context can waste tokens and make responses slower or less useful. This project was built to make local AI workflows more efficient by compressing text before it is sent to the model.

## How it works

1. Write your project notes or prompt in a markdown file.
2. Run the Python script.
3. The script sends the text to a local LM Studio model.
4. The model returns a shorter caveman-style version.
5. The compressed file is saved in a separate folder, while the original is backed up.

## Key features

- Compresses markdown/text for local LLM workflows.
- Preserves code blocks exactly.
- Preserves inline code, URLs, headings, and file paths.
- Works with LM Studio’s local OpenAI-compatible server.
- Saves a backup of the original file.
- Designed for Windows 11 and Python.

## Tech stack

- Python 3.12
- LM Studio local server
- OpenAI Python SDK
- Regular expressions for text safety checks
- Windows batch file for easy execution

## Setup

### Prerequisites
- Python installed
- LM Studio installed
- A model loaded in LM Studio
- LM Studio local server running

### Install dependencies
```bash
pip install openai
```

### Run the script
```bash
python compress.py context\project.md
```

## Folder structure

```text
cavemanidea/
├── compress.py
├── run.bat
├── context/
│   └── project.md
└── compressed/
```

## Example use case

If your project notes are long and detailed, this tool can compress them into a shorter version before they are pasted into LM Studio. That makes the prompt more efficient and easier to reuse across multiple conversations.

## What I learned

- How prompt compression can help local LLM workflows
- How to connect Python with LM Studio’s local API
- How to preserve technical content while shortening natural language
- How to build a small but practical AI tooling project

## Future improvements

- Add smarter validation for compressed output
- Support multiple file types
- Add a simple GUI
- Add automatic prompt compression for chat workflows
- Support vision-related context prep

## License

MIT
