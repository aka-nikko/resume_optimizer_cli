
# Resume Optimizer CLI

> A small CLI to generate ATS-optimized DOCX resumes from a template and a job description. Supports a local template-based mode and an AI-powered optimization mode (OpenAI).

## Features
- Generate a DOCX resume by replacing placeholders in a template `.docx` file.
- AI mode: rewrite resume content to better match a job description using OpenAI.
- Validate generated resumes against configurable rules (summary length, bullets per section, etc.).
- Optional PDF export on Windows via `docx2pdf`.

## Files
- [main.py](main.py) - CLI entrypoint and option parsing.
- [config.py](config.py) - Project configuration and validation rules.
- [services/ai_optimizer.py](services/ai_optimizer.py) - AI integration (OpenAI).
- [services/docx_writer.py](services/docx_writer.py) - DOCX template processing and placeholder replacement.
- [services/jd_parser.py](services/jd_parser.py) - Job description loader.
- [services/validator.py](services/validator.py) - Resume validation rules.
- [services/base_resume.py](services/base_resume.py) - Default resume used in local mode.
- [models/schemas.py](models/schemas.py) - Pydantic models for resume output.
- [requirements.txt](requirements.txt) - Python dependencies.

## Requirements
- Python 3.10+ (a virtual environment is recommended)
- See [requirements.txt](requirements.txt) for needed packages.

Install dependencies:

```bash
python -m venv .venv
./.venv/Scripts/Activate.ps1  # Windows PowerShell
pip install -r requirements.txt
```

## Usage

Basic usage (local template mode):

```bash
python main.py --resume path/to/template.docx --jd path/to/jd.txt --output output_resume.docx --mode local
```

Generate using AI mode (requires `OPENAI_API_KEY`):

```bash
# set OPENAI_API_KEY in environment or create a .env file
python main.py --resume path/to/template.docx --jd path/to/jd.txt --output ai_resume.docx --mode ai --count 1
```

Generate multiple AI variants:

```bash
python main.py --resume template.docx --jd jd.txt --output output.docx --mode ai --count 3
```

Export to PDF (Windows only):

```bash
python main.py --resume template.docx --jd jd.txt --output output.docx --mode local --export-pdf --pdf-output out.pdf
```

Notes
- `--output` must end with `.docx`.
- `--count > 1` is only supported with `--mode ai`.
- PDF export requires Windows and the `docx2pdf` package.
-- By default, generated files are written to the `output/` directory. The CLI will create the directory automatically if it does not exist.

Note: The repository includes the `output/` directory with generated sample resumes exported during testing — these are attached for reference.

## Template placeholders

Templates should include placeholders in the form `{{SUMMARY}}`, `{{SKILLS}}`, `{{EXPERIENCE_1}}`, `{{EXPERIENCE_2}}`, `{{PROJECT_1}}`, etc. Required placeholders: `SUMMARY` and `SKILLS`.

The writer replaces single-line placeholders with text and full-paragraph placeholders (like `{{EXPERIENCE_1}}`) with bullet lists. See [services/docx_writer.py](services/docx_writer.py) for details.

## AI Mode & Environment
- The AI mode uses the OpenAI client and expects an API key set in `OPENAI_API_KEY` or a `.env` file (the project loads environment variables via `python-dotenv`).
- Model, system prompt, and rules are defined in [config.py](config.py). The project expects JSON-only responses from the model and validates them against the schema in [models/schemas.py](models/schemas.py).

## Contributing
- Open issues or submit PRs.
- Follow existing code style.