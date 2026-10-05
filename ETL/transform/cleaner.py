import re


class TextCleaner:
    @staticmethod
    def clean(text: str):
        """
                Clean extracted text while preserving
                paragraph boundaries.
        """

        # Normalize line endings
        text = text.replace("\r\n", "\n")
        text = text.replace("\r", "\n")

        # Remove trailing/leading whitespace
        lines = [
            line.strip()
            for line in text.split("\n")
        ]

        text = "\n".join(lines)

        # Collapse 3+ newlines into 2
        text = re.sub(
            r"\n{3,}",
            "\n\n",
            text
        )
        return text or ''