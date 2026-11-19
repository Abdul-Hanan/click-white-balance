# click-white-balance

Applies simple white balancing based on a reference pixel to correct image colors.

This project demonstrates a basic global white balancing technique. It generates a synthetic image with a color cast, simulates a user picking a "white" reference pixel, and then corrects the entire image's color balance based on that reference, saving both the original and corrected results.

## Features

*   Generates a synthetic test image with a warm color tint.
*   Simulates the user's perception of a "white" pixel by pre-defining its coordinates.
*   Applies a global color correction (white balance) by scaling BGR channels.
*   Outputs both the original and corrected images as PNG files.
*   Runs entirely non-interactively, without any GUI or display windows.

## How to Run

1.  **Clone the repository (or save the files):**
    If this were a repo, you'd clone it. For this submission, ensure `main.py`, `requirements.txt`, and `README.md` are in the same directory.

2.  **Install dependencies:**
    It's recommended to use a virtual environment.
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

3.  **Run the script:**
    ```bash
    python main.py
    ```

## Output

The script will generate two image files in the same directory:
*   `original_image.png`: The initial synthetic image with the color cast.
*   `corrected_image.png`: The image after applying white balance correction.

The console output will provide details about the process, including the reference pixel's BGR values before and after correction, and the scaling factors used.