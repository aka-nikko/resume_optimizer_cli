import click
from pathlib import Path

from pydantic import ValidationError
from services.jd_parser import JDParser
from services.docx_writer import DocxWriter
from services.validator import ResumeValidator
from services.ai_optimizer import AIOptimizer
from services.base_resume import BASE_RESUME
from config import DEFAULT_OUTPUT_NAME


@click.command()
@click.option("--resume", required=True, type=click.Path(exists=True, dir_okay=False, readable=True))
@click.option("--jd", required=True, type=click.Path(exists=True, dir_okay=False, readable=True))
@click.option("--output", default=DEFAULT_OUTPUT_NAME)
@click.option("--export-pdf", is_flag=True, default=False, help="Also export the generated DOCX to PDF (Windows, requires docx2pdf)")
@click.option("--pdf-output", default=None, type=click.Path(dir_okay=False), help="Optional path for the exported PDF")
@click.option("--mode", default="local", type=click.Choice(["local", "ai"], case_sensitive=False))

def main(resume, jd, output, export_pdf, pdf_output, mode):
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

        if export_pdf:
            pdf_path = Path(pdf_output) if pdf_output else output_path.with_suffix('.pdf')

            try:
                import platform
                if platform.system() != "Windows":
                    raise RuntimeError("PDF export is supported only on Windows using docx2pdf")

                try:
                    from docx2pdf import convert
                except Exception as exc:
                    raise RuntimeError(
                        "PDF export requires the 'docx2pdf' package. Install it with 'pip install docx2pdf'"
                    ) from exc

                convert(str(output_path), str(pdf_path))
            except Exception as exc:
                raise RuntimeError(f"Failed to export PDF: {exc}") from exc
    except (OSError, ValueError, RuntimeError, ValidationError) as exc:
        raise click.ClickException(str(exc)) from exc

    click.echo(f"Resume generated: {output_path}")
    if export_pdf:
        click.echo(f"PDF exported: {pdf_path}")


if __name__ == "__main__":
    main()
