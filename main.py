import click
from services.jd_parser import JDParser
from services.docx_writer import DocxWriter
from services.validator import ResumeValidator
from services.ai_optimizer import AIOptimizer
from services.base_resume import BASE_RESUME


@click.command()
@click.option("--resume", required=True)
@click.option("--jd", required=True)
@click.option("--output", default="output_resume.docx")
@click.option("--mode", default="local")

def main(resume, jd, output, mode):
    jd_text = JDParser.parse(jd)

    if mode == "local":
        result = BASE_RESUME
    elif mode == "ai":
        base_resume = BASE_RESUME
        result = AIOptimizer.optimize(jd_text, base_resume)
    else:
        raise ValueError(f"Unknown mode: {mode}")

    ResumeValidator.validate(result)
    DocxWriter.replace_placeholders(template_path=resume, output_path=output, resume=result)

    print(f"Resume generated: {output}")


if __name__ == "__main__":
    main()