import tkinter as tk
import requests
import os
import pandas as pd
from tkinter import messagebox, ttk
from bs4 import BeautifulSoup
import numpy as np
import subprocess
import tkinter.font as tkFont

# Ensure the df and subject_options are defined as in the initial setup
URL = "https://uiet.puchd.ac.in/?page_id=4119"
r = requests.get(URL)
soup = BeautifulSoup(r.content, 'html5lib')

subject_code_elements = soup.select("td.column-4")
subject_name_elements = soup.select("td.column-5")
year_elements = soup.select("td.column-6")

subject_code = np.array([element.get_text(strip=True) for element in subject_code_elements])
subject_name = np.array([element.get_text(strip=True) for element in subject_name_elements])
year = np.array([element.get_text(strip=True) for element in year_elements])

anchors = soup.find_all('a', class_= 'wp-block-button__link')
links = np.array([a['href'] for a in anchors if 'href' in a.attrs])

# Ensure all arrays have the same length by taking the minimum length
min_len = min(len(subject_code), len(subject_name), len(year), len(links))
subject_code = subject_code[:min_len]
subject_name = subject_name[:min_len]
year = year[:min_len]
links = links[:min_len]

df = pd.DataFrame({
    'Code': subject_code,
    'Subject_Name': subject_name,
    'p_year': year,
    "links": links
})

# Create a list of unique subject codes and names for the combobox
# Combine code and name for display in the listbox
subject_options = sorted(list(set([f"{code} - {name}" for code, name in zip(df['Code'].tolist(), df['Subject_Name'].tolist())])))

# Variable to store the after ID for hiding the listbox
hide_listbox_id = None


def open_downloads_folder():
    base_download_dir = "C:\\UIET PYQ Your downloads"
    if os.path.exists(base_download_dir):
        if os.name == 'nt':  # For Windows
            os.startfile(base_download_dir)
        elif os.uname().sysname == 'Darwin': # For macOS
            subprocess.call(['open', base_download_dir])
        else: # For other Unix-like systems
            subprocess.call(['xdg-open', base_download_dir])
    else:
        messagebox.showinfo("Folder Not Found", f"The folder '{base_download_dir}' does not exist yet.")

