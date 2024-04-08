
<!-- Big Endian -->

# PNGHide: PNG Data Hider & Revealer

<p align="center">
  <img src="./assets/image.jpeg" width="200" alt="PNGHide Logo">
</p>


PNGHide is a simple tool designed for hiding and extracting data within PNG files securely and effortlessly using Python.

## Features

- **Data Hiding**: Embed images or text into PNG files, concealing sensitive information within innocuous images.
- **Data Extraction**: Extract hidden data from PNG files, unveiling concealed information with precision.
- **Secure Encryption**: Utilize cryptographic encryption for secure hiding and extraction of data.
- **User-Friendly Interface**: Intuitive command-line interface (CLI) and graphical user interface (GUI) for seamless data manipulation.



## Dependencies

- Python 3.x
- Tkinter (Python's standard GUI library)

## Installation

1. Clone or download the repository to your local machine.
2. Ensure you have Python installed on your system.
3. Install dependencies, simply run :
```bash
pip install -r requirements.txt
```


## Setup

Before using PNGHide, you need to specify the encryption key directly in the `main.py` script.

### Setting Encryption Key

1. Open the `main.py` file in a text editor.
2. Locate the `KEY` variable in the script.
3. Replace the current value of the `KEY` variable with your desired encryption key.



## Usage

### Command Line Usage


#### Embedding Data

Embedding an image file into a PNG file:

```bash
python main.py embed --input input_image.png --output output_image.png --file data_to_hide.png
```

Embedding a text file into a PNG file:

```bash
python main.py embed --input input_image.png --output output_image.png --file data_to_hide.txt
```


#### Extracting Data

Extracting hidden data from a PNG file:
```bash
python main.py extract --input input_image.png --output extracted_data
```


### GUI Usage

1. Execute the `gui.py` script:
2. Click on the "Embed Data" button to hide data within a PNG file or the "Extract Data" button to reveal hidden data.
3. Follow the intuitive prompts in the GUI to select input and output files and specify the type of data you're hiding (for embedding).



<p align="center">
  <table>
  <tr>
    <td> <img src="./assets/PNGHide 1.png" alt="First Image" width="400" /> </td>
    <td> <img src="./assets/PNGHide 2.png" alt="Second Image" width="400" /> </td>
  </tr>
  </table>
</p>



## References

If you found this project useful, consider referencing the following resources:

- [PNG file format specification](http://www.libpng.org/pub/png/spec/1.2/PNG-Contents.html): Reference for understanding the structure of PNG files.
