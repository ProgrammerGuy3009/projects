# 👁️‍🗨️ CognitoAI – Facial Recognition-Based Attendance System

**CognitoAI** is a smart attendance management system that leverages **AI-powered facial recognition** to automate and streamline attendance processes in educational institutions and organizations. Built with **KivyMD**, **OpenCV**, and **MySQL**, this intuitive and touchless system ensures accuracy, security, and real-time analytics.

---

## 🚀 Features

- 🎥 **Live Camera & Image Upload Support**  
  Detect and recognize student faces through a live webcam feed or group photo upload.

- 🤖 **Facial Recognition & Attendance Automation**  
  Real-time face matching and attendance marking using `face_recognition` and `dlib`.

- 📊 **Interactive Dashboard**  
  View statistics, heatmaps, and leaderboards. Apply filters (by date, student, course, attendance %).

- 🧠 **Smart Analytics & Visualization**  
  Built-in graphs using `Matplotlib` and `Seaborn` for performance tracking and daily trends.

- 🗂️ **Database Integration**  
  Secure storage and retrieval via MySQL backend for student and attendance data.

- 📝 **CSV Export & Editable Records**  
  Filtered attendance data can be exported and edited easily for auditing or manual updates.

---

## 📂 Application Structure

### 🧍 Face Recognition Screen  
Capture live video, recognize faces, and mark attendance.  
![image](https://github.com/user-attachments/assets/ff0ab390-3323-4cfc-9c35-ecdb9fd2716a)
![image](https://github.com/user-attachments/assets/a6d3e13a-a442-4725-9c88-d0d7be0eaf16)
📸 * – Face Recognition Screen*  

![image](https://github.com/user-attachments/assets/05a0292f-1858-4b9b-a12c-3b67ec96f9c2)
☰ * – Sidebar Navigation*

---

### 📈 Dashboard  
See real-time stats: top performers, heatmaps, daily rates, and more.  

![image](https://github.com/user-attachments/assets/5f1575a8-b86a-474c-8f49-f53c093ec172)
📊 * – Dashboard Overview*

![image](https://github.com/user-attachments/assets/4a7d773e-f69f-4cb3-a612-e3aa2cfbfc2f)
📈 * – Attendance Graphs*  

![image](https://github.com/user-attachments/assets/1c7ca6c4-b7fc-4fb2-acf4-6519710908bf)
🗂️ * – Attendance Records*  

![image](https://github.com/user-attachments/assets/a96746c1-2586-4c04-8070-f247fb0719dc)
🧯 * – Edit Attendance Section*

---

### ➕ Add Student  
Add a new student by entering details and uploading or capturing a face.  

![image](https://github.com/user-attachments/assets/6d3af584-a6f6-4b1d-b3e7-071be57e6e12)
🧑‍🎓 * – Add Student Screen*

---

## ⚙️ Features Summary

| Feature            | Description                                                        |
|--------------------|--------------------------------------------------------------------|
| Face Recognition   | Live webcam and static image recognition with confidence score     |
| Attendance Marking | Automated present/absent assignment for all students               |
| Dashboard          | Filters, leaderboards, graphs, summary cards                       |
| Export to CSV      | One-click export for filtered data                                 |
| Realtime Edits     | Update today’s attendance via GUI                                  |
| Multi-Face Support | Supports group photo recognition for multiple students             |
| Theme Toggle       | Switch between light and dark modes                                |

---

## 🛠️ Tech Stack

- **Frontend**: KivyMD (Material Design for Kivy)
- **Backend**: Python, MySQL
- **Face Recognition**: `face_recognition`, `OpenCV`, `dlib`
- **Data Visualization**: `Matplotlib`, `Seaborn`, `Pandas`

---

## ✨ CONTRIBUTION ✨

The development of *CognitoAI – A Facial Recognition-Based Attendance System* was a collaborative effort made possible through the dedicated work and specialized contributions of each team member. The responsibilities were clearly divided to ensure efficient progress and quality output.

---

### 👨‍💻 [Akshay Maurya](https://github.com/AkshayMaurya12)
**Role:** Backend Developer, Database Architect, and **Dashboard Designer**  
**Key Contributions:**

- 🗄️ **Database Design & Management:**  
  Designed the complete MySQL schema, including student and attendance tables, with proper relational structure and efficient CRUD operations.

- 📊 **Dashboard & Data Visualization:**  
  Developed an interactive and filterable dashboard to present real-time analytics using `Matplotlib`, `Pandas`, and `Seaborn`.  
  Implemented features like top performer charts, attendance heatmaps, and percentage-based filtering.

- 🎨 **Dashboard UI Design:**  
  Designed and implemented the dashboard’s user interface in `KivyMD`, ensuring a clean, organized layout with responsive elements for optimal user experience.

- 🧪 **System Integration & Testing:**  
  Integrated dashboard data with the database backend and ensured consistency, usability, and performance through thorough testing.

---

### 📷 Prasoon  
**Role:** ML Engineer, Camera Module Specialist, and Lead Frontend Developer  
**Key Contributions:**

- 📸 **Camera & Image Capture Module:**  
  Implemented the live camera feed using `OpenCV`, enabling real-time face capture and static image upload for flexible input.

- 🤖 **Face Detection & Recognition Pipeline:**  
  Built the facial recognition system using `face_recognition` and `dlib`, including encoding generation and face-matching logic with optimized accuracy.

- 🧠 **Model Integration & Attendance Logic:**  
  Connected face recognition results to real-time attendance marking in the database, including confidence-based recognition and automatic absentee marking.

- 🖥️ **User Interface & Experience:**  
  Designed and developed all user-facing interfaces using `KivyMD`, including screens for face recognition, student registration, attendance review, and app navigation.

- 🔍 **Robust Error Handling:**  
  Implemented clear, user-friendly error messages and safeguards for edge cases like missing faces, duplicate records, and system failures.

---

### 🤝 Final Outcome

Together, the team successfully built **CognitoAI**, a powerful, scalable, and user-centric attendance management system powered by AI. The seamless combination of machine learning, efficient backend systems, and a polished graphical interface resulted in a future-ready solution designed to streamline attendance for educational and institutional environments.

---

