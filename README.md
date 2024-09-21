# 🚶‍♂️ Person Detection and Tracking with YOLOv8 and Telegram Alerts 🚨

**Key Features:**
- 🔍 **Real-time Person Detection** with YOLOv8.
- 📦 **Multi-object tracking** and **region-based alerting** via Telegram.
- ⚙️ **Customizable Region Selection** for monitoring specific areas.

## 🚀 How to Run This Program
- Prerequisites 📋
- Python 3.8+ installed.
- YOLOv8 by Ultralytics. You can install it using pip.
- OpenCV for image and video processing.
- Telegram Bot API token (create your bot on Telegram using BotFather).
- Other Dependencies as listed below.

1. Clone the Repository
2. Install Dependencies 📦
   Make sure you have all required Python libraries installed. You can do this by running:
   - pip install ultralytics opencv-python-headless numpy python-telegram-bot asyncio
3. Update the TELEGRAM_TOKEN and CHAT_ID values in the script with your bot's API token and your chat ID.
4. Run the Program ▶️
5. Region Selection 🖼️
   - After the video starts, you’ll be prompted to define a region by clicking on the video frame.
   - Press the 'f' key once you’ve marked at least four points to create a polygonal region.
   - The system will now monitor this region and send alerts if a person stays within it for the specified duration
     
## 1. Model Selection and Training Data 💻

- **Model Selection:**  
  YOLOv8 is selected for its blazing speed 🚀 and precise detection 🎯. We're using the `yolov8s.pt` model, which balances lightweight performance with top-tier accuracy in real-time applications.
  
- **Training Data:**  
  The model comes pre-trained on the COCO dataset, enabling it to recognize a wide variety of objects, including the "person" class 🧍. If you need more specialized detection, custom datasets can be used for further training 🎓.

## 2. Model Accuracy 🔧

- **Detection Accuracy:**  
  YOLOv8 shines with high precision in identifying people, even in complex or crowded environments 🏙️. It can detect individuals quickly while maintaining strong performance across various lighting conditions 🌇.
  
- **Tracking Performance:**  
  The system tracks each detected person and assigns unique IDs using BoT-SORT, the default algorithm, combining motion and appearance data for robust tracking 🔄. Alternatively, the powerful ByteTrack can be enabled to enhance multi-object tracking 🚶‍♂️🚶‍♀️.

## 3. The Logic Behind 🔍🤔

To determine how long a person stays within a predefined region, the system follows this process:

- **Person Detection:**  
  YOLOv8 detects people within the video feed 📹, returning precise bounding box coordinates 🟩 for each detected individual.

- **Region Selection:**  
  Users can manually select a region within the frame 🖼️, allowing the system to monitor that area for any person who enters 👀 and remains there.

- **Alerting via Telegram:**  
  If a person stays within the designated region for a set period ⏱️, an alert is triggered 📲. The system sends a **Telegram message** along with an annotated image showing the detected individual, so you stay informed in real-time! 📸

### 🚶‍♀️ Multi-Object Tracking with BoT-SORT 🔄

The system uses BoT-SORT to track multiple people effectively. This advanced algorithm blends motion and appearance data for superior performance, ensuring accurate tracking even with complex scenes or occlusions 🛠️.

---

💡 **Future Enhancements**:  
- Real-time **notifications via multiple platforms**, including SMS and email 📧.
