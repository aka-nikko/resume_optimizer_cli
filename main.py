import click
from pathlib import Path

from pydantic import ValidationError
from services.jd_parser import JDParser
from services.docx_writer import DocxWriter
from services.validator import ResumeValidator
from services.ai_optimizer import AIOptimizer
from services.base_resume import BASE_RESUME


@click.command()
@click.option("--resume", required=True, type=click.Path(exists=True, dir_okay=False, readable=True))
@click.option("--jd", required=True, type=click.Path(exists=True, dir_okay=False, readable=True))
@click.option("--output", default="output_resume.docx")
@click.option("--mode", default="local", type=click.Choice(["local", "ai"], case_sensitive=False))

def main(resume, jd, output, mode):
    try:
        output_path = Path(output)
        if output_path.suffix.lower() != ".docx":
            raise ValueError("Output path must end with .docx")

        if output_path.parent and not output_path.parent.exists():
            raise FileNotFoundError(f"Output directory does not exist: {output_path.parent}")

        jd_text = JDParser.parse(jd)
        section_counts = DocxWriter.get_template_section_counts(resume)

        if mode.lower() == "local":
            result = BASE_RESUME
        else:
            result = AIOptimizer.optimize(jd_text, BASE_RESUME, section_counts)

        ResumeValidator.validate(result, section_counts)
        DocxWriter.replace_placeholders(template_path=resume, output_path=str(output_path), resume=result)
    except (OSError, ValueError, RuntimeError, ValidationError) as exc:
        raise click.ClickException(str(exc)) from exc

    click.echo(f"Resume generated: {output_path}")


if __name__ == "__main__":
    main()
