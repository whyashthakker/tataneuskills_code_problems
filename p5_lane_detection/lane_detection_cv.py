import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

def generate_road_image(width=640, height=480):
    image = np.zeros((height, width, 3), dtype=np.uint8)
    image.fill(100)
    cv2.line(image, (width//4, height), (width//3, height//2), (255, 255, 255), 5)
    cv2.line(image, (3*width//4, height), (2*width//3, height//2), (255, 255, 255), 5)
    return image

def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    return blur

def detect_edges(image):
    return cv2.Canny(image, 50, 150)

def region_of_interest(image):
    height, width = image.shape
    polygon = np.array([[(0, height), (width, height), (width//2, height//2)]])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, polygon, 255)
    return cv2.bitwise_and(image, mask)

def detect_lines(image):
    return cv2.HoughLinesP(image, 1, np.pi/180, 50, minLineLength=50, maxLineGap=100)

def average_slope_intercept(lines):
    left_lines, right_lines = [], []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        if x2 == x1:
            continue
        slope = (y2 - y1) / (x2 - x1)
        intercept = y1 - slope * x1
        (left_lines if slope < 0 else right_lines).append((slope, intercept))
    
    left_avg = np.average(left_lines, axis=0) if left_lines else None
    right_avg = np.average(right_lines, axis=0) if right_lines else None
    return left_avg, right_avg

def create_lane_lines(image, lines):
    left_avg, right_avg = average_slope_intercept(lines)
    y1, y2 = image.shape[0], int(image.shape[0] * 0.6)

    if left_avg is not None:
        left_x1 = int((y1 - left_avg[1]) / left_avg[0])
        left_x2 = int((y2 - left_avg[1]) / left_avg[0])
        cv2.line(image, (left_x1, y1), (left_x2, y2), (255, 0, 0), 5)

    if right_avg is not None:
        right_x1 = int((y1 - right_avg[1]) / right_avg[0])
        right_x2 = int((y2 - right_avg[1]) / right_avg[0])
        cv2.line(image, (right_x1, y1), (right_x2, y2), (255, 0, 0), 5)

def lane_detection(image):
    preprocessed = preprocess_image(image)
    edges = detect_edges(preprocessed)
    roi = region_of_interest(edges)
    lines = detect_lines(roi)
    
    if lines is not None:
        lane_image = np.zeros_like(image)
        create_lane_lines(lane_image, lines)
        return cv2.addWeighted(image, 0.8, lane_image, 1, 1)
    else:
        return image

class LaneDetectionVisualizer:
    def __init__(self):
        self.road_image = generate_road_image()
        self.current_step = 0
        self.steps = [
            ("Original Image", lambda: self.road_image),
            ("Grayscale", lambda: cv2.cvtColor(preprocess_image(self.road_image), cv2.COLOR_GRAY2RGB)),
            ("Edge Detection", lambda: cv2.cvtColor(detect_edges(preprocess_image(self.road_image)), cv2.COLOR_GRAY2RGB)),
            ("Region of Interest", lambda: cv2.cvtColor(region_of_interest(detect_edges(preprocess_image(self.road_image))), cv2.COLOR_GRAY2RGB)),
            ("Lane Detection", lambda: lane_detection(self.road_image))
        ]
        
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        plt.subplots_adjust(bottom=0.2)
        self.img_plot = self.ax.imshow(self.road_image)
        self.ax.axis('off')
        
        self.ax_prev = plt.axes([0.3, 0.05, 0.1, 0.075])
        self.ax_next = plt.axes([0.6, 0.05, 0.1, 0.075])
        self.b_prev = Button(self.ax_prev, 'Previous')
        self.b_next = Button(self.ax_next, 'Next')
        self.b_prev.on_clicked(self.previous_step)
        self.b_next.on_clicked(self.next_step)
        
        self.update_image()

    def update_image(self):
        step_name, step_func = self.steps[self.current_step]
        self.img_plot.set_data(step_func())
        self.ax.set_title(step_name)
        self.fig.canvas.draw_idle()

    def previous_step(self, event):
        self.current_step = max(0, self.current_step - 1)
        self.update_image()

    def next_step(self, event):
        self.current_step = min(len(self.steps) - 1, self.current_step + 1)
        self.update_image()

# Create and show the visualizer
visualizer = LaneDetectionVisualizer()
plt.show()
