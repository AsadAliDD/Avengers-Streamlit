import pandas as pd
from task1 import read_data
import collections


ROLE_DICT = {
    "attack_role": "A",
    "defense_role": "D",
    "healing_role": "H",
    "attack_role+defense_role": "AD",
    "attack_role+healing_role": "AH",
    "defense_role+healing_role": "DH",
    "attack_role+defense_role+healing_role": "ADH",
}


def map_roles(row: pd.Series, hero: "list[str]"):
    """
    Function to map roles to the shorthand format of A,D,H,AD,AH,DH,ADH
    """
    roles = ["attack_role", "defense_role", "healing_role"]
    assigned_role = [col for col in roles if row[col] == hero]
    assigned_role = "+".join(assigned_role)
    return ROLE_DICT[assigned_role]


def find_unique_heroes(contacts: "pd.DataFrame") -> "list[str]":
    """
    Function to find unique heroes from the contacts dataframe
    """
    heroes = []
    for col in ["attack_role", "defense_role", "healing_role"]:
        heroes += contacts[col].dropna().unique().tolist()
    return list(set(heroes))


def create_heroes_table(contacts: pd.DataFrame, heroes: "list[str]"):
    """
    Function to create a table for each hero with the country and the roles they play
    """
    for hero in heroes:
        print("Processing hero: ", hero)

        name = hero if "@" not in hero else hero.split("@")[0]
        # output_dict = {name: []}
        output_dict = collections.defaultdict(list)
        hr = contacts[
            (contacts["attack_role"] == hero)
            | (contacts["defense_role"] == hero)
            | (contacts["healing_role"] == hero)
        ]
        for _, row in hr.iterrows():
            invader = row["Invader_Species"]
            all_roles = map_roles(row, hero)
            output_dict[hero].append(row["country_hq"])
            output_dict[invader].append(all_roles)

        output_dict[hero] = list(dict.fromkeys(output_dict[hero]))
        pd.DataFrame.from_dict(output_dict, orient="index").T.to_csv(
            f"./solutions/task2/{name}.txt", sep="\t", index=False
        )


def main():
    _, contacts = read_data(
        "./Option2_Tab_Delimited_Text/country_hq.txt",
        "./Option2_Tab_Delimited_Text/contacts/*.txt",
    )
    heroes = find_unique_heroes(contacts)
    print(f"Total Heroes: {len(heroes)}")
    create_heroes_table(contacts, heroes)
    print("All Heroes Processed!")


if __name__ == "__main__":
    main()
