from utils.constants import SQUARE_TEMPLATES

class OrientationService:
    @staticmethod
    def get_orientation(template_name: str) -> str:
        if template_name in SQUARE_TEMPLATES:
            return "square"
        return "landscape"
