import resources
import calendar

def align_currency_text(alignment: bool, place: str): #True if the symbol is to the left, False if it is to the right.
    match place:
        case 'text_box':
            return 0.035 if alignment == True else 0.855
        case _:
            raise resources.PlaceDoesNotExistError(f"The 'place' keyword argument does not support '{place}'")

def color_setter(value1: float, seperator: float = 0.0,
                 dft_less = (191 / 255, 30 / 255, 30 / 255, 1),
                 dft_more = (127 / 255, 199 / 255, 127 / 255, 1),
                 dft_exact = (1, 1, 1, 1)):
    if value1 > seperator: return dft_more
    elif value1 < seperator: return dft_less
    else: return dft_exact

def sign_setter(value1: float, seperator: float = 0.0,
                 dft_less = "-",
                 dft_more = "+",
                 dft_exact = ""):
    if value1 > seperator: return dft_more
    elif value1 < seperator: return dft_less
    else: return dft_exact
