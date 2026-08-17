"""Select and derive research-relevant Census 2022 Small Area features."""

import csv
from pathlib import Path


PROJECT_FOLDER = Path(__file__).resolve().parents[1]
INPUT_FILE = PROJECT_FOLDER / "data" / "raw" / "cso_saps_2022_small_area.csv"
OUTPUT_FILE = (
    PROJECT_FOLDER
    / "data"
    / "processed"
    / "census_demographic_features_small_area_2022.csv"
)


def number(row, field):
    value = row.get(field, "").strip()
    return float(value) if value else 0.0


def total(row, fields):
    return sum(number(row, field) for field in fields)


def ratio(numerator, denominator):
    return round(numerator / denominator * 100, 4) if denominator else ""


def clean_count(value):
    return int(value) if float(value).is_integer() else value


AGE_65_PLUS = [
    "T1_1AGE65_69T",
    "T1_1AGE70_74T",
    "T1_1AGE75_79T",
    "T1_1AGE80_84T",
    "T1_1AGEGE_85T",
]
PRE_2001 = [
    "T6_2_PRE19H",
    "T6_2_19_45H",
    "T6_2_46_60H",
    "T6_2_61_70H",
    "T6_2_71_80H",
    "T6_2_81_90H",
    "T6_2_91_00H",
]
THIRD_LEVEL = [
    "T10_4_HCT",
    "T10_4_ODNDT",
    "T10_4_HDPQT",
    "T10_4_PDT",
    "T10_4_DT",
]
LOW_EDUCATION = ["T10_4_NFT", "T10_4_PT", "T10_4_LST"]


