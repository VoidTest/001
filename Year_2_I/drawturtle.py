import cv2
import numpy as np
import turtle
import os
import math

# Global variables for interactive zoom.
zoom = 1.0
G_centered_contours = []  # Centered contours (unscaled)
G_approx_contours = []    # For computing average intensities
G_img = None              # The original image, needed for intensity computations

CANVAS_WIDTH = 600
CANVAS_HEIGHT = 600
MARGIN = 20  # margin to leave around the drawing

def load_image(image_path):
    """
    Loads a grayscale image at its original resolution.
    """
    if not os.path.exists(image_path):
        raise ValueError(f"Image not found at {image_path}")
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError("Image not found or unable to load.")
    return img

def preprocess_image(img):
    """
    Applies a light Gaussian blur and a morphological closing to connect nearby edges.
    """
    blurred = cv2.GaussianBlur(img, (3, 3), 0)
    kernel = np.ones((3, 3), np.uint8)
    closed = cv2.morphologyEx(blurred, cv2.MORPH_CLOSE, kernel)
    return closed

def detect_edges(img):
    """
    Detects edges using Canny edge detection on the preprocessed image.
    """
    preprocessed = preprocess_image(img)
    edges = cv2.Canny(preprocessed, 40, 100)
    return edges

def get_contours(edges, min_area=2):
    """
    Finds contours using RETR_TREE (to capture nested/internal features)
    and filters out very small ones.
    """
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return [cnt for cnt in contours if cv2.contourArea(cnt) > min_area]

def approximate_contour(contour, epsilon_factor=0.0007):
    """
    Approximates a contour to a polygon.
    A lower epsilon_factor preserves more detail.
    """
    epsilon = epsilon_factor * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, epsilon, True)
    pts = approx.reshape(-1, 2)
    return pts

def center_contours(contours_pts):
    """
    Centers a list of contours on the drawing area without scaling them.
    Returns the centered contours.
    """
    all_pts = np.vstack(contours_pts)
    min_xy = np.min(all_pts, axis=0)
    max_xy = np.max(all_pts, axis=0)
    center = (min_xy + max_xy) / 2.0

    # We choose the center of our canvas as (CANVAS_WIDTH/2, CANVAS_HEIGHT/2)
    screen_center = np.array([CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2])
    offset = screen_center - center

    centered_contours = []
    for pts in contours_pts:
        pts = pts.astype(np.float32)
        pts_centered = pts + offset
        # In turtle, the y-coordinate increases upward; invert y.
        pts_centered[:, 1] = -pts_centered[:, 1]
        centered_contours.append(pts_centered)
    return centered_contours

def get_bounding_box(contours):
    """
    Computes the bounding box (min and max x and y) of a list of contours.
    """
    all_pts = np.vstack(contours)
    min_xy = np.min(all_pts, axis=0)
    max_xy = np.max(all_pts, axis=0)
    return min_xy, max_xy

def compute_initial_zoom(centered_contours):
    """
    Computes an initial zoom factor so that the entire drawing fits within the canvas,
    with a given margin.
    """
    min_xy, max_xy = get_bounding_box(centered_contours)
    drawing_width = max_xy[0] - min_xy[0]
    drawing_height = max_xy[1] - min_xy[1]
    # Compute scale factors to fit width and height (taking margin into account).
    scale_w = (CANVAS_WIDTH - MARGIN) / drawing_width if drawing_width > 0 else 1
    scale_h = (CANVAS_HEIGHT - MARGIN) / drawing_height if drawing_height > 0 else 1
    return min(scale_w, scale_h)

def get_average_intensity(pts, img):
    """
    Computes the average intensity (0-255) for the given contour's points using the original image.
    """
    intensities = []
    h, w = img.shape
    for p in pts:
        x, y = int(round(p[0])), int(round(p[1]))
        x = np.clip(x, 0, w - 1)
        y = np.clip(y, 0, h - 1)
        intensities.append(img[y, x])
    return sum(intensities) / len(intensities) if intensities else 0

def draw_all_contours():
    """
    Clears the turtle canvas and draws all centered contours using the current global zoom factor.
    The pen color for each contour is based on its average intensity.
    """
    turtle.clearscreen()
    screen = turtle.Screen()
    screen.setup(CANVAS_WIDTH, CANVAS_HEIGHT)
    turtle.colormode(255)
    turtle.tracer(5)
    
    t = turtle.Turtle()
    t.speed(0)
    t.hideturtle()
    
    for i, pts in enumerate(G_centered_contours):
        pts_zoomed = pts * zoom  # Apply the current zoom factor.
        avg_intensity = get_average_intensity(G_approx_contours[i], G_img)
        color = (int(avg_intensity), int(avg_intensity), int(avg_intensity))
        t.pencolor(color)
        if len(pts_zoomed) == 0:
            continue
        t.penup()
        t.goto(pts_zoomed[0][0], pts_zoomed[0][1])
        t.pendown()
        for point in pts_zoomed[1:]:
            t.goto(point[0], point[1])
        t.goto(pts_zoomed[0][0], pts_zoomed[0][1])
        turtle.update()

def zoom_in():
    global zoom
    zoom *= 1.1  # Increase zoom by 10%
    draw_all_contours()

def zoom_out():
    global zoom
    zoom /= 1.1  # Decrease zoom by 10%
    draw_all_contours()

def main():
    global G_centered_contours, G_approx_contours, G_img, zoom
    image_path = r"\\ri.riga.lv\rag\Audzekni\akaletovs\My Documents\GitHub\001\Year_2_I\input.jpg"
    G_img = load_image(image_path)
    edges = detect_edges(G_img)
    contours = get_contours(edges, min_area=2)
    if not contours:
        raise ValueError("No contours found!")
    G_approx_contours = [approximate_contour(cnt, epsilon_factor=0.0007) for cnt in contours]
    # Center the contours (without scaling).
    G_centered_contours = center_contours(G_approx_contours)
    # Compute the initial zoom so that the entire drawing fits within the canvas.
    zoom = compute_initial_zoom(G_centered_contours)
    
    screen = turtle.Screen()
    screen.setup(CANVAS_WIDTH, CANVAS_HEIGHT)
    screen.onkey(zoom_in, "+")
    screen.onkey(zoom_in, "Up")
    screen.onkey(zoom_out, "-")
    screen.onkey(zoom_out, "Down")
    screen.listen()
    
    draw_all_contours()
    turtle.done()

if __name__ == "__main__":
    main()
