import re
import math

class InputParser:
    """
    Functional class containing methods for parsing user input.
    """

    @staticmethod
    def parse_text(text: str, min_value: int = None, max_value: int = None) -> float:
        """
        Parse user input and convert it to a floating point value in millimeters.

        Arguments: 
        - text: original text string. Accepts 'in', 'feet', 'ft', 'mm', and 'cm' as units.
        - min_value: minimum bound for output.
        - max_value: maximum bound for output.

        Returns:
        - Floating point value in millimeters.
        """
        try:
            unit_conversion = {'in': 25.4, 'feet': 304.8, 'ft': 304.8, 'mm': 1, 'cm': 10}

            if text.replace('.', '').isdigit():
                value_mm = float(text)  
            else:
                match = re.match(r'([\d./]+)\s*([a-zA-Z]*)', text)
                if not match:
                    return None  

                value_str, unit = match.group(1), match.group(2).lower()
                if '/' in value_str:
                    value = InputParser._parse_fraction(value_str)
                    if value is None:
                        return None
                else:
                    value = float(value_str)

                if unit and unit not in unit_conversion:
                    return None  

                value_mm = value * unit_conversion.get(unit, 1)  

            value_mm = round(value_mm, 5)

            if min_value is not None and max_value is not None:    
                value_mm = max(min_value, min(value_mm, max_value))

            return value_mm
        
        except Exception as e:
            return text

    @staticmethod
    def _parse_fraction(fraction: str):
        """ Parses fractional string. Returns None in the case of an invalid input. """
        try:
            numerator, denominator = fraction.split('/')
            if denominator == '0':
                return None  
            return float(numerator) / float(denominator)
        except ValueError:
            return None  
        