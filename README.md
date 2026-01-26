# iNat Barcode Generator

> ⚠️ **EARLY BETA** - This project is in early beta and additional testing is required. Please report any issues or unexpected behavior on GitHub.

A Python GUI tool that creates ["movie barcode"](https://pypi.org/project/movie-barcodes/) style visualizations from iNaturalist observation data. The tool downloads images from CSV exports and converts them into a color-based barcode where each pixel represents the average color of an image.

## Example

![Example Barcode](output%20example.png)

*A sample barcode generated from iNaturalist observations*

## Features

- 🎨 **GUI Interface** - User-friendly dark theme with intuitive controls
- 📊 **Customizable Dimensions** - Set image height and width (or auto-calculate based on image count)
- 🖼️ **Automatic Image Processing** - Downloads images and extracts average colors
- 📈 **Progress Tracking** - Real-time progress bar with failed image count
- ⚠️ **Large Dataset Warning** - Alerts user when processing >1000 images
- ⚡ **Quick Actions** - Enter key shortcut to generate, Open File button to view results
- 🛑 **Cancel Operation** - Stop processing at any time
- 📝 **Auto-detection** - Automatically finds observation CSVs in the current directory
- 🎯 **Image Preview** - Shows image count from CSV before processing

## Installation

### Prerequisites
- Python 3.7 or higher

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/inat-barcode-generator.git
cd inat-barcode-generator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the script:
```bash
python inat_barcode_gui.py
```

2. The GUI will open with the following fields:
   - **CSV File Path** - Select your iNaturalist observations CSV export
   - **Images** - Displays the number of images in the CSV
   - **Image Height** - Height of the output barcode in pixels (default: 500)
   - **Image Width** - Width in pixels (default: auto = number of images)
   - **Output File Name** - Name for the generated image (auto-timestamped)
   - **Output Directory** - Where to save the barcode image

3. Click **Generate Barcode** or press **Enter** to start processing

4. Monitor progress with the progress bar and status updates

5. Click **Open File** to view the generated barcode, or **Cancel** to stop at any time

## Getting iNaturalist CSV Data

1. Visit [iNaturalist.org](https://www.inaturalist.org)
2. Filter observations (by location, taxa, date range, etc.)
3. Click **Export** and select **CSV**
4. Save the file in your working directory

## How It Works

1. **Reads CSV** - Loads observation data with image URLs
2. **Downloads Images** - Fetches each image from the URLs
3. **Extracts Colors** - Calculates the average RGB color of each image
4. **Creates Barcode** - Renders vertical colored lines, one per image
5. **Exports Image** - Saves as PNG to your selected directory

Each vertical line's color represents the average color of that observation's image, creating a unique visual "barcode" of your observations.

## Requirements

- `numpy` - Numerical computing
- `pandas` - CSV data handling
- `requests` - HTTP image downloads
- `pillow` - Image generation
- `tqdm` - Progress bars (optional, for terminal versions)

## Features in Detail

### Auto-sizing
- Set Image Width to "auto" to have width equal the number of images (default)
- Each image gets 1 pixel of width by default

### Error Handling
- Shows count of failed downloads during processing
- Continues processing even if some images fail to download
- Displays final summary with success count

### Large Dataset Protection
- Warns if processing >1000 images to prevent accidental long processing times
- Allows you to cancel and use a smaller dataset

### Keyboard Shortcuts
- **Enter** - Generate barcode
- **Ctrl+C** - Force quit (in terminal)

## Troubleshooting

**"Module not found" errors**
- Install missing modules: `pip install -r requirements.txt`

**Images not downloading**
- Check internet connection
- Verify CSV has valid image URLs

**Processing is slow**
- Large datasets (>1000 images) take considerable time
- Try processing a smaller date range or location filter

**Output image is blank/wrong colors**
- Verify the Image Height setting (min ~50 pixels recommended)
- Check that images in the CSV are accessible

## License

MIT License - See LICENSE file for details

## Contributing

Contributions welcome! Feel free to submit issues or pull requests.

## Author

Created for iNaturalist observation analysis


