from docx import Document
from copy import deepcopy
from docx.shared import Inches, Pt


class DocxWriter:
    @staticmethod
    def insert_bullet_list(paragraph, bullets):
        current = paragraph
        current.text = f"• {bullets[0]}"

        current.paragraph_format.left_indent = Inches(0.25)
        current.paragraph_format.first_line_indent = Inches(0)

        for run in current.runs:
            run.font.size = Pt(10)

        for bullet in bullets[1:]:
            new_p = deepcopy(current._element)
            current._element.addnext(new_p)

            from docx.text.paragraph import Paragraph

            current = Paragraph(new_p, paragraph._parent)
            current.text = f"• {bullet}"

            current.paragraph_format.left_indent = Inches(0.25)
            current.paragraph_format.first_line_indent = Inches(0)

            for run in current.runs:
                run.font.size = Pt(10)

    @staticmethod
    def build_skill_section(skills):
        lines = []

        for category, skill_list in skills.items():
            lines.append(f"{category}: " + ", ".join(skill_list))

        return "\n".join(lines)

    @staticmethod
    def replace_placeholders(template_path, output_path, resume):
        doc = Document(template_path)

        replacements = {
            "{{SUMMARY}}"       : resume.summary,
            "{{KPIT_SE}}"       : resume.kpit_se,
            "{{KPIT_ASE}}"      : resume.kpit_ase,
            "{{KPIT_TRAINEE}}"  : resume.kpit_trainee,
            "{{NIC}}"           : resume.nic,
            "{{DIT}}"           : resume.dit,
            "{{SKILLS}}"        : DocxWriter.build_skill_section(resume.skills),
            "{{PROJECT_DAT}}"   : resume.project_dat,
            "{{PROJECT_GPT}}"   : resume.project_gpt,
            "{{PROJECT_ACG}}"   : resume.project_acg,
            "{{PROJECT_CMS}}"   : resume.project_cms
        }

        for paragraph in doc.paragraphs:
            for key, value in replacements.items():
                if key in paragraph.text:
                    if isinstance(value, list):
                        DocxWriter.insert_bullet_list(paragraph, value)
                    else:
                        paragraph.text = (paragraph.text.replace(key, value))
                        
                        for run in paragraph.runs:
                            run.font.size = Pt(10)

        doc.save(output_path)