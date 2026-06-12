import re
from docx import Document
from copy import deepcopy
from docx.shared import Inches, Pt


class DocxWriter:
    FONT_SIZE = 10
    PLACEHOLDER_PATTERN = re.compile(r"\{\{\s*([^{}]+?)\s*\}\}")

    @staticmethod
    def apply_font(paragraph):
        for run in paragraph.runs:
            run.font.size = Pt(DocxWriter.FONT_SIZE)

    @staticmethod
    def add_markdown_bold(paragraph, text):
        parts = re.split(r"(\*\*.*?\*\*)", text)

        for part in parts:
            if(part.startswith("**") and part.endswith("**")):
                run = paragraph.add_run(part[2:-2])
                run.bold = True
            else:
                run = paragraph.add_run(part)
                run.bold = False

            run.font.size = Pt(DocxWriter.FONT_SIZE)

    @staticmethod
    def insert_bullet_list(paragraph, bullets):
        current = paragraph
        current.clear()
        current.add_run("• ")
        DocxWriter.add_markdown_bold(current, bullets[0])

        current.paragraph_format.left_indent = Inches(0.25)
        current.paragraph_format.first_line_indent = Inches(0)

        for bullet in bullets[1:]:
            new_p = deepcopy(current._element)
            current._element.addnext(new_p)

            from docx.text.paragraph import Paragraph

            current = Paragraph(new_p,paragraph._parent)
            current.clear()
            current.add_run("• ")
            DocxWriter.add_markdown_bold(current, bullet)

            current.paragraph_format.left_indent = Inches(0.25)
            current.paragraph_format.first_line_indent = Inches(0)

    @staticmethod
    def build_skill_section(skills):
        lines = []

        for category, skill_list in skills.items():
            lines.append(f"**{category}**: " + ", ".join(skill_list))

        return "\n".join(lines)

    @staticmethod
    def replace_text(paragraph,text):
        paragraph.clear()
        run = paragraph.add_run(text)
        run.font.size = Pt(DocxWriter.FONT_SIZE)

    @staticmethod
    def normalize_placeholder_name(name):
        return re.sub(r"[^A-Z0-9]+", "_", name.upper()).strip("_")

    @staticmethod
    def iter_paragraphs(doc):
        for paragraph in doc.paragraphs:
            yield paragraph

        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    for paragraph in cell.paragraphs:
                        yield paragraph

    @staticmethod
    def format_field_value(field, value):
        if field == "skills":
            return DocxWriter.build_skill_section(value)

        return value

    @staticmethod
    def build_replacements(resume):
        resume_data = resume.model_dump()
        replacements = {
            "SUMMARY": resume_data["summary"],
            "SKILLS": DocxWriter.format_field_value("skills", resume_data["skills"]),
        }

        experience_fields = [
            field
            for field in resume_data
            if field not in {"summary", "skills"} and not field.startswith("project_")
        ]
        project_fields = [
            field
            for field in resume_data
            if field.startswith("project_")
        ]

        for index, field in enumerate(experience_fields, start=1):
            replacements[f"EXPERIENCE_{index}"] = resume_data[field]

        for index, field in enumerate(project_fields, start=1):
            replacements[f"PROJECT_{index}"] = resume_data[field]

        return replacements

    @staticmethod
    def replace_placeholders(template_path, output_path, resume):
        doc = Document(template_path)
        replacements = DocxWriter.build_replacements(resume)

        for paragraph in DocxWriter.iter_paragraphs(doc):
            matches = DocxWriter.PLACEHOLDER_PATTERN.findall(paragraph.text)
            if not matches:
                continue

            if len(matches) == 1 and DocxWriter.PLACEHOLDER_PATTERN.fullmatch(paragraph.text.strip()):
                placeholder = DocxWriter.normalize_placeholder_name(matches[0])
                value = replacements.get(placeholder)

                if isinstance(value, list):
                    DocxWriter.insert_bullet_list(paragraph, value)
                    continue

            new_text = paragraph.text
            for match in matches:
                placeholder = DocxWriter.normalize_placeholder_name(match)
                value = replacements.get(placeholder)
                if value is None:
                    continue

                if isinstance(value, list):
                    value = "\n".join(value)

                new_text = re.sub(
                    r"\{\{\s*" + re.escape(match) + r"\s*\}\}",
                    lambda _: value,
                    new_text,
                )

            new_text = new_text.strip()

            if new_text == paragraph.text:
                continue

            paragraph.clear()
            DocxWriter.add_markdown_bold(paragraph, new_text)

        doc.save(output_path)