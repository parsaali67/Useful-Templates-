import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def load_data():
    """
    Opens a file dialog for the user to select a CSV file and loads it into a DataFrame.
    The CSV should contain at least "Date" and "Cases" columns.
    """
    file_path = filedialog.askopenfilename(
        filetypes=[("CSV files", "*.csv")]
    )
    if file_path:
        try:
            df = pd.read_csv(file_path)
            if 'Date' not in df.columns or 'Cases' not in df.columns:
                messagebox.showerror(
                    "Error",
                    "CSV must contain 'Date' and 'Cases' columns."
                )
                return None
            df['Date'] = pd.to_datetime(df['Date'])
            df.sort_values('Date', inplace=True)
            return df
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Failed to load CSV file:\n{e}"
            )
            return None
    return None


def plot_data(df):
    """
    Creates a Matplotlib figure plotting 'Cases' over time.
    """
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(df['Date'], df['Cases'], marker='o', linestyle='-')
    ax.set_title("COVID-19 Cases Over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("Number of Cases")
    fig.autofmt_xdate()
    return fig


def display_plot(root, fig):
    """
    Embeds the given Matplotlib figure into the Tkinter window.
    """
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(
        side=tk.TOP, fill=tk.BOTH, expand=True
    )


def on_load(root):
    """
    Handler for the 'Load CSV Data' button. Loads data and displays the plot if successful.
    """
    df = load_data()
    if df is not None:
        fig = plot_data(df)
        display_plot(root, fig)


def main():
    # Create the main window
    root = tk.Tk()
    root.title("Interactive Data Dashboard")

    # Create a frame for the controls
    control_frame = tk.Frame(root)
    control_frame.pack(side=tk.TOP, pady=10)

    # Button to load CSV data
    load_button = tk.Button(
        control_frame,
        text="Load CSV Data",
        command=lambda: on_load(root)
    )
    load_button.pack()

    # Start the Tkinter main loop
    root.mainloop()


if __name__ == "__main__":
    main()
