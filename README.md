# 🚶‍♂️ Person Detection and Tracking with YOLOv8 and Telegram Alerts 🚨

**Key Features:**
- 🔍 **Real-time Person Detection** with YOLOv8.
- 📦 **Multi-object tracking** and **region-based alerting** via Telegram.
- ⚙️ **Customizable Region Selection** for monitoring specific areas.

## 1. Model Selection and Training Data 💻

- **Model Selection:**  
  YOLOv8 is selected for its blazing speed 🚀 and precise detection 🎯. We're using the `yolov8s.pt` model, which balances lightweight performance with top-tier accuracy in real-time applications.
  
- **Training Data:**  
  The model comes pre-trained on the COCO dataset, enabling it to recognize a wide variety of objects, including the "person" class 🧍. If you need more specialized detection, custom datasets can be used for further training 🎓.

## 2. Model Accuracy 🔧

- **Detection Accuracy:**  
  YOLOv8 shines with high precision in identifying people, even in complex or crowded environments 🏙️. It can detect individuals quickly while maintaining strong performance across various lighting conditions 🌇.
  
- **Tracking Performance:**  
  The system assigns unique IDs to each person using a distance-based tracking method. For those seeking cutting-edge tracking accuracy, this can be upgraded with advanced algorithms like **SORT** or **BoT-SORT** 🔄.

## 3. The Logic Behind 🔍🤔

To determine how long a person stays within a predefined region, the system follows this process:

- **Person Detection:**  
  YOLOv8 detects people within the video feed 📹, returning precise bounding box coordinates 🟩 for each detected individual.

- **Region Selection:**  
  Users can manually select a region within the frame 🖼️, allowing the system to monitor that area for any person who enters 👀 and remains there.

- **Alerting via Telegram:**  
  If a person stays within the designated region for a set period ⏱️, an alert is triggered 📲. The system sends a **Telegram message** along with an annotated image showing the detected individual, so you stay informed in real-time! 📸

### 🚶‍♀️ Multi-Object Tracking with BoT-SORT 🔄

Currently, the tracking system uses a distance-based method to assign unique IDs to people. However, for a more advanced solution, **BoT-SORT** can be integrated 🛠️. BoT-SORT combines motion and appearance data, delivering more robust tracking in complex scenes with multiple moving objects.

---

💡 **Future Enhancements**:  
- Integration with **BoT-SORT** for more accurate multi-object tracking.
- Adding an adjustable **alert threshold** to fine-tune how long a person must stay in the region before sending an alert.
- Real-time **notifications via multiple platforms**, including SMS and email 📧.
