class values:
    GAME_PORTAL = "4pd0n31e"

    CATEGORY_INBOUNDS = "7wkp6v2r"
    CATEGORY_NOSLA = "n2yq98ko"
    CATEGORY_OOB = "lvdowokp"
    CATEGORY_GLITCHLESS = "wk6pexd1"


    VARIABLE_PC_CONSOLE = "kn0mz7ol"
    VALUE_PC_CONSOLE_PC = "jq6nxjnl"
    VALUE_PC_CONSOLE_CONSOLE = "5lmv49yl"

    # Out of Bounds Variables
    VARIABLE_OOB_VERSION = "2lgg0x6l"
    VALUE_OOB_VERSION_3420 = "4qy3x97l"
    VALUE_OOB_VERSION_4104 = "qyzy5nd1"
    VALUE_OOB_VERSION_5135 = "5q85epkq"
    VALUE_OOB_VERSION_LATEST = "21dr45jq"

    VARIABLE_OOB_VAULT_SAVE = "0nwoe0lq"
    VALUE_OOB_VAULT_SAVE_YES = "mlnr2jqp"
    VALUE_OOB_VAULT_SAVE_NO = "4qy362l7"


    # Nosla Variables
    VARIABLE_UNR_OR_LEG = "ql61qmv8"
    VALUE_UNR_OR_LEG_UNRESTRICTED = "21g5r9xl"
    VALUE_UNR_OR_LEG_LEGACY = "jqz97g41"


def getCategory(categoryId: str):
    category = ""
    match categoryId:
        case values.CATEGORY_INBOUNDS:
            category = "Inbounds"
        case values.CATEGORY_GLITCHLESS:
            category = "Glitchless"
        case values.CATEGORY_OOB:
            category = "Out of Bounds"
        case values.CATEGORY_NOSLA:
            category = "No SLA"
        
        case _:
            category = None

    return category
