import resources

def align_currency_text(alignment: bool, place: str): #True if the symbol is to the left, False if it is to the right.
    match place:
        case 'text_box':
            return 0.035 if alignment == True else 0.855
        case _:
            raise resources.PlaceDoesNotExistError(f"The 'place' keyword argument does not support '{place}'")