def download_papers_action():
    # Get input from the entry field
    search_term = subject_entry.get().strip()

    output_text.config(state=tk.NORMAL)
    output_text.delete('1.0', tk.END)
    output_text.insert(tk.END, f"Searching for papers with code or name: {search_term}\n")

    # Ensure the 'Code' and 'Subject_Name' columns in df contain strings for comparison
    # Perform case-insensitive search on the combined string first
    df['Combined'] = df['Code'].astype(str) + ' - ' + df['Subject_Name'].astype(str)
    matching_papers = df[df['Combined'].str.lower() == search_term.lower()].copy()

    # If no exact match on combined string, try matching code or name separately (case-insensitive)
    if matching_papers.empty:
         matching_papers = df[
            (df['Code'].astype(str).str.lower() == search_term.lower()) |
            (df['Subject_Name'].astype(str).str.lower() == search_term.lower())
        ].copy()

    # Drop the temporary 'Combined' column
    df.drop(columns=['Combined'], inplace=True)


    if matching_papers.empty:
        output_text.insert(tk.END, "No papers found for the entered subject code or name.\n")
    else:
        # Define the base download directory
        base_download_dir = "C:\\UIET PYQ Your downloads"

        # Safely get the directory name, handling potential issues if matching_papers is empty
        if not matching_papers.empty:
            # Use the subject name from the first matching paper for the directory name
            directory_name = matching_papers.iloc[0]['Subject_Name']
             # Sanitize directory name and create the full path
            sanitized_directory_name = "".join(x if x.isalnum() or x in [' ', '_', '-'] else "_" for x in directory_name).strip()
            sanitized_directory_name = sanitized_directory_name.replace(' ', '_')
            full_download_path = os.path.join(base_download_dir, sanitized_directory_name)

        else:
            # Handle the case where matching_papers is empty after the check (shouldn't happen with the check above, but for safety)
             full_download_path = base_download_dir # Default to base directory


        if not os.path.exists(full_download_path):
            os.makedirs(full_download_path)
            output_text.insert(tk.END, f"Directory '{full_download_path}' created.\n")
        else:
            output_text.insert(tk.END, f"Directory '{full_download_path}' already exists.\n")

        # Update the label with the save location
        save_location_label.config(text=f"Files are being saved to: {full_download_path}")


        for index, row in matching_papers.iterrows():
            paper_url = row['links']
            subject_name = row['Subject_Name']
            year = row['p_year']

            # Sanitize subject name for filename (replace spaces and special characters with underscores)
            sanitized_subject_name = "".join(x if x.isalnum() or x in [' ', '_', '-'] else "_" for x in subject_name).strip()
            sanitized_subject_name = sanitized_subject_name.replace(' ', '_')


            # Construct base filename
            base_filename = f"{sanitized_subject_name}_{year}"
            filename = f"{base_filename}.pdf"
            filepath = os.path.join(full_download_path, filename)

            # Handle duplicate filenames
            count = 1
            while os.path.exists(filepath):
                filename = f"{base_filename}_{count}.pdf"
                filepath = os.path.join(full_download_path, filename)
                count += 1

            try:
                response = requests.get(paper_url, stream=True) # Use stream=True for potentially large files
                response.raise_for_status()  # Raise an exception for bad status codes

                # Add a check for PDF content type (optional but good practice)
                if 'application/pdf' not in response.headers.get('Content-Type', ''):
                    output_text.insert(tk.END, f"Skipping {filename}: URL does not point to a PDF.\n")
                    continue

                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192): # Download in chunks
                        f.write(chunk)
                output_text.insert(tk.END, f"Downloaded and saved: {filename}\n")
            except requests.exceptions.RequestException as e:
                output_text.insert(tk.END, f"Failed to download {filename}: {e}\n")
            except Exception as e:
                output_text.insert(tk.END, f"An error occurred while processing {filename}: {e}\n")


    output_text.config(state=tk.DISABLED)

def filter_suggestions(event=None): # Allow event to be None for manual calls
    """Filters the subject_options based on the text in the subject_entry widget and updates the listbox, showing/hiding it."""
    search_term = subject_entry.get().strip()

    # Clear the current contents of the listbox
    subject_listbox.delete(0, tk.END)

    if not search_term:
        # If the entry is empty, insert all subject options
        options_to_display = subject_options
    else:
        # Filter subject_options based on case-insensitive search
        options_to_display = [
            item for item in subject_options
            if search_term.lower() in item.lower()
        ]

    # Insert the filtered options into the listbox
    for item in options_to_display:
        subject_listbox.insert(tk.END, item)

    # Show or hide the listbox based on results and focus
    if options_to_display and root.focus_get() == subject_entry:
        subject_listbox.grid()
    else:
        subject_listbox.grid_remove()


def on_listbox_select(event):
    """Populates the subject_entry with the selected item from the listbox and hides the listbox."""
    selected_indices = subject_listbox.curselection()
    if selected_indices:
        # Get the index of the first selected item
        index = selected_indices[0]
        # Get the text of the selected item
        selected_item = subject_listbox.get(index)
        # Clear the current content of the subject_entry
        subject_entry.delete(0, tk.END)
        # Insert the selected item text into the subject_entry
        subject_entry.insert(tk.END, selected_item)
        # Hide the listbox after selection
        subject_listbox.grid_remove()
        # Cancel the pending hide action if there is one
        global hide_listbox_id
        if hide_listbox_id:
            root.after_cancel(hide_listbox_id)
            hide_listbox_id = None


def hide_listbox_delayed():
    """Hides the listbox after a short delay."""
    subject_listbox.grid_remove()
    global hide_listbox_id
    hide_listbox_id = None # Clear the ID after hiding

def on_entry_focus_out(event):
    """Schedules the listbox to be hidden after a delay."""
    global hide_listbox_id
    if hide_listbox_id: # Cancel previous scheduled hide if exists
        root.after_cancel(hide_listbox_id)
    # Schedule hide after 200ms to allow clicking on the listbox
    hide_listbox_id = root.after(200, hide_listbox_delayed)

