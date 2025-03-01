import datetime
import pandas as pd
import xlsxwriter


def clean_and_process_data(df, criteria, site_name):
    """Clean and process the data to prepare it for Excel output."""

    # Clean and convert price
    df["price"] = df["price"].str.strip().str.replace("$", "", regex=False).str.replace(",", "", regex=False)
    print("Raw prices before conversion:", df["price"].unique())  # Debugging output

    # Try converting prices and handle errors
    try:
        df["price"] = pd.to_numeric(df["price"], errors="raise")  # Raise an error for problematic values
    except ValueError as e:
        print(f"Error converting price: {e}")

    # Afte  r cleaning, fill NaN and convert to integers
    df["price"] = df["price"].fillna(0).astype(int)
    print("Cleaned prices:", df["price"].head())  # Debugging output

    # Clean and convert mileage
    df["mileage"] = df["mileage"].str.strip().str.replace(",", "", regex=False).str.replace(" mi.", "", regex=False).str.replace(" miles", "", regex=False)
    print("Raw mileage before conversion:", df["mileage"].unique())  # Debugging output

    # Try converting mileage and handle errors
    try:
        df["mileage"] = pd.to_numeric(df["mileage"], errors="raise")
    except ValueError as e:
        print(f"Error converting mileage: {e}")
    try:
        if df["mileage"] == 'Mileage not available':
            df["mileage"] = '0'
    except ValueError as e:
        print(f"milage is correct")

    df["mileage"] = df["mileage"].fillna(0).astype(int)
    print("Cleaned mileage:", df["mileage"].head())  # Debugging output

    # Clean and convert distance
    df["distance"] = df["distance"].str.strip().str.replace(" mi. away", "", regex=False).str.replace(",", "", regex=False)
    print("Raw distances before conversion:", df["distance"].unique())  # Debugging output

    # Try converting distances and handle errors
    try:
        df["distance"] = pd.to_numeric(df["distance"], errors="raise")
    except ValueError as e:
        print(f"Error converting distance: {e}")

    df["distance"] = df["distance"].fillna(0).astype(int)
    print("Cleaned distances:", df["distance"].head())  # Debugging output

    # Add current year and calculate miles per annum
    now = datetime.datetime.now()
    df["year"] = now.year
    df["miles_pa"] = df.apply(
        lambda row: row["mileage"] / (now.year - row["year"]) if (now.year - row["year"]) > 0 else 0, axis=1
    )
    df["miles_pa"] = df["miles_pa"].replace([float('inf'), -float('inf')], 0).fillna(0).astype(int)

    # Filter based on price criteria
    df = df[df["price"] < int(criteria["price_to"])]

    # Add the website link prefix for consistency
    if site_name == "Carvana":
        df["link"] = "https://www.carvana.com" + df["link"]
    elif site_name == "cars":
        df["link"] = "https://www.cars.com" + df["link"]

    return df


def apply_conditional_formatting(worksheet):
    """Apply conditional formatting to the worksheet."""
    # Apply conditional formatting for price, mileage, distance, and miles per annum
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
    """Output cleaned data to Excel."""
    df = pd.DataFrame(data)
    print(df)
    # Clean and process data
    df = clean_and_process_data(df, criteria, site_name)

    # Select columns to write to Excel
    df = df[["name", "link", "price", "mileage", "distance", "miles_pa"]]

    # Define output file name based on site name
    output_file = f"{site_name}.xlsx"

    try:
        with pd.ExcelWriter(output_file, engine="xlsxwriter") as writer:
            df.to_excel(writer, sheet_name=site_name, index=False)

            # Access the workbook and worksheet
            workbook = writer.book
            worksheet = writer.sheets[site_name]

            # Apply conditional formatting
            apply_conditional_formatting(worksheet)

            print(f"Output saved to current directory as '{output_file}'.")

    except Exception as e:
        print(f"Error saving Excel file: {e}")