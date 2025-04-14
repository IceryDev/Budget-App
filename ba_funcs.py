import resources
import calendar
import datetime
import dill

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

def rtrn_disp(): #Return displayed month
    return datetime.date(resources.disp_year, resources.disp_month % 12 + 1, 1)

def save_entry_groups():
    for key, value in resources.entry_groups.items():
        resources.serializable_groups[key] = resources.EntryGroup(key, entries=[x.entry for x in value.entries])
    with open('logs.pkl', 'wb') as file:
        dill.dump([resources.serializable_groups, resources.dft_acc, resources.dft_ctg, resources.budget_groups], file)

def load_entry_groups():
    try:
        with open('logs.pkl', 'rb') as file:
            temp_list = dill.load(file)
            resources.serializable_groups = temp_list[0]
            resources.dft_acc = temp_list[1]
            resources.dft_ctg = temp_list[2]
            resources.budget_groups = temp_list[3]
            return resources.serializable_groups
    except FileNotFoundError:
        pass