def on_entry_focus_in(event):
    """Shows the listbox if the entry is focused and there are suggestions (empty entry shows all)."""
    # Cancel any pending hide action
    global hide_listbox_id
    if hide_listbox_id:
        root.after_cancel(hide_listbox_id)
        hide_listbox_id = None
    # Update and potentially show the listbox immediately on focus
    filter_suggestions()


# Create the main application window
root = tk.Tk()
root.title("Past Year Paper Downloader")
root.geometry("600x450") # Increased height to accommodate author frame

# Define fonts and colors
BG_COLOR = "#e0f7fa"  # Light cyan background
FRAME_BG_COLOR = "#b2ebf2" # Cyan background for frames
BTN_COLOR = "#00796b" # Teal button
BTN_TEXT_COLOR = "#ffffff" # White button text
LABEL_COLOR = "#004d40" # Dark teal labels
TEXT_COLOR = "#000000" # Black text
ENTRY_BG = "#ffffff" # White entry background
LISTBOX_BG = "#ffffff" # White listbox background
LISTBOX_SELECT_BG = "#4dd0e1" # Light blue selection background
AUTHOR_FRAME_BG = "#80deea" # Lighter cyan for author frame

DEFAULT_FONT = tkFont.nametofont("TkDefaultFont")
DEFAULT_FONT.configure(size=10)
TITLE_FONT = tkFont.Font(family="Helvetica", size=14, weight="bold")
LABEL_FONT = tkFont.Font(family="Helvetica", size=10)
BUTTON_FONT = tkFont.Font(family="Helvetica", size=10, weight="bold")
TEXT_FONT = tkFont.Font(family="Consolas", size=9) # Monospace font for output

root.configure(bg=BG_COLOR)

# Create a main frame to hold all other frames
main_frame = tk.Frame(root, bg=FRAME_BG_COLOR)
main_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

# Configure grid weights for the main_frame to allow columns and rows to expand
main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_rowconfigure(0, weight=0)  # Input frame row - fixed height
main_frame.grid_rowconfigure(1, weight=0)  # Button frame row - fixed height
main_frame.grid_rowconfigure(2, weight=1)  # Listbox row - expands vertically
main_frame.grid_rowconfigure(3, weight=1)  # Output frame row - expands vertically
main_frame.grid_rowconfigure(4, weight=0)  # Save location label row - fixed height
main_frame.grid_rowconfigure(5, weight=0)  # Author frame row - fixed height


# Create a frame for the input widgets (Label and Entry)
input_frame = tk.Frame(main_frame, bg=FRAME_BG_COLOR)
input_frame.grid(row=0, column=0, pady=5, sticky="ew")  # Place input_frame in row 0 of main_frame

# Configure grid weights for the input_frame to make the Entry expand
input_frame.grid_columnconfigure(0, weight=0)  # Label column - fixed width
input_frame.grid_columnconfigure(1, weight=1)  # Entry column - expands horizontally


# Create a frame for the buttons
button_frame = tk.Frame(main_frame, bg=FRAME_BG_COLOR)
button_frame.grid(row=1, column=0, pady=10, sticky="ew")  # Place button_frame in row 1 of main_frame

# Configure grid weights for the button_frame to distribute space
button_frame.grid_columnconfigure(0, weight=1)  # Download button column - expands
button_frame.grid_columnconfigure(1, weight=1)  # View downloads button column - expands


# Create label and entry for subject code/name and place them in the input_frame using grid
subject_code_label = tk.Label(input_frame, text="Enter Subject Code or Name:", bg=FRAME_BG_COLOR, fg=LABEL_COLOR, font=LABEL_FONT)
subject_code_label.grid(row=0, column=0, padx=5, sticky="w")  # Place label in row 0, column 0 of input_frame

subject_entry = tk.Entry(input_frame, bg=ENTRY_BG, fg=TEXT_COLOR, font=DEFAULT_FONT)
subject_entry.grid(row=0, column=1, padx=5, sticky="ew")  # Place entry in row 0, column 1 of input_frame

