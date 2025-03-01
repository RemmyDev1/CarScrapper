import tkinter as tk
from tkinter import messagebox

# Function to collect user input using tkinter forms
def get_user_input():
    root = tk.Tk()
    root.title("Car Search Input Form")

    # Set the background color
    root.configure(bg="#f0f8ff")  # Light azure background

    # Set the font styles
    title_font = ("Helvetica", 16, "bold")
    label_font = ("Helvetica", 12)

    # Title label
    title_label = tk.Label(root, text="Car Search Criteria", bg="#f0f8ff", font=title_font)
    title_label.grid(row=0, column=0, columnspan=2, pady=10)

    # Text Entry for Make
    make_label = tk.Label(root, text="Make:", bg="#f0f8ff", font=label_font)
    make_label.grid(row=1, column=0, sticky='e', padx=5, pady=5)

    make_entry = tk.Entry(root, width=30)
    make_entry.grid(row=1, column=1, padx=5, pady=5)

    # Text Entry for Model
    model_label = tk.Label(root, text="Model:", bg="#f0f8ff", font=label_font)
    model_label.grid(row=2, column=0, sticky='e', padx=5, pady=5)

    model_entry = tk.Entry(root, width=30)
    model_entry.grid(row=2, column=1, padx=5, pady=5)

    # Labels and entry field for zipcode
    zipcode_label = tk.Label(root, text="Zipcode:", bg="#f0f8ff", font=label_font)
    zipcode_label.grid(row=3, column=0, sticky='e', padx=5, pady=5)

    zipcode_entry = tk.Entry(root, width=30)
    zipcode_entry.grid(row=3, column=1, padx=5, pady=5)

    # Dropdown for Min Year
    min_year_label = tk.Label(root, text="Min Year:", bg="#f0f8ff", font=label_font)
    min_year_label.grid(row=4, column=0, sticky='e', padx=5, pady=5)

    min_year_options = [str(year) for year in range(2000, 2024)]
    selected_min_year = tk.StringVar(root)
    selected_min_year.set(min_year_options[0])
    min_year_menu = tk.OptionMenu(root, selected_min_year, *min_year_options)
    min_year_menu.grid(row=4, column=1, padx=5, pady=5)

    # Dropdown for Max Year
    max_year_label = tk.Label(root, text="Max Year:", bg="#f0f8ff", font=label_font)
    max_year_label.grid(row=5, column=0, sticky='e', padx=5, pady=5)

    max_year_options = [str(year) for year in range(2000, 2025)]
    selected_max_year = tk.StringVar(root)
    selected_max_year.set(max_year_options[-1])
    max_year_menu = tk.OptionMenu(root, selected_max_year, *max_year_options)
    max_year_menu.grid(row=5, column=1, padx=5, pady=5)

    # Dropdown for Min Price
    min_price_label = tk.Label(root, text="Min Price:", bg="#f0f8ff", font=label_font)
    min_price_label.grid(row=6, column=0, sticky='e', padx=5, pady=5)

    min_price_options = ["$0", "$2000", "$5000", "$10000", "$15000", "$20000", "$25000"]
    selected_min_price = tk.StringVar(root)
    selected_min_price.set(min_price_options[0])
    min_price_menu = tk.OptionMenu(root, selected_min_price, *min_price_options)
    min_price_menu.grid(row=6, column=1, padx=5, pady=5)

    # Dropdown for Max Price
    max_price_label = tk.Label(root, text="Max Price:", bg="#f0f8ff", font=label_font)
    max_price_label.grid(row=7, column=0, sticky='e', padx=5, pady=5)

    max_price_options = ["$2000", "$5000", "$10000", "$15000", "$20000", "$25000", "$30000", "$35000"]
    selected_max_price = tk.StringVar(root)
    selected_max_price.set(max_price_options[-1])
    max_price_menu = tk.OptionMenu(root, selected_max_price, *max_price_options)
    max_price_menu.grid(row=7, column=1, padx=5, pady=5)

    # Dropdown for Mileage
    mileage_label = tk.Label(root, text="Mileage:", bg="#f0f8ff", font=label_font)
    mileage_label.grid(row=8, column=0, sticky='e', padx=5, pady=5)

    mileage_options = ["15000", "30000", "45000", "60000", "75000",
                       "100000", "150000", "200000", "200000"]
    selected_mileage = tk.StringVar(root)
    selected_mileage.set(mileage_options[0])
    mileage_menu = tk.OptionMenu(root, selected_mileage, *mileage_options)
    mileage_menu.grid(row=8, column=1, padx=5, pady=5)

    # Dropdown for Radius
    radius_label = tk.Label(root, text="Radius (in miles):", bg="#f0f8ff", font=label_font)
    radius_label.grid(row=9, column=0, sticky='e', padx=5, pady=5)

    radius_options = ["50", "75", "100", "250"]
    selected_radius = tk.StringVar(root)
    selected_radius.set(radius_options[0])
    radius_menu = tk.OptionMenu(root, selected_radius, *radius_options)
    radius_menu.grid(row=9, column=1, padx=5, pady=5)

    # Initialize user_data as a list to collect inputs
    user_data = []

    # Function to submit the form
    def submit_form():
        nonlocal user_data  # Make user_data accessible in this scope
        # Gather input data
        user_data = {
            "zipcode": zipcode_entry.get(),
            "make": make_entry.get(),
            "model": model_entry.get(),
            "min_year": selected_min_year.get(),
            "max_year": selected_max_year.get(),
            "min_price": selected_min_price.get(),
            "max_price": selected_max_price.get(),
            "mileage": selected_mileage.get(),
            "radius": selected_radius.get()
        }

        # Perform basic validation
        if not user_data["zipcode"]:  # Check if zipcode is filled
            messagebox.showwarning("Input Error", "Please fill in the zipcode.")
        elif not user_data["make"]:  # Check if make is filled
            messagebox.showwarning("Input Error", "Please fill in the make.")
        elif not user_data["model"]:  # Check if model is filled
            messagebox.showwarning("Input Error", "Please fill in the model.")
        else:
            root.destroy()  # Close the Tkinter window after submission

    # Submit button
    submit_button = tk.Button(root, text="Submit", bg="#4CAF50", fg="white", font=label_font, command=submit_form)
    submit_button.grid(row=10, columnspan=2, pady=10)

    root.mainloop()

    return user_data  # Return the collected user data after the window is closed