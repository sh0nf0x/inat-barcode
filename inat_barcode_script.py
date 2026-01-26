import sys
import subprocess

# Install required packages if not already installed
required_packages = {
    'tkinter': 'tk',
    'numpy': 'numpy',
    'pandas': 'pandas',
    'requests': 'requests',
    'PIL': 'pillow',
    'tqdm': 'tqdm'
}

for package, pip_name in required_packages.items():
    try:
        __import__(package)
    except ImportError:
        print(f"Installing {pip_name}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", pip_name])

import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import os
import numpy as np
import pandas as pd
import requests
from PIL import Image, ImageDraw
import time
from io import BytesIO
from tqdm import tqdm
import threading
import glob
from datetime import datetime
import subprocess as sp
import platform

class BarcodeGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("iNat Barcode Generator")
        self.root.configure(bg="#333333")
        self.cancel_flag = False
        self.last_output_path = None
        self.cancel_flag = False
        self.last_output_path = None
        
        # Find observations-*.csv files
        observations_files = glob.glob("observations-*.csv")
        default_csv = observations_files[0] if observations_files else ""
        
        # Title
        tk.Label(root, text="iNat Barcode Generator", font=("Arial", 16, "bold"), bg="#333333", fg="#74AC00").grid(row=0, column=0, columnspan=3, pady=15)
        
        # CSV File Path
        tk.Label(root, text="CSV File Path:", font=("Arial", 10, "bold"), bg="#333333", fg="white").grid(row=1, column=0, sticky="w", padx=10, pady=10)
        self.csv_path_var = tk.StringVar(value=default_csv)
        tk.Entry(root, textvariable=self.csv_path_var, width=40).grid(row=1, column=1, padx=10, pady=10)
        tk.Button(root, text="Browse", command=self.browse_csv, bg="#74AC00", fg="black", font=("Arial", 9, "bold")).grid(row=1, column=2, padx=5, pady=10, sticky="w")
        
        # Image Count Preview
        tk.Label(root, text="Images:", font=("Arial", 9), bg="#333333", fg="white").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.image_count_var = tk.StringVar(value="None selected")
        tk.Label(root, textvariable=self.image_count_var, font=("Arial", 9, "bold"), bg="#333333", fg="#74AC00").grid(row=2, column=1, sticky="w", padx=10, pady=5)
        
        # Image Height
        tk.Label(root, text="Image Height (pixels):", font=("Arial", 10, "bold"), bg="#333333", fg="white").grid(row=3, column=0, sticky="w", padx=10, pady=10)
        self.height_var = tk.StringVar(value="500")
        tk.Entry(root, textvariable=self.height_var, width=40).grid(row=3, column=1, padx=10, pady=10)
        
        # Image Width
        tk.Label(root, text="Image Width (pixels):", font=("Arial", 10, "bold"), bg="#333333", fg="white").grid(row=4, column=0, sticky="w", padx=10, pady=10)
        self.width_var = tk.StringVar(value="auto")
        tk.Entry(root, textvariable=self.width_var, width=40).grid(row=4, column=1, padx=10, pady=10)
        
        # Helper text for Image Width
        tk.Label(root, text="(Leave as 'auto' to match number of images)", font=("Arial", 8, "italic"), bg="#333333", fg="#CCCCCC").grid(row=5, column=0, columnspan=2, sticky="w", padx=10, pady=5)
        
        # Output File Name
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        tk.Label(root, text="Output File Name:", font=("Arial", 10, "bold"), bg="#333333", fg="white").grid(row=6, column=0, sticky="w", padx=10, pady=10)
        self.output_var = tk.StringVar(value=f"inat_barcode_{timestamp}.png")
        tk.Entry(root, textvariable=self.output_var, width=40).grid(row=6, column=1, padx=10, pady=10)
        
        # Output Directory
        tk.Label(root, text="Output Directory:", font=("Arial", 10, "bold"), bg="#333333", fg="white").grid(row=7, column=0, sticky="w", padx=10, pady=10)
        self.output_dir_var = tk.StringVar(value=os.getcwd())
        tk.Entry(root, textvariable=self.output_dir_var, width=40).grid(row=7, column=1, padx=10, pady=10)
        tk.Button(root, text="Browse", command=self.browse_output_dir, bg="#74AC00", fg="black", font=("Arial", 9, "bold")).grid(row=7, column=2, padx=5, pady=10, sticky="w")
        
        # Generate Button
        tk.Button(root, text="Generate Barcode", command=self.generate_barcode, bg="#74AC00", fg="black", font=("Arial", 12, "bold")).grid(row=8, column=0, columnspan=3, pady=20, padx=10, sticky="ew")
        
        # Status Label
        self.status_var = tk.StringVar(value="Ready")
        tk.Label(root, textvariable=self.status_var, font=("Arial", 9), fg="#00FF00", bg="#333333").grid(row=9, column=0, columnspan=3, padx=10, pady=10)
        
        # Progress Bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(root, variable=self.progress_var, maximum=100, length=400)
        self.progress_bar.grid(row=10, column=0, columnspan=3, padx=10, pady=10, sticky="ew")
        
        # Cancel and Open File buttons frame
        self.button_frame = tk.Frame(root, bg="#333333")
        self.button_frame.grid(row=11, column=0, columnspan=3, padx=10, pady=10)
        
        self.cancel_button = tk.Button(self.button_frame, text="Cancel", command=self.cancel_operation, bg="#FF6B6B", fg="black", font=("Arial", 10, "bold"), state="disabled")
        self.cancel_button.pack(side="left", padx=5)
        
        self.open_button = tk.Button(self.button_frame, text="Open File", command=self.open_last_file, bg="#74AC00", fg="black", font=("Arial", 10, "bold"), state="disabled")
        self.open_button.pack(side="left", padx=5)
        
        # Auto-size window to fit all content
        root.update_idletasks()
        root.geometry("")
        
        # Bind Enter key to generate
        root.bind('<Return>', lambda e: self.generate_barcode())
        root.bind('<Return>', lambda e: self.generate_barcode())
    
    def browse_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if file_path:
            self.csv_path_var.set(file_path)
            self.update_image_count()
    
    def update_image_count(self):
        csv_path = self.csv_path_var.get()
        if not csv_path or not os.path.exists(csv_path):
            self.image_count_var.set("None selected")
            return
        
        try:
            df = pd.read_csv(csv_path)
            num_images = len(df)
            self.image_count_var.set(f"{num_images} images")
        except Exception as e:
            self.image_count_var.set(f"Error: {str(e)[:20]}")
            self.update_image_count()
    
    def update_image_count(self):
        csv_path = self.csv_path_var.get()
        if not csv_path or not os.path.exists(csv_path):
            self.image_count_var.set("None selected")
            return
        
        try:
            df = pd.read_csv(csv_path)
            num_images = len(df)
            
            # Display count and warn if >1000
            if num_images > 1000:
                self.image_count_var.set(f"{num_images} images ⚠️")
                messagebox.showwarning("Large Dataset", f"This CSV contains {num_images} images.\n\nProcessing may take a significant amount of time. Consider using a smaller dataset for testing.")
            else:
                self.image_count_var.set(f"{num_images} images")
        except Exception as e:
            self.image_count_var.set(f"Error: {str(e)[:20]}")
            self.update_total_width()
    
    def browse_output_dir(self):
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.output_dir_var.set(directory)
    
    def cancel_operation(self):
        self.cancel_flag = True
        self.status_var.set("Cancelling...")
        self.root.update()
    
    def open_last_file(self):
        if self.last_output_path and os.path.exists(self.last_output_path):
            try:
                if platform.system() == 'Windows':
                    os.startfile(self.last_output_path)
                elif platform.system() == 'Darwin':  # macOS
                    sp.Popen(['open', self.last_output_path])
                else:  # Linux
                    sp.Popen(['xdg-open', self.last_output_path])
            except Exception as e:
                messagebox.showerror("Error", f"Could not open file: {str(e)}")
    
    def browse_output_dir(self):
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.output_dir_var.set(directory)
    
    def generate_barcode(self):
        # Reset cancel flag and enable cancel button
        self.cancel_flag = False
        self.cancel_button.config(state="normal")
        self.open_button.config(state="disabled")
        self.progress_var.set(0)
        
        # Validate inputs
        csv_path = self.csv_path_var.get()
        if not csv_path:
            messagebox.showerror("Error", "Please select a CSV file.")
            return
        
        if not os.path.exists(csv_path):
            messagebox.showerror("Error", f"CSV file not found: {csv_path}")
            return
        
        try:
            height = int(self.height_var.get())
        except ValueError:
            messagebox.showerror("Error", "Image height must be a number.")
            return
        
        width_input = self.width_var.get().strip()
        if width_input.lower() == "auto":
            width = None
        else:
            try:
                width = int(width_input)
            except ValueError:
                messagebox.showerror("Error", "Image width must be a number or 'auto'.")
                return
        
        output_path = self.output_var.get()
        if not output_path.endswith(".png"):
            output_path += ".png"
        
        output_dir = self.output_dir_var.get()
        if not os.path.exists(output_dir):
            messagebox.showerror("Error", f"Output directory does not exist: {output_dir}")
            return
        
        full_output_path = os.path.join(output_dir, output_path)
        
        # Run in separate thread to avoid freezing GUI
        thread = threading.Thread(target=self._generate_barcode_worker, args=(csv_path, height, width, full_output_path))
        thread.start()
    
    def _generate_barcode_worker(self, csv_path, height, width, output_path):
        try:
            self.status_var.set("Loading CSV...")
            self.root.update()
            
            # Read the CSV file
            df = pd.read_csv(csv_path)
            
            # Replace "medium" with "square" in URLs
            df['image_url'] = df['image_url'].str.replace('medium', 'square')
            
            # Extract image URLs
            image_urls = df['image_url'].tolist()
            self.status_var.set(f"Processing {len(image_urls)} images...")
            self.root.update()
            
            # Initialize list for RGB values and failed count
            avg_rgb_values = []
            failed_count = 0
            
            # Process each image
            for idx, image_url in enumerate(image_urls):
                # Check if cancel was requested
                if self.cancel_flag:
                    self.status_var.set("Cancelled by user")
                    self.cancel_button.config(state="disabled")
                    self.root.update()
                    return
                
                try:
                    response = requests.get(image_url)
                    image = Image.open(BytesIO(response.content))
                    image_array = np.array(image)
                    avg_rgb = np.mean(image_array, axis=(0, 1)).astype(int)
                    avg_rgb_values.append(avg_rgb)
                except Exception as e:
                    failed_count += 1
                    continue
                
                # Update progress bar
                progress = ((idx + 1) / len(image_urls)) * 100
                self.progress_var.set(progress)
                self.status_var.set(f"Processing images: {idx + 1}/{len(image_urls)} (Failed: {failed_count})")
                self.root.update()
            
            # Determine image dimensions
            image_width = width if width is not None else len(image_urls)
            image_height = height
            
            # Create new image
            self.status_var.set("Creating composite image...")
            self.root.update()
            
            new_image = Image.new('RGB', (image_width, image_height))
            draw = ImageDraw.Draw(new_image)
            
            # Draw vertical lines
            for i, rgb in enumerate(avg_rgb_values):
                if i < image_width:
                    draw.line([(i, 0), (i, image_height)], fill=tuple(rgb), width=1)
            
            # Save the image
            new_image.save(output_path)
            
            absolute_path = os.path.abspath(output_path)
            directory = os.path.dirname(absolute_path)
            self.last_output_path = absolute_path
            
            self.progress_var.set(100)
            if failed_count > 0:
                self.status_var.set(f"Success! {len(avg_rgb_values)} images processed, {failed_count} failed. Saved to {directory}")
            else:
                self.status_var.set(f"Success! All {len(avg_rgb_values)} images processed. Saved to {directory}")
            self.cancel_button.config(state="disabled")
            self.open_button.config(state="normal")
            self.root.update()
            
        except Exception as e:
            self.status_var.set("Error occurred")
            self.cancel_button.config(state="disabled")
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    gui = BarcodeGeneratorGUI(root)
    root.mainloop()
