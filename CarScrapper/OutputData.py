import datetime
import pandas as pd
import xlsxwriter


def clean_and_process_data(df, criteria, site_name):

    df["price"] = df["price"].str.strip().str.replace("$", "", regex=False).str.replace(",", "", regex=False)
    print("Raw prices before conversion:", df["price"].unique())  # Debugging output

    try:
        df["price"] = pd.to_numeric(df["price"], errors="raise")
    except ValueError as e:
        print(f"Error converting price: {e}")

    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["price"] = df["price"].fillna(0).astype(int)
    print("Cleaned prices:", df["price"].head())

    df["mileage"] = df["mileage"].str.strip().str.replace(",", "", regex=False).str.replace(" miles", "", regex=False)
    print("Raw mileage before conversion:", df["mileage"].unique())


    try:
        df["mileage"] = pd.to_numeric(df["mileage"], errors="raise")
    except ValueError as e:
        print(f"Error converting mileage: {e}")

    df["mileage"] = df["mileage"].astype(str).str.replace(" mi.", "", regex=False)
    df["mileage"] = pd.to_numeric(df["mileage"], errors="coerce")
    df["mileage"] = df["mileage"].fillna(0).astype(int)


    df["distance"] = df["distance"].str.strip().str.replace(" mi. away", "", regex=False).str.replace(",", "", regex=False)
    print("Raw distances before conversion:", df["distance"].unique())


    try:
        df["distance"] = pd.to_numeric(df["distance"], errors="raise")
    except ValueError as e:
        print(f"Error converting distance: {e}")


    df["distance"] = pd.to_numeric(df["distance"], errors="coerce")

    df["distance"] = df["distance"].fillna(0).astype(float).astype(int)



    now = datetime.datetime.now()
    df["year"] = now.year
    df["miles_pa"] = df.apply(
        lambda row: row["mileage"] / (now.year - row["year"]) if (now.year - row["year"]) > 0 else 0, axis=1
    )
    df["miles_pa"] = df["miles_pa"].replace([float('inf'), -float('inf')], 0).fillna(0).astype(int)


    df = df[df["price"] < int(criteria["price_to"])]

    if site_name == "autotrader":
        df["link"] = "https://www.autotrader.com" + df["link"]
    elif site_name == "cars":
        df["link"] = "https://www.cars.com" + df["link"]

    return df


def apply_conditional_formatting(worksheet):

    worksheet.conditional_format("C2:C1000", {
        'type': '3_color_scale',
        'min_color': '#63be7b',
        'mid_color': '#ffdc81',
        'max_color': '#f96a6c'
    })
    worksheet.conditional_format("D2:D1000", {
        'type': '3_color_scale',
        'min_color': '#63be7b',
        'mid_color': '#ffdc81',
        'max_color': '#f96a6c'
    })
    worksheet.conditional_format("E2:E1000", {
        'type': '3_color_scale',
        'min_color': '#63be7b',
        'mid_color': '#ffdc81',
        'max_color': '#f96a6c'
    })
    worksheet.conditional_format("F2:F1000", {
        'type': '3_color_scale',
        'min_color': '#63be7b',
        'mid_color': '#ffdc81',
        'max_color': '#f96a6c'
    })


def output_data_to_excel(data, criteria, site_name):
    df = pd.DataFrame(data)
    print(df)
    if df.empty:
        print(f"No data to save for {site_name}. Skipping file creation.")
        return

    df = clean_and_process_data(df, criteria, site_name)

    df = df[["name", "link", "price", "mileage", "distance", "miles_pa"]]

    output_file = f"{site_name}.xlsx"

    try:
        with pd.ExcelWriter(output_file, engine="xlsxwriter") as writer:
            df.to_excel(writer, sheet_name=site_name, index=False)

            workbook = writer.book
            worksheet = writer.sheets[site_name]

            apply_conditional_formatting(worksheet)

            print(f"Output saved to current directory as '{output_file}'.")

    except Exception as e:
        print(f"Error saving Excel file: {e}")
