import re
import math

class InputParser:
    """
    Functional class containing methods for parsing user input.
    """

    @staticmethod
    def parse_text(text: str, min_value: int = None, max_value: int = None, final_conversion_factor: float=1) -> float:
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
            unit_conversion_mm = {'in': 25.4, 'feet': 304.8, 'ft': 304.8, 'mm': 1, 'cm': 10}
            unit_conversion_in = {'in': 1, 'feet': 12, 'ft': 12, 'mm': 0.0393701, 'cm': 0.393701}

            unit_conversion = unit_conversion_mm if final_conversion_factor == 1 else unit_conversion_in

            if text.replace('.', '').isdigit():
                output_value = float(text)  
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

                output_value = value * unit_conversion.get(unit, 1)  

            output_value = round(output_value, 5)

            if min_value is not None and max_value is not None:    
                output_value = max(min_value, min(output_value, max_value))

            return output_value
        
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
        