import cv2
import numpy as np
from ultralytics import YOLO
import time
import telegram
import asyncio
import os

# Telegram bot configuration
TELEGRAM_TOKEN = ""  # Replace with your bot token
CHAT_ID = ""  # Replace with your chat ID

bot = telegram.Bot(token=TELEGRAM_TOKEN)

async def send_alert(person_id, frame, bbox_color=(0, 0, 255), class_name="person", save_directory="alerts"):
    """Send an alert message and image to the Telegram bot with retry logic."""
    
    # Create directory to save images if it doesn't exist
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    # Define the filename with absolute path
    image_filename = os.path.join(save_directory, f"person_{person_id}.jpg")

    # Annotate the frame
    cv2.putText(frame, f"{class_name} ID: {person_id}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, bbox_color, 2)

    # Save the frame as a jpg
    if cv2.imwrite(image_filename, frame):
        print(f"Image {image_filename} saved successfully.")
    else:
        print(f"Failed to save {image_filename}.")
        return  # Exit if the image is not saved correctly

    # Retry logic for sending the image to Telegram
    attempts = 5
    while attempts > 0:
        try:
            with open(image_filename, 'rb') as image_file:
                await bot.send_photo(chat_id=CHAT_ID, photo=image_file)
            print(f"Alert sent to Telegram for Person ID {person_id}.")
            
            await asyncio.sleep(1)  # Add delay between requests (1 second)
            break  # Exit the loop if sending succeeds
        
        except telegram.error.TimedOut:
            attempts -= 1
            print(f"Connection timeout. Retrying... {3 - attempts}/3")
            await asyncio.sleep(2)  # Wait before retrying
        
        except Exception as e:
            print(f"Failed to send image to Telegram after retries: {e}")
            break  # Exit the loop on other exceptions


def run_async_alert(person_id, frame):
    loop = asyncio.get_event_loop()
    if loop.is_running():
        # If there's an event loop running, create a task instead
        asyncio.ensure_future(send_alert(person_id, frame))
    else:
        loop.run_until_complete(send_alert(person_id, frame))

def create_region(frame):
    img = frame.copy()
    region = []

    def click_event(event, x, y, flags, params):
        nonlocal img, region
        if event == cv2.EVENT_LBUTTONDOWN:
            cv2.circle(img, (x, y), 5, (255, 255, 0), -1)
            region.append(x)
            region.append(y)
            cv2.imshow("Tracking", img)

    cv2.namedWindow("Tracking")
    cv2.setMouseCallback("Tracking", click_event, {"img": img})

    cv2.putText(
        img,
        "Click to define region. Press 'f' to finish",
        (10, 20),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (255, 255, 255),
        2,
    )
    cv2.imshow("Tracking", img)

    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == ord("f"):
            if len(region) >= 8:  # Minimum points to define a polygon
                return region
            else:
                print('Please enter at least 4 points for the region.')
                region = []
                img = frame.copy()
                cv2.setMouseCallback("Tracking", click_event, {"img": img})
                cv2.putText(
                    img,
                    "Click to define region. Press 'f' to finish",
                    (10, 20),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (255, 255, 255),
                    2,
                )
                cv2.imshow("Tracking", img)

def draw_region(frame, region, color=(0, 255, 0)):
    if len(region) < 8:
        return
    vertices = np.array([[region[i], region[i + 1]] for i in range(0, len(region), 2)])
    cv2.polylines(frame, [vertices], isClosed=True, color=color, thickness=2)

# Open video file
cap = cv2.VideoCapture(r"")  # Update with your video path

# Define codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output_tracking.avi', fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))

# Get a frame for drawing the region
ret, frame = cap.read()
if not ret:
    raise RuntimeError("Failed to capture the first frame for region selection")

# Let the user define the region
region = create_region(frame)

# Thresholds
person_threshold = 2  # Number of people in the region to trigger an alert
duration_threshold = 5  # Time in seconds for alert
alert_display_duration = 3  # Keep alert visible for 3 seconds

# Initialize variables for tracking
start_time = {}
alert_triggered = {}
alert_display_time = {}
timeout_duration = 2  # Remember people for 2 seconds if they exit briefly
last_seen = {}
existing_boxes = {}  # To keep track of existing boxes
next_id = 1  # Start IDs from 1

# Function to find the closest ID based on the box
def find_closest_id(new_box, existing_boxes, threshold=50):
    closest_id = None
    min_distance = float('inf')
    for id, box in existing_boxes.items():
        distance = np.linalg.norm(np.array(new_box[:2]) - np.array(box[:2]))  # Calculate distance
        if distance < min_distance and distance < threshold:  # Check against threshold
            min_distance = distance
            closest_id = id
    return closest_id

# Load the YOLO model
model = YOLO("yolov8s.pt")  # Change this to your specific model if needed

# Perform tracking
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Perform tracking with YOLO
    results = model.track(frame)

    # Draw the selected region on the frame
    draw_region(frame, region)

    # Initialize count of persons in the region
    persons_in_region = 0

    # Check detections
    for result in results:
        boxes = result.boxes
        for box in boxes:
            if box.id is None:  # Check if the ID is None
                continue  # Skip this box if ID is not assigned

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cls_id = int(box.cls)
            class_name = model.names[cls_id]

            new_box = (x1, y1, x2, y2)

            # Only count "person" class
            if class_name == "person":
                closest_id = find_closest_id(new_box, existing_boxes)

                if closest_id is not None:
                    id = closest_id  # Use the closest existing ID
                else:
                    id = next_id  # Create a new ID
                    next_id += 1  # Increment next ID

                existing_boxes[id] = new_box  # Update the existing boxes

                # Check if the tracked person is within the selected region
                vertices = np.array([[region[i], region[i + 1]] for i in range(0, len(region), 2)])
                if cv2.pointPolygonTest(vertices, (x1, y1), False) >= 0:
                    bbox_color = (0, 0, 255)  # Red
                    last_seen[id] = time.time()
                    if id not in start_time:
                        start_time[id] = time.time()
                        alert_triggered[id] = False
                    elif time.time() - start_time[id] >= duration_threshold:
                        if not alert_triggered[id]:
                            print(f"ALERT: Person ID {id} in region for {duration_threshold} seconds!")
                            alert_triggered[id] = True
                            alert_display_time[id] = time.time()  # Record when the alert was triggered

                            # Annotate the frame before sending
                            annotated_frame = frame.copy()
                            cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), bbox_color, 2)
                            cv2.putText(annotated_frame, f"{class_name} ID: {id}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, bbox_color, 2)

                            run_async_alert(id, annotated_frame)  # Send annotated frame to Telegram
                else:
                    bbox_color = (0, 255, 0)  # Green
                    if id in last_seen and (time.time() - last_seen[id] > timeout_duration):
                        if id in start_time:
                            del start_time[id]
                            del alert_triggered[id]
                            if id in alert_display_time:
                                del alert_display_time[id]

                cv2.rectangle(frame, (x1, y1), (x2, y2), bbox_color, 2)
                cv2.putText(frame, f"{class_name} ID: {id}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, bbox_color, 2)

    # Display alerts if still within the display time window
    current_time = time.time()
    for person_id in alert_display_time.copy():
        if current_time - alert_display_time[person_id] < alert_display_duration:
            cv2.putText(
                frame,
                f"ALERT: Person ID {person_id} in region!",
                (50, 50 + 30 * person_id),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                3,
            )
        else:
            del alert_display_time[person_id]

    cv2.imshow('Tracking', frame)
    out.write(frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release everything
cap.release()
out.release()
cv2.destroyAllWindows()
