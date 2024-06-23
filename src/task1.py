import pandas as pd
import glob


def read_data(hq_path: str, contact_path: str):
    """
    Function to read the data from the Tab Delimited Text files
    """
    country_hq = pd.read_table(hq_path)
    contact_files = glob.glob(contact_path)
    contacts = pd.DataFrame()
    for contact in contact_files:
        contact = pd.read_table(contact)
        contact["country_hq"] = contact.columns[0]
        contact.columns.values[0] = "Invader_Species"
        contacts = pd.concat([contacts, contact])
    return country_hq, contacts


def parse_email(name: str) -> str:
    """
    Function to Check if the email is already present in the name like in DC Characters
    """
    if "@" in name:
        print(f"DC Detected: {name}")
        return name

    return f"{name}@avengers.com"


def get_roles(df: pd.DataFrame, country_code: str) -> pd.DataFrame:
    """
    Function to get the roles of each hero in each country
    """
    country_dict = {"Country_Code": [], "Invader_Species": [], "Role": [], "Email": []}
    for _, row in df.iterrows():
        if pd.notnull(row["attack_role"]):
            country_dict["Country_Code"].append(country_code)
            country_dict["Invader_Species"].append(row["Invader_Species"])
            country_dict["Role"].append("attack_role")
            country_dict["Email"].append(parse_email(row["attack_role"]))
        if pd.notnull(row["defense_role"]):
            country_dict["Country_Code"].append(country_code)
            country_dict["Invader_Species"].append(row["Invader_Species"])
            country_dict["Role"].append("defense_role")
            country_dict["Email"].append(parse_email(row["defense_role"]))
        if pd.notnull(row["healing_role"]):
            country_dict["Country_Code"].append(country_code)
            country_dict["Invader_Species"].append(row["Invader_Species"])
            country_dict["Role"].append("healing_role")
            country_dict["Email"].append(parse_email(row["healing_role"]))
    return pd.DataFrame(country_dict)


def create_lookup_table(
    country_hq: pd.DataFrame, contacts: pd.DataFrame
) -> pd.DataFrame:
    """
    Function to create the lookup table for the roles of each hero in each country
    """
    aliens = pd.merge(
        contacts, country_hq, how="left", right_on=["Aliens"], left_on="country_hq"
    )
    predators = pd.merge(
        contacts, country_hq, how="left", right_on=["Predators"], left_on="country_hq"
    )
    dand = pd.merge(
        contacts,
        country_hq,
        how="left",
        right_on=["D&D Monsters"],
        left_on="country_hq",
    )
    lookup_table = pd.DataFrame()
    for country_code in country_hq["Country Code"].unique():
        print(f"Country Name: {country_code}")
        aliens_temp = aliens[
            (aliens["Country Code"] == country_code)
            & (aliens["Invader_Species"] == "aliens")
        ]
        predators_temp = predators[
            (predators["Country Code"] == country_code)
            & (predators["Invader_Species"] == "predators")
        ]
        dand_temp = dand[
            (dand["Country Code"] == country_code)
            & (dand["Invader_Species"].str.contains("d&d"))
        ]
        roles_aliens = get_roles(aliens_temp, country_code)
        roles_predators = get_roles(predators_temp, country_code)
        roles_dand = get_roles(dand_temp, country_code)
        lookup_table = pd.concat(
            [lookup_table, roles_aliens, roles_predators, roles_dand]
        )
    return lookup_table


def main():
    country_hq, contacts = read_data(
        "./Option2_Tab_Delimited_Text/country_hq.txt",
        "./Option2_Tab_Delimited_Text/contacts/*.txt",
    )
    lookup_table = create_lookup_table(country_hq, contacts)
    lookup_table.to_csv("./solutions/task1.txt", sep="\t", index=False)
    print("Lookup table created successfully")


if __name__ == "__main__":
    main()