def transform(row):
    population = number(row, "T1_1AGETT")
    children = number(row, "T10_1_LT15T")
    older = total(row, AGE_65_PLUS)
    households = number(row, "T5_1T_H")
    household_persons = number(row, "T5_1T_P")
    one_person = number(row, "T5_1OP_H")
    one_parent = total(row, ["T5_1OPFC_H", "T5_1OPMC_H"])

    labour_total = number(row, "T8_1_TT")
    employed = number(row, "T8_1_WT")
    unemployed = total(row, ["T8_1_LFFJT", "T8_1_STUT", "T8_1_LTUT"])
    retired = number(row, "T8_1_RT")
    unable_to_work = number(row, "T8_1_UTWSDT")

    education_total = number(row, "T10_4_TT")
    third_level = total(row, THIRD_LEVEL)
    low_education = total(row, LOW_EDUCATION)

    housing_stock = number(row, "T6_8_T")
    occupied = number(row, "T6_8_O")
    temporarily_absent = number(row, "T6_8_TA")
    holiday_homes = number(row, "T6_8_UHH")
    other_vacant = number(row, "T6_8_OVD")

    dwelling_total = number(row, "T6_1_TH")
    house_bungalow = number(row, "T6_1_HB_H")
    apartment = total(row, ["T6_1_FA_H", "T6_1_BS_H"])

    construction_total = number(row, "T6_2_TH")
    pre_2001 = total(row, PRE_2001)
    built_2016_later = number(row, "T6_2_16LH")

    tenure_total = number(row, "T6_3_TH")
    owner_occupied = total(row, ["T6_3_OMLH", "T6_3_OOH"])
    private_rented = number(row, "T6_3_RPLH")
    social_rented = total(row, ["T6_3_RLAH", "T6_3_RVCHBH"])

    heating_total = number(row, "T6_5_T")
    oil = number(row, "T6_5_OCH")
    gas = number(row, "T6_5_NGCH")
    electricity = number(row, "T6_5_ECH")
    solid_fuel = total(row, ["T6_5_CCH", "T6_5_PCH"])
    no_central_heating = number(row, "T6_5_NCH")

    renewable_total = number(row, "T6_10_T")
    has_renewable = number(row, "T6_10_RE")

    counts = {
        "population": population,
        "children_under_15": children,
        "persons_65_plus": older,
        "private_households": households,
        "persons_in_private_households": household_persons,
        "one_person_households": one_person,
        "one_parent_households": one_parent,
        "labour_status_population": labour_total,
        "persons_at_work": employed,
        "unemployed_persons": unemployed,
        "retired_persons": retired,
        "unable_to_work_persons": unable_to_work,
        "education_population": education_total,
        "third_level_educated": third_level,
        "low_education": low_education,
        "total_housing_stock": housing_stock,
        "occupied_dwellings": occupied,
        "temporarily_absent_dwellings": temporarily_absent,
        "holiday_homes": holiday_homes,
        "other_vacant_dwellings": other_vacant,
        "house_or_bungalow_households": house_bungalow,
        "apartment_or_bedsit_households": apartment,
        "pre_2001_dwellings": pre_2001,
        "built_2016_or_later_dwellings": built_2016_later,
        "owner_occupied_households": owner_occupied,
        "private_rented_households": private_rented,
        "social_rented_households": social_rented,
        "oil_heated_households": oil,
        "gas_heated_households": gas,
        "electric_heated_households": electricity,
        "coal_or_peat_heated_households": solid_fuel,
        "no_central_heating_households": no_central_heating,
        "renewable_energy_households": has_renewable,
    }

    result = {
        "census_year": 2022,
        "small_area_guid": row["GUID"],
        "small_area_code": row["GEOGID"],
        "urban_rural_code": row["UR_Category"],
        "urban_rural_class": row["UR_Category_Desc"],
    }
    result.update({key: clean_count(value) for key, value in counts.items()})
    result.update(
        {
            "average_household_size": round(household_persons / households, 4)
            if households
            else "",
            "children_under_15_pct": ratio(children, population),
            "persons_65_plus_pct": ratio(older, population),
            "one_person_households_pct": ratio(one_person, households),
            "one_parent_households_pct": ratio(one_parent, households),
            "employment_pct": ratio(employed, labour_total),
            "unemployment_pct": ratio(unemployed, labour_total),
            "retired_pct": ratio(retired, labour_total),
            "unable_to_work_pct": ratio(unable_to_work, labour_total),
            "third_level_education_pct": ratio(third_level, education_total),
            "low_education_pct": ratio(low_education, education_total),
            "occupied_dwellings_pct": ratio(occupied, housing_stock),
            "other_vacant_dwellings_pct": ratio(other_vacant, housing_stock),
            "holiday_homes_pct": ratio(holiday_homes, housing_stock),
            "house_or_bungalow_pct": ratio(house_bungalow, dwelling_total),
            "apartment_or_bedsit_pct": ratio(apartment, dwelling_total),
            "pre_2001_dwellings_pct": ratio(pre_2001, construction_total),
            "built_2016_or_later_pct": ratio(built_2016_later, construction_total),
            "owner_occupied_pct": ratio(owner_occupied, tenure_total),
            "private_rented_pct": ratio(private_rented, tenure_total),
            "social_rented_pct": ratio(social_rented, tenure_total),
            "oil_heating_pct": ratio(oil, heating_total),
            "gas_heating_pct": ratio(gas, heating_total),
            "electric_heating_pct": ratio(electricity, heating_total),
            "coal_or_peat_heating_pct": ratio(solid_fuel, heating_total),
            "no_central_heating_pct": ratio(no_central_heating, heating_total),
            "renewable_energy_pct": ratio(has_renewable, renewable_total),
        }
    )
    return result


def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError("Run download_small_area_census.py first.")
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with INPUT_FILE.open("r", encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        first = next(reader)
        if first["GUID"] == "IE0":
            raise ValueError("Unexpected national total before Small Area records.")
        first_result = transform(first)
        fieldnames = list(first_result)
        count = 0
        with OUTPUT_FILE.open("w", encoding="utf-8-sig", newline="") as target:
            writer = csv.DictWriter(target, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(first_result)
            count += 1
            for row in reader:
                if row["GUID"] == "IE0":
                    continue
                writer.writerow(transform(row))
                count += 1
    print(f"Small Areas processed: {count:,}")
    print(f"Processed file created: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
