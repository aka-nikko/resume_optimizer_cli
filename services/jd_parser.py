from pathlib import Path


class JDParser:
    @staticmethod
    def parse(file_path: str) -> str:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(file_path)

        return path.read_text(encoding="utf-8", errors="ignore")