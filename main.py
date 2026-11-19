import cv2
import numpy as np
import os

def generate_test_image(width=600, height=400):
    """
    Generates a synthetic image with a simulated warm color cast and a
    designated 'white' patch for reference.

    Args:
        width (int): Width of the generated image.
        height (int): Height of the generated image.

    Returns:
        tuple: A tuple containing:
            - np.ndarray: The generated BGR image.
            - tuple: (x, y) coordinates of the reference 'white' pixel.
    """
    img = np.zeros((height, width, 3), dtype=np.uint8)

    # Base background color: slightly yellowish/warm BGR (Blue, Green, Red)
    # This color has more Red than Green, and more Green than Blue, simulating a warm tint.
    base_b = 100
    base_g = 160
    base_r = 200
    img[:, :] = (base_b, base_g, base_r)  # Fill with base color

    # "White" patch: also warm-tinted, but meant to be perceived as white.
    # Its BGR values are higher but still maintain the yellowish tint (R > G > B).
    patch_b = 180
    patch_g = 210
    patch_r = 230

    patch_size = 100
    start_x = (width - patch_size) // 2
    end_x = start_x + patch_size
    start_y = (height - patch_size) // 2
    end_y = start_y + patch_size

    img[start_y:end_y, start_x:end_x] = (patch_b, patch_g, patch_r)

    # Define the "white" reference pixel coordinates (center of the patch)
    reference_pixel_coords = (start_x + patch_size // 2, start_y + patch_size // 2)

    return img, reference_pixel_coords

def apply_white_balance(image, reference_pixel_coords):
    """
    Applies a global white balance correction to an image based on a reference pixel.
    The reference pixel's BGR channels are scaled so they all become equal to their average.
    This same scaling is then applied to all pixels in the image.

    Args:
        image (np.ndarray): The input BGR image (uint8).
        reference_pixel_coords (tuple): (x, y) coordinates of the pixel perceived as white.

    Returns:
        np.ndarray: The white-balanced BGR image (uint8).
    """
    # Convert image to float32 for accurate calculations to avoid truncation errors
    img_float = image.astype(np.float32)

    # Get BGR values of the reference pixel
    ref_x, ref_y = reference_pixel_coords
    # OpenCV images are typically indexed as [height, width, channels] or [y, x, channels]
    ref_b, ref_g, ref_r = img_float[ref_y, ref_x]

    print(f"  Reference pixel's original BGR: ({ref_b:.2f}, {ref_g:.2f}, {ref_r:.2f})")

    # Calculate the average intensity of the reference pixel.
    # This will be the target intensity for each channel of the reference pixel.
    avg_ref_intensity = (ref_b + ref_g + ref_r) / 3.0

    # Calculate scaling factors for each channel.
    # Avoid division by zero if a channel is 0 (unlikely for a "white" pixel)
    # If a channel is 0, we treat it as 1 to prevent NaN and ensure the color is not completely eliminated.
    scale_b = avg_ref_intensity / (ref_b if ref_b != 0 else 1)
    scale_g = avg_ref_intensity / (ref_g if ref_g != 0 else 1)
    scale_r = avg_ref_intensity / (ref_r if ref_r != 0 else 1)

    print(f"  Scaling factors (B, G, R): ({scale_b:.2f}, {scale_g:.2f}, {scale_r:.2f})")

    # Apply scaling to each channel of the entire image
    corrected_img = np.zeros_like(img_float)
    corrected_img[:, :, 0] = img_float[:, :, 0] * scale_b  # Blue channel
    corrected_img[:, :, 1] = img_float[:, :, 1] * scale_g  # Green channel
    corrected_img[:, :, 2] = img_float[:, :, 2] * scale_r  # Red channel

    # Clip values to [0, 255] and convert back to uint8
    # np.clip ensures that pixel values do not exceed the valid range after scaling
    corrected_img = np.clip(corrected_img, 0, 255).astype(np.uint8)

    # Verify the reference pixel after correction (for debugging)
    b_corr, g_corr, r_corr = corrected_img[ref_y, ref_x]
    print(f"  Reference pixel's corrected BGR: ({b_corr}, {g_corr}, {r_corr})")

    return corrected_img

def main():
    print("--- Click White Balance Project ---")

    # 1. Generate a synthetic test image
    print("\n[Step 1/3] Generating synthetic test image...")
    original_image, white_pixel_coords = generate_test_image()
    print(f"  Test image generated with dimensions {original_image.shape[1]}x{original_image.shape[0]}.")
    print(f"  Simulated 'white' reference pixel for correction is at: {white_pixel_coords}")

    # Save the original image
    output_original_path = "original_image.png"
    cv2.imwrite(output_original_path, original_image)
    print(f"  Original image saved to '{output_original_path}'")

    # 2. Apply white balance correction
    print("\n[Step 2/3] Applying white balance correction based on the reference pixel...")
    corrected_image = apply_white_balance(original_image, white_pixel_coords)

    # 3. Save the corrected image
    print("\n[Step 3/3] Saving the corrected image...")
    output_corrected_path = "corrected_image.png"
    cv2.imwrite(output_corrected_path, corrected_image)
    print(f"  Corrected image saved to '{output_corrected_path}'")

    print("\n--- White balance process completed. Check output files. ---")

if __name__ == "__main__":
    main()