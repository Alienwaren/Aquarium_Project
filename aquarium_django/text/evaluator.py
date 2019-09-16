from string import Template
from typing import Any, Dict
import markdown
from abc import ABC, abstractmethod


class TextEvaluatorBase(ABC):
    @abstractmethod
    def evaluate(self, template: str, context: Dict[str, Any]):
        pass


class MarkdownTextEvaluator(TextEvaluatorBase):
    def evaluate(self, template: str, context: Dict[str, Any]) -> str:
        """
        AAAAAAAAAAA
        :param template:
        :param context:
        :return:
        """
        if not str:
            raise ValueError("Cannot parse empty string")

        parsed_markdown_as_html = markdown.markdown(template)
        html_template = Template(parsed_markdown_as_html)

        return html_template.safe_substitute(context)
