from enum import Enum


def normalize_string(name:str) -> str:
    # set in lowercase
    name = name.lower()
    # remove possible spaces at the end or start
    name = name.strip()
    # remove special characters
    name = ''.join(e for e in name if is_alnum_or_space(e))
    # replace space for _
    name = ' '.join(name.split())

    name = name.replace(" ", "_")

    return name

def is_alnum_or_space(name:str) -> bool:
    return all(c.isalnum() or c.isspace() for c in name)


class UnitMeasure(Enum):
    """Unit measure."""
    oz = "ounce"
    lb = "pound"
    fl = "ounce"
    kg = "kilo"
    gal = "gallon"
    ml =  "milliliter"
    g =  "gram"
    l =   "liter"
    floz = "once"

    @classmethod
    def get_unit_measure(cls, unit:str) -> str:
        """Get unit measure."""
        if isinstance(unit, str):
            unit.replace(" ", "")
        try:
            return cls[unit].value
        except:
            return None
    