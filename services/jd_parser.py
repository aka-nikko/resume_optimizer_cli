from pathlib import Path


class JDParser:
    @staticmethod
    def parse(file_path: str) -> str:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"Job description file not found: {file_path}")

        if not path.is_file():
            raise ValueError(f"Job description path is not a file: {file_path}")

        try:
            text = path.read_text(encoding="utf-8").strip()
        except UnicodeDecodeError as exc:
            raise ValueError(f"Job description file must be UTF-8 text: {file_path}") from exc
        except OSError as exc:
            raise OSError(f"Unable to read job description file '{file_path}': {exc}") from exc

        if not text:
            raise ValueError(f"Job description file is empty: {file_path}")

        return text