# Create a Listbox for displaying suggestions and place it directly in the main_frame
subject_listbox = tk.Listbox(main_frame, height=10, bg=LISTBOX_BG, fg=TEXT_COLOR, font=DEFAULT_FONT, selectbackground=LISTBOX_SELECT_BG)  # height controls initial number of visible items
# Initially hide the listbox
subject_listbox.grid(row=2, column=0, padx=10, sticky="ew")  # Place listbox in row 2 of main_frame (below input and button frames)
subject_listbox.grid_remove() # Hide it initially


# Create the download button and place it in the button_frame using grid
download_button = tk.Button(button_frame, text="Download Papers", command=download_papers_action, bg=BTN_COLOR, fg=BTN_TEXT_COLOR, font=BUTTON_FONT, relief=tk.RAISED)
download_button.grid(row=0, column=0, padx=5, sticky="e")  # Place download button in row 0, column 0 of button_frame

# Create the "View Downloads" button and place it in the button_frame using grid
view_downloads_button = tk.Button(button_frame, text="View Downloads", command=open_downloads_folder, bg=BTN_COLOR, fg=BTN_TEXT_COLOR, font=BUTTON_FONT, relief=tk.RAISED)
view_downloads_button.grid(row=0, column=1, padx=5, sticky="w")  # Place view downloads button in row 0, column 1 of button_frame


# Create a frame for the output text widget and scrollbar
output_frame = tk.Frame(main_frame, bg=FRAME_BG_COLOR)
output_frame.grid(row=3, column=0, pady=5, sticky="nsew")  # Place output_frame in row 3 of main_frame

# Configure grid weights for the output_frame to make the text widget expand
output_frame.grid_columnconfigure(0, weight=1)  # Text widget column - expands horizontally
output_frame.grid_columnconfigure(1, weight=0)  # Scrollbar column - fixed width
output_frame.grid_rowconfigure(0, weight=1)  # Text widget row - expands vertically


# Label to display save location and place it in the main_frame using grid
save_location_label = tk.Label(main_frame, text="", bg=FRAME_BG_COLOR, fg=LABEL_COLOR, font=LABEL_FONT)
save_location_label.grid(row=4, column=0, pady=5, sticky="w")  # Place save location label in row 4 of main_frame


# Create a Text widget for displaying output and place it in the output_frame using grid
output_text = tk.Text(output_frame, height=10, state=tk.DISABLED, bg="#e0e0e0", fg=TEXT_COLOR, font=TEXT_FONT) # Added background color
output_text.grid(row=0, column=0, sticky="nsew")  # Place output_text in row 0, column 0 of output_frame


# Add a scrollbar to the Text widget and place it in the output_frame using grid
scrollbar = tk.Scrollbar(output_frame, command=output_text.yview)
scrollbar.grid(row=0, column=1, sticky="ns")  # Place scrollbar in row 0, column 1 of output_frame
output_text['yscrollcommand'] = scrollbar.set

# Create a frame for the author attribution at the bottom
author_frame = tk.Frame(main_frame, bg=AUTHOR_FRAME_BG)
author_frame.grid(row=5, column=0, pady=5, sticky="ew") # Place author_frame in row 5 of main_frame
author_frame.grid_columnconfigure(0, weight=1) # Allow column to expand

# Add author name label
author_label = tk.Label(author_frame, text="Created by - Ayushmann Aggarwal", bg=AUTHOR_FRAME_BG, fg=LABEL_COLOR, font=LABEL_FONT)
author_label.pack(pady=2) # Use pack to center within the author_frame


# Bind the filter_suggestions function to the KeyRelease event on the entry widget
subject_entry.bind('<KeyRelease>', filter_suggestions)

# Bind focus events for showing/hiding the listbox
subject_entry.bind('<FocusIn>', on_entry_focus_in)
subject_entry.bind('<FocusOut>', on_entry_focus_out)


# Bind the on_listbox_select function to the ListboxSelect event on the listbox
subject_listbox.bind('<<ListboxSelect>>', on_listbox_select)


# Initially populate the listbox with all options (this is done within filter_suggestions when the entry is empty)
# filter_suggestions() # No need to call explicitly, FocusIn will handle it


# Run the Tkinter event loop
root.mainloop()