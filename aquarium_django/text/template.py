from pathlib import Path
from typing import Callable, Dict, Any, Type, List


class TextTemplate(object):
    """AAAAAAAAAAAAAAAAAAAA"""
    def __init__(self, template_evaluator: Type):
        self.template_evaluator: Type = template_evaluator()


    def templates_from_files(self, paths: List[Path], contexts: List[Dict]) -> Dict:
        """
        AAAAAAAAAAAAAAAAAAAAAAAAA
        :param paths:
        :param contexts:
        :return:
        """
        evaluated_templates = {}
        for path, context in zip(paths, contexts):
            evaluated_templates[f"{path.stem}_content"] = self.template_from_file(path, context)
        return evaluated_templates

    def template_from_file(self, path: Path, context: Dict[str, Any]) -> str:
        """
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        :param path:
        :param context:
        :return:
        """
        with open(path, "r") as template_file:
            template = template_file.read()

        return self.template_evaluator.evaluate(template, context)

    def evaluate_template(self, evaluated_string: str, context: Dict[str, Any]) -> str:
        """
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        :return:
        :raises:
            ValueError
        """
        if self.template_evaluator is None:
            raise ValueError("Template evaluator cannot be empty")

        return self.template_evaluator.evaluate(evaluated_string, context)
