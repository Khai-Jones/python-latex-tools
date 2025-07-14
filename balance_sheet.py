"""
Global Variables
"""

current_assets = {}
non_current_assets = {}
current_liabilities = {}
non_current_liabilities = {}
capital = {}


def choosing_dict():
    name = ""
    dictionary = {}

    print("1. Current Assets")
    print("2. Non-current Assets")
    print("3. Current Liability")
    print("4. Non-current Liability")
    print("5. Capital")

    while True:
        print("\n")
        decision = input("Type (1,2,3,4,5): ").strip()
        if decision == "1":
            dictionary = current_assets
            name = "current assets"
            break
        if decision == "2":
            dictionary = non_current_assets
            name = "non current assets"
            break
        if decision == "3":
            dictionary = current_liabilities
            name = "current liabilites"
            break
        if decision == "4":
            dictionary = non_current_liabilities
            name = "non current liabilties"
            break
        if decision == "5":
            dictionary = capital
            name = "capital"
            break

        print("Choose a valid choice")

    return dictionary, name


def section_input(dictionary, name):
    """
    Prompt user to input asset names and values until 'done' is entered.
    Stores the input into the global 'assets' dictionary with integer values.
    """
    print(f"{name} section ")
    while True:
        outer_key = input(f"Enter {name} name: ").strip().lower()
        if outer_key.strip().lower() == "done":
            break
        try:
            dictionary[outer_key] = {}
            dictionary[outer_key]["less"] = {}

            value = input(f"Enter {name} value: ")
            dictionary[outer_key]["value"] = int(value)

            while True:
                choice = input("Exter a less item (y/n): ").strip().lower()
                if choice == "n":
                    break
                less_name = input(f"Enter less item for {name}: ")
                less_value = input("Enter less value for the item: ")

                dictionary[outer_key]["less"][less_name] = int(less_value)

        except ValueError:
            print("Enter a valid number")


def process_input():
    """
    Processes asset, liability, and equity dictionaries into LaTeX tabular format.
    Returns a string of LaTeX code representing the Statement of Financial Position.
    """

    def helper_func(dictionary):
        component_row = " "
        value_total = 0
        less_value_total = 0

        entries = list(dictionary.items())  # For checking last item

        for idx, (name, data) in enumerate(entries):
            item_less_total = 0

            if not data["less"]:
                component_row += (
                    f"{name} & \\${data['value']:,} &  & \\${data['value']:,} \\\\ \n"
                )
            else:
                component_row += f"{name} & \\${data['value']:,} & & \\\\ \n"
                less_items = list(data["less"].items())

                for less_name, less_value in less_items:
                    item_less_total += less_value
                    component_row += (
                        f"Less: {less_name} &  &  (\\${less_value:,})  \\\\ \n"
                    )

                is_last_entry = idx == len(entries) - 1
                if not is_last_entry:
                    nbv = data["value"] - item_less_total
                    component_row += f" & & & \\${nbv:,} \\\\ \n"

            value_total += data["value"]
            less_value_total += item_less_total

        return component_row, value_total, less_value_total

    current_ass_row, current_asset_total, ca_less_value_total = helper_func(
        current_assets
    )
    ncurrent_ass_row, ncurrent_asset_total, nca_less_value_total = helper_func(
        non_current_assets
    )
    current_liab_row, current_liab_total, cl_less_value_total = helper_func(
        current_liabilities
    )
    ncurrent_liab_row, ncurrent_liab_total, ncl_less_value_total = helper_func(
        non_current_liabilities
    )
    capital_row, capital_total, c_less_value_total = helper_func(capital)

    return f"""

\\begin{{center}}
\\begin{{tabular}}{{lrrr}}
\\toprule
 & \\textbf{{Cost (\\$)}} & \\textbf{{Depreciation (\\$)}} & \\textbf{{NBV (\\$)}} \\\\
\\midrule
\\textbf{{Non-current assets}} & & & \\\\
{ncurrent_ass_row}
\\addlinespace
Total NCA & \\${ncurrent_asset_total:,} & (\\${nca_less_value_total:,}) & \\${(ncurrent_asset_total - nca_less_value_total):,} \\\\
\\midrule
\\textbf{{Current assets}} & & & \\\\
{current_ass_row}
\\addlinespace
Total Current Assets & \\${current_asset_total:,} & (\\${ca_less_value_total:,}) & {(current_asset_total - ca_less_value_total):,} \\\\
\\midrule
\\textbf{{Total assets}} & & & \\${((ncurrent_asset_total - nca_less_value_total) + (current_asset_total - ca_less_value_total) ):,} \\\\
\\midrule
\\textbf{{Capital}} & & & \\\\
{capital_row}
\\addlinespace
Total Capital & \\${capital_total:,} & \\{c_less_value_total:,} & \\${(capital_total - c_less_value_total):,} \\\\
\\midrule
\\textbf{{Non-current liabilities}} & & & \\\\
{ncurrent_liab_row}
\\addlinespace
Total Non-current Liabilities & \\${ncurrent_liab_total:,} & \\${ncl_less_value_total:,} & \\${(ncurrent_liab_total - ncl_less_value_total):,} \\\\
\\midrule
\\textbf{{Current liabilities}} & & & \\\\
{current_liab_row}
\\addlinespace
Total Current Liabilities & \\${current_liab_total:,} &\\${cl_less_value_total:,} & \\${(current_liab_total - cl_less_value_total):,}\\\\
\\midrule
\\textbf{{Total Capital and Liabilities}} & & & \\${((capital_total - c_less_value_total) + (ncurrent_liab_total - ncl_less_value_total) + (current_liab_total - cl_less_value_total)):,} \\\\
\\bottomrule
\\end{{tabular}}
\\end{{center}}

      """


# Create latex output
def main():
    """
    Runs the full input and LaTeX generation process for the balance sheet.
    """

    while True:
        dictionary, name = choosing_dict()
        section_input(dictionary, name)
        again = (
            input("Do you want to enter records for another section (y/n)?: ")
            .strip()
            .lower()
        )
        if again != "y":
            break

    output = process_input()

    file_name = input("Enter name of file (.tex): ")
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(output)
    print("File Created")


main()
