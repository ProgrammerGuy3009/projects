from kivymd.app import MDApp
from kivymd.uix.button import MDIconButton
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.toast import toast
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from plyer import filechooser
from kivy.uix.filechooser import FileChooserIconView
import mysql.connector
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import cv2
import numpy as np
import face_recognition
import os
from datetime import date, datetime
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.dropdownitem import MDDropDownItem
from kivymd.uix.card import MDCard
from kivymd.uix.menu import MDDropdownMenu
import io
from kivy.uix.image import CoreImage
from PIL import Image as PILImage
import pandas as pd
import pickle

Window.size = (800, 600)

class FaceRecognitionScreen(Screen):
    pass

class DashboardScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_date = None
        self.end_date = None
        self.selected_student = None
        self.selected_course = None
        self.selected_attendance_range = None

class MainScreen(Screen):
    pass


KV = """
MainScreen:

<MainScreen>:
    name: "main"

    MDNavigationLayout:
        id: nav_layout

        ScreenManager:
            id: screen_manager

            FaceRecognitionScreen:
                name: "face_recognition"

            DashboardScreen:
                name: "dashboard"
            
            AddStudentScreen:

        MDNavigationDrawer:
            id: nav_drawer
            type: "modal"
            radius: (0, 16, 16, 0)
            width: "280dp"

            MDBoxLayout:
                orientation: "vertical"
                padding: "8dp"
                spacing: "8dp"

                MDBoxLayout:
                    orientation: "vertical"
                    size_hint_y: None
                    height: "120dp"
                    padding: "16dp"

                    MDBoxLayout:
                        orientation: "horizontal"
                        spacing: "12dp"
                        adaptive_height: True

                        MDIcon:
                            icon: "face-recognition"
                            font_size: "48sp"
                            theme_text_color: "Primary"
                            pos_hint: {"center_y": 0.5}

                        MDLabel:
                            text: "CognitoAI"
                            font_style: "H5"
                            theme_text_color: "Primary"
                            size_hint_y: None
                            height: self.texture_size[1]
                            pos_hint: {"center_y": 0.5}

                    MDLabel:
                        text: "Face Recognition ERP System"
                        theme_text_color: "Secondary"
                        font_style: "Caption"

                MDSeparator:
                    height: "1dp"

                ScrollView:
                    MDList:
                    
                        OneLineIconListItem:
                            text: "Face Recognition"
                            on_release:
                                app.root.ids.nav_drawer.set_state("close")
                                app.switch_screen("face_recognition")
                            IconLeftWidget:
                                icon: "face-recognition"

                        OneLineIconListItem:
                            text: "Dashboard"
                            on_release:
                                app.root.ids.nav_drawer.set_state("close")
                                app.switch_screen("dashboard")
                            IconLeftWidget:
                                icon: "chart-bar"

                        OneLineIconListItem:
                            text: "User Info"
                            on_release:
                                app.root.ids.nav_drawer.set_state("close")
                            IconLeftWidget:
                                icon: "account"

                        OneLineIconListItem:
                            text: "Add Student"
                            on_release:
                                app.root.ids.nav_drawer.set_state("close")
                                app.switch_screen("add_student")
                            IconLeftWidget:
                                icon: "account-plus"


                        OneLineIconListItem:
                            text: "About"
                            on_release:
                                app.root.ids.nav_drawer.set_state("close")
                                app.show_about()
                            IconLeftWidget:
                                icon: "information-outline"

                        OneLineIconListItem:
                            text: "Help"
                            on_release:
                                app.root.ids.nav_drawer.set_state("close")
                                # app.switch_screen("help")
                            IconLeftWidget:
                                icon: "help-circle-outline"

                        OneLineIconListItem:
                            text: "Toggle Night Mode"
                            on_release:
                                app.root.ids.nav_drawer.set_state("close")
                                app.toggle_theme()
                            IconLeftWidget:
                                icon: "theme-light-dark"
                        

<FaceRecognitionScreen>:
    ScrollView:
        MDBoxLayout:
            orientation: "vertical"
            size_hint_y: None
            height: self.minimum_height
            padding: "16dp"
            spacing: "16dp"

            MDTopAppBar:
                title: "Face Recognition"
                elevation: 4
                left_action_items: [["menu", lambda x: app.root.ids.nav_drawer.set_state("toggle")]]

            MDCard:
                orientation: "vertical"
                size_hint_y: None
                height: "400dp"
                padding: "8dp"
                elevation: 1
                radius: [10, 10, 10, 10]

                MDLabel:
                    text: "Camera Feed"
                    size_hint_y: None
                    height: "30dp"
                    halign: "center"
                    theme_text_color: "Secondary"

                MDSeparator:
                    height: "1dp"

                MDBoxLayout:
                    id: camera_layout
                    padding: "8dp"

                    Image:
                        id: camera_feed
                        allow_stretch: True
                        keep_ratio: True

            MDCard:
                orientation: "vertical"
                size_hint_y: None
                height: self.minimum_height
                padding: "16dp"
                elevation: 1
                radius: [10, 10, 10, 10]

                MDLabel:
                    text: "Face Recognition Controls"
                    size_hint_y: None
                    height: "30dp"
                    halign: "center"
                    theme_text_color: "Secondary"

                MDSeparator:
                    height: "1dp"

                MDGridLayout:
                    cols: 2
                    adaptive_height: True
                    spacing: "16dp"
                    padding: "16dp"

                    MDRaisedButton:
                        text: "Start Camera"
                        icon: "camera"
                        size_hint_x: 1
                        on_release: app.start_camera()

                    MDRaisedButton:
                        text: "Recognize Faces"
                        icon: "face-recognition"
                        size_hint_x: 1
                        on_release: app.recognize_faces()

                    MDRaisedButton:
                        text: "Mark Attendance"
                        icon: "check-circle"
                        size_hint_x: 1
                        md_bg_color: app.theme_cls.accent_color
                        on_release: app.mark_attendance_from_camera()

                    MDRaisedButton:
                        text: "Update Face"
                        icon: "account-edit"
                        size_hint_x: 1
                        md_bg_color: app.theme_cls.accent_color
                        on_release: app.open_store_face_dialog()



                MDBoxLayout:
                    orientation: "horizontal"
                    size_hint_y: None
                    height: "50dp"
                    padding: "16dp"

                    MDRaisedButton:
                        text: "Upload Group Photo"
                        icon: "image-multiple"
                        size_hint_x: 1
                        on_release: app.upload_group_photo()

<DashboardScreen>:
    MDBoxLayout:
        orientation: "vertical"
        padding: "16dp"
        spacing: "16dp"

        MDTopAppBar:
            title: "Dashboard"
            elevation: 4
            left_action_items: [["menu", lambda x: app.root.ids.nav_drawer.set_state("toggle")]]

        # SUMMARY CARDS
        MDGridLayout:
            cols: 3
            spacing: "12dp"
            size_hint_y: None
            height: "100dp"

            MDCard:
                orientation: "vertical"
                padding: "8dp"
                radius: [12, 12, 12, 12]
                md_bg_color: app.theme_cls.primary_light

                MDLabel:
                    text: "Total Students"
                    halign: "center"
                    theme_text_color: "Secondary"
                    font_style: "Caption"

                MDLabel:
                    id: total_students
                    text: "0"
                    halign: "center"
                    theme_text_color: "Primary"
                    font_style: "H6"

            MDCard:
                orientation: "vertical"
                padding: "8dp"
                radius: [12, 12, 12, 12]
                md_bg_color: app.theme_cls.primary_light

                MDLabel:
                    text: "Total Attendance Records"
                    halign: "center"
                    theme_text_color: "Secondary"
                    font_style: "Caption"

                MDLabel:
                    id: total_records
                    text: "0"
                    halign: "center"
                    theme_text_color: "Primary"
                    font_style: "H6"

            MDCard:
                orientation: "vertical"
                padding: "8dp"
                radius: [12, 12, 12, 12]
                md_bg_color: app.theme_cls.primary_light

                MDLabel:
                    text: "Class Avg Attendance %"
                    halign: "center"
                    theme_text_color: "Secondary"
                    font_style: "Caption"

                MDLabel:
                    id: class_avg
                    text: "0%"
                    halign: "center"
                    theme_text_color: "Primary"
                    font_style: "H6"
        
        ScrollView:
            MDBoxLayout:
                orientation: "vertical"
                size_hint_y: None
                height: self.minimum_height
                padding: "16dp"
                spacing: "16dp"

                MDCard:
                    orientation: "vertical"
                    padding: "16dp"
                    size_hint_y: None
                    height: self.minimum_height
                    elevation: 1
                    radius: [10, 10, 10, 10]

                    MDLabel:
                        text: "Filters"
                        halign: "center"
                        theme_text_color: "Primary"
                        font_style: "H6"

                    MDGridLayout:
                        cols: 2
                        padding: "8dp"
                        spacing: "8dp"
                        adaptive_height: True

                        MDTextField:
                            id: start_date
                            hint_text: "Start Date (YYYY-MM-DD)"
                            on_focus: if self.focus: app.show_date_picker("start")
                            size_hint_x: 0.5

                        MDTextField:
                            id: end_date
                            hint_text: "End Date (YYYY-MM-DD)"
                            on_focus: if self.focus: app.show_date_picker("end")
                            size_hint_x: 0.5

                        MDDropDownItem:
                            id: student_dropdown
                            text: "Select Student"
                            on_release: app.show_student_dropdown(self)
                            size_hint_x: 0.5

                        MDDropDownItem:
                            id: course_dropdown
                            text: "Select Course"
                            on_release: app.show_course_dropdown(self)
                            size_hint_x: 0.5

                        MDDropDownItem:
                            id: attendance_range_dropdown
                            text: "Select Attendance Range"
                            on_release: app.show_attendance_range_dropdown(self)
                            size_hint_x: 0.5

                    MDBoxLayout:
                        orientation: "horizontal"
                        spacing: "8dp"
                        padding: "8dp"
                        size_hint_y: None
                        height: "48dp"

                        MDRaisedButton:
                            text: "Apply Filters"
                            size_hint_x: 0.33
                            on_release: app.update_dashboard()

                        MDRaisedButton:
                            text: "Reset Filters"
                            size_hint_x: 0.33
                            md_bg_color: app.theme_cls.error_color
                            on_release: app.reset_filters()

                        MDRaisedButton:
                            text: "Export to CSV"
                            size_hint_x: 0.33
                            on_release: app.export_filtered_data_to_csv()

                MDCard:
                    orientation: "vertical"
                    padding: "16dp"
                    size_hint_y: None
                    height: self.minimum_height
                    elevation: 1
                    radius: [10, 10, 10, 10]

                    MDLabel:
                        text: "Leaderboard"
                        halign: "center"
                        theme_text_color: "Primary"
                        font_style: "H6"

                    MDBoxLayout:
                        id: leaderboard_cards
                        orientation: "vertical"
                        spacing: "8dp"
                        size_hint_y: None
                        height: self.minimum_height
# 
                MDCard:
                    orientation: "vertical"
                    padding: "16dp"
                    size_hint_y: None
                    height: self.minimum_height
                    elevation: 1
                    radius: [10, 10, 10, 10]

                    MDLabel:
                        text: "Students by Attendance Range"
                        halign: "center"
                        theme_text_color: "Primary"
                        font_style: "H6"

                    ScrollView:
                        size_hint_y: None
                        height: "200dp"

                        MDList:
                            id: attendance_range_list        
# 

                
                # Graphs in a 2-column grid
                MDGridLayout:
                    cols: 2
                    spacing: "12dp"
                    padding: "8dp"
                    size_hint_y: None
                    height: self.minimum_height

                    MDCard:
                        orientation: "vertical"
                        padding: "12dp"
                        size_hint_x: 0.49
                        size_hint_y: None
                        height: "350dp"
                        elevation: 1
                        radius: [10, 10, 10, 10]

                        MDLabel:
                            text: "Overall Attendance Statistics"
                            halign: "center"
                            theme_text_color: "Primary"
                            font_style: "H6"

                        MDBoxLayout:
                            orientation: "vertical"
                            size_hint_y: None
                            height: "220dp"

                            Image:
                                id: overall_stats
                                size_hint_y: None
                                height: "220dp"
                                allow_stretch: True
                                keep_ratio: True

                            MDBoxLayout:
                                orientation: "horizontal"
                                size_hint_y: None
                                height: "40dp"
                                padding: "8dp"
                                spacing: "8dp"
                                pos_hint: {"center_x": 0.5}

                                MDIconButton:
                                    icon: "magnify-plus-outline"
                                    on_release: app.zoom_graph("overall_stats", 1.1)

                                MDIconButton:
                                    icon: "magnify-minus-outline"
                                    on_release: app.zoom_graph("overall_stats", 0.9)

                    MDCard:
                        orientation: "vertical"
                        padding: "12dp"
                        size_hint_x: 0.49
                        size_hint_y: None
                        height: "350dp"
                        elevation: 1
                        radius: [10, 10, 10, 10]

                        MDLabel:
                            text: "Individual Attendance Trend"
                            halign: "center"
                            theme_text_color: "Primary"
                            font_style: "H6"

                        MDBoxLayout:
                            orientation: "vertical"
                            size_hint_y: None
                            height: "220dp"

                            Image:
                                id: individual_trend
                                size_hint_y: None
                                height: "220dp"
                                allow_stretch: True
                                keep_ratio: True

                            MDBoxLayout:
                                orientation: "horizontal"
                                size_hint_y: None
                                height: "40dp"
                                padding: "8dp"
                                spacing: "8dp"
                                pos_hint: {"center_x": 0.5}

                                MDIconButton:
                                    icon: "magnify-plus-outline"
                                    on_release: app.zoom_graph("individual_trend", 1.1)

                                MDIconButton:
                                    icon: "magnify-minus-outline"
                                    on_release: app.zoom_graph("individual_trend", 0.9)

                    MDCard:
                        orientation: "vertical"
                        padding: "12dp"
                        size_hint_x: 0.49
                        size_hint_y: None
                        height: "350dp"
                        elevation: 1
                        radius: [10, 10, 10, 10]

                        MDLabel:
                            text: "Attendance Heatmap"
                            halign: "center"
                            theme_text_color: "Primary"
                            font_style: "H6"

                        MDBoxLayout:
                            orientation: "vertical"
                            size_hint_y: None
                            height: "220dp"

                            Image:
                                id: heatmap_graph
                                size_hint_y: None
                                height: "220dp"
                                allow_stretch: True
                                keep_ratio: True

                            MDBoxLayout:
                                orientation: "horizontal"
                                size_hint_y: None
                                height: "40dp"
                                padding: "8dp"
                                spacing: "8dp"
                                pos_hint: {"center_x": 0.5}

                                MDIconButton:
                                    icon: "magnify-plus-outline"
                                    on_release: app.zoom_graph("heatmap_graph", 1.1)

                                MDIconButton:
                                    icon: "magnify-minus-outline"
                                    on_release: app.zoom_graph("heatmap_graph", 0.9)

                    MDCard:
                        orientation: "vertical"
                        padding: "12dp"
                        size_hint_x: 0.49
                        size_hint_y: None
                        height: "350dp"
                        elevation: 1
                        radius: [10, 10, 10, 10]

                        MDLabel:
                            text: "Daily Attendance Rate"
                            halign: "center"
                            theme_text_color: "Primary"
                            font_style: "H6"

                        MDBoxLayout:
                            orientation: "vertical"
                            size_hint_y: None
                            height: "220dp"

                            Image:
                                id: daily_attendance_rate
                                size_hint_y: None
                                height: "220dp"
                                allow_stretch: True
                                keep_ratio: True

                            MDBoxLayout:
                                orientation: "horizontal"
                                size_hint_y: None
                                height: "40dp"
                                padding: "8dp"
                                spacing: "8dp"
                                pos_hint: {"center_x": 0.5}

                                MDIconButton:
                                    icon: "magnify-plus-outline"
                                    on_release: app.zoom_graph("daily_attendance_rate", 1.1)

                                MDIconButton:
                                    icon: "magnify-minus-outline"
                                    on_release: app.zoom_graph("daily_attendance_rate", 0.9)

                MDCard:
                    orientation: "vertical"
                    padding: "16dp"
                    size_hint_y: None
                    height: self.minimum_height
                    elevation: 1
                    radius: [10, 10, 10, 10]

                    MDLabel:
                        text: "Attendance Records (Latest First)"
                        halign: "center"
                        theme_text_color: "Primary"
                        font_style: "H6"

                    ScrollView:
                        size_hint_y: None
                        height: "250dp"

                        MDList:
                            id: attendance_list

                MDCard:
                    orientation: "vertical"
                    padding: "16dp"
                    size_hint_y: None
                    height: self.minimum_height
                    elevation: 1
                    radius: [10, 10, 10, 10]

                    MDLabel:
                        text: "Edit Today's Attendance"
                        halign: "center"
                        theme_text_color: "Primary"
                        font_style: "H6"

                    ScrollView:
                        size_hint_y: None
                        height: "300dp"

                        MDList:
                            id: edit_attendance_list


<AddStudentScreen@Screen>:
    name: "add_student"

    MDBoxLayout:
        orientation: "vertical"
        padding: "20dp"
        spacing: "10dp"

        MDTopAppBar:
            title: "Add New Student"
            elevation: 4
            left_action_items: [["menu", lambda x: app.root.ids.nav_drawer.set_state("toggle")]]

        MDCard:
            orientation: "vertical"
            size_hint_y: None
            height: "200dp"
            padding: "8dp"
            elevation: 1
            radius: [10, 10, 10, 10]

            MDLabel:
                text: "Camera Feed"
                size_hint_y: None
                height: "30dp"
                halign: "center"
                theme_text_color: "Secondary"

            MDSeparator:
                height: "1dp"

            Image:
                id: add_student_camera_feed
                size_hint_y: None
                height: "150dp"
                allow_stretch: True
                keep_ratio: True

        MDTextField:
            id: add_roll
            hint_text: "Roll Number"
            mode: "rectangle"
            on_text: app.check_roll_availability(self.text)

        MDTextField:
            id: add_name
            hint_text: "Name"
            mode: "rectangle"

        MDTextField:
            id: add_course
            hint_text: "Course"
            mode: "rectangle"

        MDTextField:
            id: add_dob
            hint_text: "Date of Birth (YYYY-MM-DD)"
            mode: "rectangle"

        MDGridLayout:
            cols: 2
            adaptive_height: True
            spacing: "16dp"
            padding: "16dp"

            MDRaisedButton:
                text: "Start Camera"
                icon: "camera"
                on_release: app.start_add_student_camera()

            MDRaisedButton:
                text: "Capture Face"
                icon: "camera-snapshot"
                on_release: app.capture_face_for_add()

            MDRaisedButton:
                text: "Upload Image"
                icon: "image-plus"
                on_release: app.upload_face_image()

            MDRaisedButton:
                text: "Save Student"
                icon: "content-save"
                md_bg_color: app.theme_cls.primary_color
                on_release: app.save_new_student()

        Widget:
            size_hint_y: None
            height: "20dp"


"""

class FaceAttendance:
    def __init__(self):
        self.known_face_encodings = []
        self.known_roll_numbers = []
        self.load_known_faces()
    
    def load_known_faces(self):
        self.known_face_encodings = []
        self.known_roll_numbers = []
        connection = mysql.connector.connect(host="localhost", user="root", password="0000", database="COGNITOAI")
        cursor = connection.cursor()
        cursor.execute("SELECT roll_no, face_id FROM student_info WHERE face_id IS NOT NULL")
        for roll_no, face_blob in cursor.fetchall():
            try:
                encoding = np.frombuffer(face_blob, dtype=np.float64)
                if encoding.size == 128:  # Ensure valid face encoding (128 dimensions)
                    self.known_face_encodings.append(encoding)
                    self.known_roll_numbers.append(str(roll_no))
            except Exception as e:
                print(f"Error decoding face for roll {roll_no}: {e}")
        connection.close()

    def recognize_from_image(self, image):
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        locations = face_recognition.face_locations(rgb)
        encodings = face_recognition.face_encodings(rgb, locations)
        recognized = []
        for enc in encodings:
            distances = face_recognition.face_distance(self.known_face_encodings, enc)
            best_idx = np.argmin(distances)
            if distances[best_idx] < 0.6:
                confidence = (1 - distances[best_idx]) * 100
                recognized.append((self.known_roll_numbers[best_idx], confidence))
        return recognized

    def mark_attendance(self, rolls):
        connection = mysql.connector.connect(host="localhost", user="root", password="0000", database="COGNITOAI")
        cursor = connection.cursor()
        today = date.today().strftime('%Y-%m-%d')
        for roll in rolls:
            cursor.execute("SELECT * FROM attendance WHERE roll_no = %s AND date = %s", (roll, today))
            if cursor.fetchone() is None:
                cursor.execute("INSERT INTO attendance (roll_no, date, attendance) VALUES (%s, %s, 'P')", (roll, today))
        connection.commit()
        connection.close()

class StoreFaceDialog(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', spacing="12dp", padding="25dp", size_hint_y=None)
        self.height = "400dp"
        self.debounce_event = None
        self.bind(minimum_height=self.setter('height'))
        self.title_label = MDLabel(
            text="Store Face Data",
            halign="center",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1),
            font_style="H6",
            size_hint_y=None,
            height="40dp",
            padding=(10, 10)
        )
        self.add_widget(self.title_label)
        self.roll_input = MDTextField(
            hint_text="Enter Roll No",
            helper_text="Auto-fills if existing",
            helper_text_mode="on_focus",
            size_hint_y=None,
            height="60dp"
        )
        self.roll_input.bind(text=self.check_existing_student)
        self.add_widget(self.roll_input)

        self.name_input = MDTextField(hint_text="Enter Name")
        self.course_input = MDTextField(hint_text="Enter Course")
        self.dob_input = MDTextField(hint_text="DOB (YYYY-MM-DD)")
        self.add_widget(self.name_input)
        self.add_widget(self.course_input)
        self.add_widget(self.dob_input)

        self.buttons = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height='40dp')
        self.buttons.add_widget(MDFlatButton(text="Cancel", on_release=self.dismiss_dialog))
        self.buttons.add_widget(MDFlatButton(text="Load from Image", on_release=self.load_from_image))
        self.buttons.add_widget(MDRaisedButton(text="Capture from Camera", on_release=self.capture_from_camera))
        self.add_widget(self.buttons)

        self.dialog = None

    def open(self):
        self.dialog = MDDialog(
            title="",
            type="custom",
            content_cls=self,
            buttons=[],
            auto_dismiss=False
        )
        self.dialog.open()

    def dismiss_dialog(self, *args):
        self.dialog.dismiss()

    def check_existing_student(self, instance, value):
        if self.debounce_event:
            self.debounce_event.cancel()
        self.debounce_event = Clock.schedule_once(self.query_student_data, 0.5)

    def query_student_data(self, dt):
        roll_no = self.roll_input.text.strip()
        if not roll_no:
            return

        conn = mysql.connector.connect(host="localhost", user="root", password="0000", database="COGNITOAI")
        cursor = conn.cursor()
        cursor.execute("SELECT name, course, dob FROM student_info WHERE roll_no = %s", (roll_no,))
        data = cursor.fetchone()
        conn.close()

        if data:
            self.name_input.text = data[0]
            self.course_input.text = data[1]
            self.dob_input.text = str(data[2])
            toast("Student data loaded.")
        else:
            self.name_input.text = ""
            self.course_input.text = ""
            self.dob_input.text = ""

    def load_from_image(self, *args):
        chooser = FileChooserIconView()

        def select_file(instance, selection, touch):
            if selection:
                image_path = selection[0]
                self.store_face_data(image_path=image_path)
                popup.dismiss()

        popup = Popup(title="Select Image", content=chooser, size_hint=(0.9, 0.9))
        chooser.bind(on_submit=select_file)
        popup.open()

    def capture_from_camera(self, *args):
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()

        if ret:
            temp_path = "temp_capture.jpg"
            cv2.imwrite(temp_path, frame)
            self.store_face_data(image_path=temp_path)
            os.remove(temp_path)
        else:
            toast("Failed to capture image")

    def store_face_data(self, image_path):
        roll_no = self.roll_input.text.strip()
        name = self.name_input.text.strip()
        course = self.course_input.text.strip()
        dob = self.dob_input.text.strip()

        if not (roll_no and name and course and dob):
            toast("Please fill all fields")
            return

        img = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(img)
        if not encodings:
            toast("No face detected")
            return

        face_data = encodings[0].tobytes()

        conn = mysql.connector.connect(host="localhost", user="root", password="0000", database="COGNITOAI")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM student_info WHERE roll_no = %s", (roll_no,))
        # if cursor.fetchone():
        #     cursor.execute("""
        #         UPDATE student_info 
        #         SET name = %s, course = %s, dob = %s, face_id = %s
        #         WHERE roll_no = %s
        #     """, (name, course, dob, face_data, roll_no))
        #     toast("Student info updated")
        # else:
        #     cursor.execute("""
        #         INSERT INTO student_info (roll_no, name, course, dob, face_id)
        #         VALUES (%s, %s, %s, %s, %s)
        #     """, (roll_no, name, course, dob, face_data))
        #     toast("New student added")

        if cursor.fetchone():
            cursor.execute("""
                UPDATE student_info 
                SET name = %s, course = %s, dob = %s, face_id = %s
                WHERE roll_no = %s
            """, (name, course, dob, face_data, roll_no))
            toast("Student info updated successfully.")
        else:
            toast("Roll number not found. Please add new students from the Add Student tab.")
            conn.close()
            return


        conn.commit()
        conn.close()
        self.dialog.dismiss()


class CognitoAIApp(MDApp):
    def build(self):
        self.title = "CognitoAI"
        self.theme_cls.theme_style = "Light"  # Set initial theme
        self.theme_cls.primary_palette = "Blue"
        self.attendance = FaceAttendance()
        self.capture = None
        self.student_menu = None
        self.course_menu = None
        self.attendance_range_menu = None
        self.zoom_levels = {
            "overall_stats": 1.0,
            "individual_trend": 1.0,
            "heatmap_graph": 1.0,
            "daily_attendance_rate": 1.0
        }
        return Builder.load_string(KV)

    def switch_screen(self, screen):
        self.root.ids.screen_manager.current = screen
        if screen == "dashboard":
            self.load_dashboard_summary()
            self.load_attendance_records()
            self.load_editable_attendance()
            self.load_attendance_range_list()

    def zoom_graph(self, graph_id, scale_factor):
        # Get the current zoom level
        current_zoom = self.zoom_levels.get(graph_id, 1.0)
        new_zoom = current_zoom * scale_factor

        # Set zoom limits (e.g., 0.5x to 2.0x)
        if new_zoom < 0.5:
            new_zoom = 0.5
            toast("Minimum zoom level reached.")
        elif new_zoom > 2.0:
            new_zoom = 2.0
            toast("Maximum zoom level reached.")

        # Update the zoom level
        self.zoom_levels[graph_id] = new_zoom

        # Get the Image widget
        image_widget = self.root.ids.screen_manager.get_screen("dashboard").ids[graph_id]

        # Adjust the size of the Image widget
        base_height = 220  # Original height in dp
        new_height = base_height * new_zoom
        image_widget.height = f"{new_height}dp"

    def toggle_theme(self):
        if self.theme_cls.theme_style == "Light":
            self.theme_cls.theme_style = "Dark"
            self.theme_cls.primary_palette = "BlueGray"  # Suitable for dark mode
            toast("Switched to Night Mode")
        else:
            self.theme_cls.theme_style = "Light"
            self.theme_cls.primary_palette = "Blue"  # Suitable for light mode
            toast("Switched to Light Mode")
    def reset_filters(self):
        screen = self.root.ids.screen_manager.get_screen("dashboard")
        
        # Clear all filter fields
        screen.start_date = None
        screen.end_date = None
        screen.selected_student = None
        screen.selected_course = None
        screen.selected_attendance_range = None
        
        # Reset UI elements
        screen.ids.start_date.text = ""
        screen.ids.end_date.text = ""
        screen.ids.student_dropdown.text = "Select Student"
        screen.ids.course_dropdown.text = "Select Course"
        screen.ids.attendance_range_dropdown.text = "Select Attendance Range"
        
        # Determine fallback date range
        conn = mysql.connector.connect(host="localhost", user="root", password="0000", database="COGNITOAI")
        cursor = conn.cursor()
        cursor.execute("SELECT MIN(date), MAX(date) FROM attendance")
        result = cursor.fetchone()
        conn.close()

        start_date = result[0] if result and result[0] else datetime(2024, 1, 1).date()
        end_date = result[1] if result and result[1] else datetime.now().date()

        # Reload dashboard with full data
        self.load_dashboard_summary()
        self.load_attendance_records()
        self.load_editable_attendance()
        self.load_attendance_range_list()
        self.generate_overall_stats(start_date, end_date, None, None)
        self.generate_individual_trend(start_date, end_date, None)
        self.generate_attendance_heatmap(start_date, end_date)
        self.generate_daily_attendance_rate(start_date, end_date)
        
        toast("Filters reset. Dashboard reloaded.")


    def start_camera(self):
        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.update_camera, 1.0 / 30.0)

    def update_camera(self, dt):
        if not self.capture:
            return
        ret, frame = self.capture.read()
        if ret:
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(cv2.flip(frame, 0).tobytes(), colorfmt='bgr', bufferfmt='ubyte')
            self.root.ids.screen_manager.get_screen("face_recognition").ids.camera_feed.texture = texture

    def recognize_faces(self):
        if self.capture:
            ret, frame = self.capture.read()
            if ret:
                data = self.attendance.recognize_from_image(frame)
                if data:
                    self.show_recognition_dialog(data)
                else:
                    self.show_dialog("No faces recognized", "Please try again with a different image.")

    def mark_attendance_from_camera(self):
        if self.capture:
            ret, frame = self.capture.read()
            if ret:
                data = self.attendance.recognize_from_image(frame)
                if data:
                    recognized = []
                    for roll, conf in data:
                        name = self.get_student_name(roll)
                        recognized.append({"roll_no": roll, "name": name, "confidence": round(conf, 2)})
                    self.show_attendance_confirmation(recognized)
                else:
                    self.show_dialog("No students recognized", "Try again.")

    def show_attendance_confirmation(self, recognized_students):
        message = "The following students were recognized:\n\n"
        for student in recognized_students:
            message += f"{student['name']} ({student['confidence']}%) (Roll No: {student['roll_no']})\n"
        message += "\nDo you want to mark them present?"

        self.pending_recognized = recognized_students
        self.dialog = MDDialog(
            title="Confirm Attendance Marking",
            text=message,
            buttons=[
                MDFlatButton(text="Cancel", on_release=lambda x: self.dialog.dismiss()),
                MDRaisedButton(text="Mark Present", on_release=self.confirm_attendance)
            ]
        )
        self.dialog.open()

    def confirm_attendance(self, instance):
        self.dialog.dismiss()
        today = date.today().strftime('%Y-%m-%d')

        conn = mysql.connector.connect(host="localhost", user="root", password="0000", database="COGNITOAI")
        cursor = conn.cursor()

        cursor.execute("SELECT roll_no FROM student_info")
        all_rolls = [row[0] for row in cursor.fetchall()]
        # present_rolls = [s['roll_no'] for s in self.pending_recognized]
        present_rolls = [str(s['roll_no']) for s in self.pending_recognized]
        print("Present rolls:", present_rolls)


        for roll in all_rolls:
            roll = str(roll).strip()
            cursor.execute("SELECT * FROM attendance WHERE roll_no = %s AND date = %s", (roll, today))
            if cursor.fetchone():
                continue
            status = 'P' if roll in present_rolls else 'A'
            cursor.execute("INSERT INTO attendance (roll_no, date, attendance) VALUES (%s, %s, %s)", (roll, today, status))
            print(f"Marking {roll} as {'Present' if status == 'P' else 'Absent'}")


        conn.commit()
        conn.close()

        toast("Attendance successfully marked.")

    def upload_group_photo(self):
        filechooser.open_file(on_selection=self.process_image)

    def process_image(self, selection):
        if selection:
            image = cv2.imread(selection[0])
            data = self.attendance.recognize_from_image(image)
            if data:
                recognized = []
                for roll, conf in data:
                    name = self.get_student_name(roll)
                    recognized.append({"roll_no": roll, "name": name, "confidence": round(conf, 2)})
                self.show_attendance_confirmation(recognized)
            else:
                self.show_dialog("No students recognized", "Try again.")


    def show_recognition_dialog(self, data):
        content = MDBoxLayout(orientation="vertical", spacing="12dp")
        for roll, conf in data:
            name = self.get_student_name(roll)
            content.add_widget(MDLabel(text=f"{name} ({roll}) - {conf:.1f}%", theme_text_color="Primary"))
        self.dialog = MDDialog(title="Recognized Faces", type="custom", content_cls=content,
                               buttons=[MDFlatButton(text="Close", on_release=lambda x: self.dialog.dismiss())])
        self.dialog.open()

    def open_store_face_dialog(self, *args):
        dialog = StoreFaceDialog()
        dialog.open()

    def get_student_name(self, roll):
        conn = mysql.connector.connect(host="localhost", user="root", password="0000", database="COGNITOAI")
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM student_info WHERE roll_no=%s", (roll,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else "Unknown"

    def show_dialog(self, title, text):
        self.dialog = MDDialog(title=title, text=text, buttons=[MDFlatButton(text="OK", on_release=lambda x: self.dialog.dismiss())])
        self.dialog.open()

    def show_date_picker(self, field):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=lambda instance, value, date_range: self.on_date_save(field, value))
        date_dialog.open()

    def on_date_save(self, field, value):
        screen = self.root.ids.screen_manager.get_screen("dashboard")
        if field == "start":
            screen.start_date = value
            self.root.ids.screen_manager.get_screen("dashboard").ids.start_date.text = value.strftime('%Y-%m-%d')
        else:
            screen.end_date = value
            self.root.ids.screen_manager.get_screen("dashboard").ids.end_date.text = value.strftime('%Y-%m-%d')

    def show_student_dropdown(self, caller):
        conn = mysql.connector.connect(host="localhost", user="root", password="0000", database="COGNITOAI")
        cursor = conn.cursor()
        cursor.execute("SELECT roll_no, name FROM student_info")
        students = [(row[0], row[1]) for row in cursor.fetchall()]
        conn.close()

        menu_items = [
            {
                "text": f"{name} ({roll})",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=(roll, name): self.set_student(x)
            } for roll, name in students
        ]
        menu_items.append({
            "text": "All Students",
            "viewclass": "OneLineListItem",
            "on_release": lambda x=None: self.set_student(None)
        })

        self.student_menu = MDDropdownMenu(
            caller=caller,
            items=menu_items,
            width_mult=4,
        )
        self.student_menu.open()

    def show_course_dropdown(self, caller):
        conn = mysql.connector.connect(host="localhost", user="root", password="0000", database="COGNITOAI")
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT course FROM student_info")
        courses = [row[0] for row in cursor.fetchall()]
        conn.close()

        menu_items = [
            {
                "text": course,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=course: self.set_course(x)
            } for course in courses
        ]
        menu_items.append({
            "text": "All Courses",
            "viewclass": "OneLineListItem",
            "on_release": lambda x=None: self.set_course(None)
        })

        self.course_menu = MDDropdownMenu(
            caller=caller,
            items=menu_items,
            width_mult=4,
        )
        self.course_menu.open()


    def show_attendance_range_dropdown(self, caller):
        ranges = [
            ("Below 50%", (0, 50)),
            ("50% to 70%", (50, 70)),
            ("Above 75%", (75, 100)),
            ("All Ranges", None)
        ]
        menu_items = [
            {
                "text": range_name,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=range_val, y=range_name: self.set_attendance_range(x, y)
            } for range_name, range_val in ranges
        ]
        self.attendance_range_menu = MDDropdownMenu(
            caller=caller,
            items=menu_items,
            width_mult=4,
        )
        self.attendance_range_menu.open()

    def set_attendance_range(self, range_val, range_name):
        screen = self.root.ids.screen_manager.get_screen("dashboard")
        screen.selected_attendance_range = range_val
        screen.ids.attendance_range_dropdown.text = range_name  # Update dropdown text
        if self.attendance_range_menu:
            self.attendance_range_menu.dismiss()
        self.update_dashboard()  # Refresh dashboard to apply the filter

    def set_student(self, student):
        screen = self.root.ids.screen_manager.get_screen("dashboard")
        screen.selected_student = student
        if student:
            self.root.ids.screen_manager.get_screen("dashboard").ids.student_dropdown.text = f"{student[1]} ({student[0]})"
        else:
            self.root.ids.screen_manager.get_screen("dashboard").ids.student_dropdown.text = "All Students"
        self.student_menu.dismiss()

    def set_course(self, course):
        screen = self.root.ids.screen_manager.get_screen("dashboard")
        screen.selected_course = course
        self.root.ids.screen_manager.get_screen("dashboard").ids.course_dropdown.text = course if course else "All Courses"
        self.course_menu.dismiss()

    def update_dashboard(self):
        screen = self.root.ids.screen_manager.get_screen("dashboard")

        # Determine filtering mode
        start_date = screen.start_date
        end_date = screen.end_date
        selected_student = screen.selected_student
        selected_course = screen.selected_course
        selected_attendance_range = screen.selected_attendance_range

        # Set fallback range if dates are not selected
        if not start_date or not end_date:
            conn = mysql.connector.connect(host="localhost", user="root", password="0000", database="COGNITOAI")
            cursor = conn.cursor()
            cursor.execute("SELECT MIN(date), MAX(date) FROM attendance")
            result = cursor.fetchone()
            conn.close()

            if result and result[0] and result[1]:
                start_date = result[0]
                end_date = result[1]
            else:
                toast("No attendance records found.")
                return

        # Handle student-specific graphs
        if selected_student:
            self.generate_individual_trend(start_date, end_date, selected_student)
            self.generate_overall_stats(start_date, end_date, selected_student, selected_course)
        else:
            self.generate_individual_trend(start_date, end_date, None)
            self.generate_overall_stats(start_date, end_date, None, selected_course)
            self.generate_attendance_heatmap(start_date, end_date)

        # Generate the daily attendance rate graph (not student-specific)
        self.generate_daily_attendance_rate(start_date, end_date)

        # Always load summary and records
        self.load_dashboard_summary()
        self.load_attendance_records()
        self.load_editable_attendance()
        self.load_attendance_range_list()  # Load attendance range list

    def export_filtered_data_to_csv(self):
        from datetime import datetime
        screen = self.root.ids.screen_manager.get_screen("dashboard")
        start_date = screen.start_date
        end_date = screen.end_date
        selected_student = screen.selected_student
        selected_course = screen.selected_course
        selected_attendance_range = screen.selected_attendance_range

        # Set fallback date range if not provided
        if not start_date or not end_date:
            conn = mysql.connector.connect(host="localhost", user="root", password="0000", database="COGNITOAI")
            cursor = conn.cursor()
            cursor.execute("SELECT MIN(date), MAX(date) FROM attendance")
            result = cursor.fetchone()
            conn.close()
            start_date = result[0] if result and result[0] else datetime(2024, 1, 1).date()
            end_date = result[1] if result and result[1] else datetime.now().date()

        # Build the query
        query = """
            SELECT a.date, a.roll_no, s.name, s.course, a.attendance,
                # COUNT(CASE WHEN a2.attendance = 'P' THEN 1 END) * 100.0 / COUNT(a2.*) AS attendance_percentage
                # COUNT(CASE WHEN a2.attendance = 'P' THEN 1 END) * 100.0 / COUNT(a2.attendance) AS attendance_percentage
            FROM attendance a
            JOIN student_info s ON a.roll_no = s.roll_no
            LEFT JOIN attendance a2 ON a.roll_no = a2.roll_no
            WHERE a.date BETWEEN %s AND %s
        """
        query += " GROUP BY a.date, a.roll_no, s.name, s.course, a.attendance ORDER BY a.date DESC"
        params = [start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')]

        if selected_student:
            query += " AND a.roll_no = %s"
            params.append(selected_student[0])
        if selected_course:
            query += " AND s.course = %s"
            params.append(selected_course)
        if selected_attendance_range:
            min_percent, max_percent = selected_attendance_range
            query += """
                AND a.roll_no IN (
                    SELECT sub.roll_no
                    FROM (
                        SELECT a2.roll_no,
                            COUNT(CASE WHEN a2.attendance = 'P' THEN 1 END) * 100.0 / COUNT(*) AS percentage
                        FROM attendance a2
                        WHERE a2.date BETWEEN %s AND %s
                        GROUP BY a2.roll_no
                        HAVING percentage BETWEEN %s AND %s
                    ) sub
                )
            """
            params.extend([start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'), min_percent, max_percent])

        query += " GROUP BY a.date, a.roll_no, s.name, s.course, a.attendance ORDER BY a.date DESC"

        # Execute query
        conn = mysql.connector.connect(host="localhost", user="root", password="0000", database="COGNITOAI")
        cursor = conn.cursor()
        cursor.execute(query, params)
        data = cursor.fetchall()
        conn.close()

        if not data:
            toast("No data available to export.")
            return

        # Create DataFrame
        df = pd.DataFrame(data, columns=['Date', 'Roll No', 'Name', 'Course', 'Attendance', 'Attendance Percentage'])
        df['Attendance Percentage'] = df['Attendance Percentage'].round(2)

        # Define default filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"attendance_export_{timestamp}.csv"

        # Open file chooser to select save location
        def save_csv(selection):
            if selection:
                file_path = selection[0]
                if not file_path.endswith('.csv'):
                    file_path += '.csv'
                try:
                    df.to_csv(file_path, index=False)
                    toast(f"Data exported successfully to {file_path}")
                except Exception as e:
                    toast(f"Error exporting CSV: {e}")
            else:
                toast("Export cancelled.")

        filechooser.save_file(on_selection=save_csv, title="Save CSV File", filters=[("CSV Files", "*.csv")], filename=default_filename)

    def generate_daily_attendance_rate(self, start_date, end_date):
        conn = mysql.connector.connect(host="localhost", user="root", password="0000", database="COGNITOAI")
        cursor = conn.cursor()

        # Handle None values with fallback
        if start_date is None or end_date is None:
            cursor.execute("SELECT MIN(date), MAX(date) FROM attendance")
            result = cursor.fetchone()
            start_date = result[0] if result and result[0] else datetime(2024, 1, 1).date()
            end_date = result[1] if result and result[1] else datetime.now().date()

        screen = self.root.ids.screen_manager.get_screen("dashboard")
        selected_attendance_range = screen.selected_attendance_range

        query = """
            SELECT a.date, 
                COUNT(CASE WHEN a.attendance = 'P' THEN 1 END) * 100.0 / COUNT(*) as attendance_rate
            FROM attendance a
            JOIN student_info s ON a.roll_no = s.roll_no
            WHERE a.date BETWEEN %s AND %s
        """
        params = [start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')]

        if selected_attendance_range:
            min_percent, max_percent = selected_attendance_range
            query += """
                AND a.roll_no IN (
                    SELECT sub.roll_no
                    FROM (
                        SELECT a2.roll_no,
                               COUNT(CASE WHEN a2.attendance = 'P' THEN 1 END) * 100.0 / COUNT(*) AS percentage
                        FROM attendance a2
                        WHERE a2.date BETWEEN %s AND %s
                        GROUP BY a2.roll_no
                        HAVING percentage BETWEEN %s AND %s
                    ) sub
                )
            """
            params.extend([start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'), min_percent, max_percent])

        query += " GROUP BY a.date ORDER BY a.date"

        cursor.execute(query, params)
        data = cursor.fetchall()
        conn.close()

        if not data:
            toast("No data for daily attendance rate.")
            return

        df = pd.DataFrame(data, columns=['Date', 'AttendanceRate'])
        df['Date'] = pd.to_datetime(df['Date'])

        plt.figure(figsize=(5, 3.5))
        sns.lineplot(data=df, x='Date', y='AttendanceRate', marker='o', color='teal')
        plt.title("Daily Attendance Rate", fontsize=12)
        plt.xlabel("Date", fontsize=10)
        plt.ylabel("Attendance Rate (%)", fontsize=10)
        plt.xticks(rotation=45, fontsize=8)
        plt.yticks(fontsize=8)
        plt.grid(True)
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        image = CoreImage(buf, ext='png')
        self.root.ids.screen_manager.get_screen("dashboard").ids.daily_attendance_rate.texture = image.texture
        buf.close()

    def generate_overall_stats(self, start_date, end_date, selected_student, selected_course):
        conn = mysql.connector.connect(host="localhost", user="root", password="0000", database="COGNITOAI")
        cursor = conn.cursor()

        # Handle None values with fallback
        if start_date is None or end_date is None:
            cursor.execute("SELECT MIN(date), MAX(date) FROM attendance")
            result = cursor.fetchone()
            start_date = result[0] if result and result[0] else datetime(2024, 1, 1).date()
            end_date = result[1] if result and result[1] else datetime.now().date()

        screen = self.root.ids.screen_manager.get_screen("dashboard")
        selected_attendance_range = screen.selected_attendance_range

        query = """
            SELECT a.attendance, COUNT(*) 
            FROM attendance a
            JOIN student_info s ON a.roll_no = s.roll_no
            WHERE a.date BETWEEN %s AND %s
        """
        params = [start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')]

        if selected_student:
            query += " AND a.roll_no = %s"
            params.append(selected_student[0])
        if selected_course:
            query += " AND s.course = %s"
            params.append(selected_course)
        if selected_attendance_range:
            min_percent, max_percent = selected_attendance_range
            query += """
                AND a.roll_no IN (
                    SELECT sub.roll_no
                    FROM (
                        SELECT a2.roll_no,
                               COUNT(CASE WHEN a2.attendance = 'P' THEN 1 END) * 100.0 / COUNT(*) AS percentage
                        FROM attendance a2
                        WHERE a2.date BETWEEN %s AND %s
                        GROUP BY a2.roll_no
                        HAVING percentage BETWEEN %s AND %s
                    ) sub
                )
            """
            params.extend([start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'), min_percent, max_percent])

        query += " GROUP BY a.attendance"

        cursor.execute(query, params)
        data = cursor.fetchall()
        conn.close()

        if not data:
            toast("No data found for overall stats.")
            return

        df = pd.DataFrame(data, columns=['Attendance', 'Count'])

        sns.set_style("whitegrid")
        plt.figure(figsize=(5, 3.5))
        chart = sns.barplot(data=df, x='Attendance', y='Count', palette='pastel')
        chart.bar_label(chart.containers[0], fontsize=8)
        plt.title("Attendance Stats", fontsize=12)
        plt.xlabel("Attendance", fontsize=10)
        plt.ylabel("Count", fontsize=10)
        plt.xticks(fontsize=8)
        plt.yticks(fontsize=8)
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)

        image = CoreImage(buf, ext='png')
        self.root.ids.screen_manager.get_screen("dashboard").ids.overall_stats.texture = image.texture
        buf.close()


    def generate_individual_trend(self, start_date, end_date, selected_student):
        conn = mysql.connector.connect(host="localhost", user="root", password="0000", database="COGNITOAI")
        cursor = conn.cursor()

        # Handle None values with fallback
        if start_date is None or end_date is None:
            cursor.execute("SELECT MIN(date), MAX(date) FROM attendance")
            result = cursor.fetchone()
            start_date = result[0] if result and result[0] else datetime(2024, 1, 1).date()
            end_date = result[1] if result and result[1] else datetime.now().date()

        screen = self.root.ids.screen_manager.get_screen("dashboard")
        selected_attendance_range = screen.selected_attendance_range

        query = """
            SELECT a.date, a.attendance 
            FROM attendance a
            JOIN student_info s ON a.roll_no = s.roll_no
            WHERE a.date BETWEEN %s AND %s
        """
        params = [start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')]

        if selected_student:
            query += " AND a.roll_no = %s"
            params.append(selected_student[0])
        elif selected_attendance_range:
            min_percent, max_percent = selected_attendance_range
            query += """
                AND a.roll_no IN (
                    SELECT sub.roll_no
                    FROM (
                        SELECT a2.roll_no,
                               COUNT(CASE WHEN a2.attendance = 'P' THEN 1 END) * 100.0 / COUNT(*) AS percentage
                        FROM attendance a2
                        WHERE a2.date BETWEEN %s AND %s
                        GROUP BY a2.roll_no
                        HAVING percentage BETWEEN %s AND %s
                    ) sub
                )
            """
            params.extend([start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'), min_percent, max_percent])

        cursor.execute(query, params)
        data = cursor.fetchall()
        conn.close()

        if not data:
            toast("No individual attendance data.")
            return

        df = pd.DataFrame(data, columns=['Date', 'Attendance'])
        df['Date'] = pd.to_datetime(df['Date'])
        df.sort_values('Date', inplace=True)
        df['AttendanceNum'] = df['Attendance'].map({'P': 1, 'A': 0})

        plt.figure(figsize=(5, 3.5))
        sns.lineplot(data=df, x='Date', y='AttendanceNum', marker='o')
        plt.yticks([0, 1], ['Absent', 'Present'], fontsize=8)
        plt.title("Attendance Trend", fontsize=12)
        plt.xlabel("Date", fontsize=10)
        plt.ylabel("Status", fontsize=10)
        plt.xticks(rotation=45, fontsize=8)
        plt.grid(True)
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)

        image = CoreImage(buf, ext='png')
        self.root.ids.screen_manager.get_screen("dashboard").ids.individual_trend.texture = image.texture
        buf.close()

    def generate_attendance_heatmap(self, start_date, end_date):
        conn = mysql.connector.connect(host="localhost", user="root", password="0000", database="COGNITOAI")
        cursor = conn.cursor()

        # Handle None values with fallback
        if start_date is None or end_date is None:
            cursor.execute("SELECT MIN(date), MAX(date) FROM attendance")
            result = cursor.fetchone()
            start_date = result[0] if result and result[0] else datetime(2024, 1, 1).date()
            end_date = result[1] if result and result[1] else datetime.now().date()

        screen = self.root.ids.screen_manager.get_screen("dashboard")
        selected_attendance_range = screen.selected_attendance_range

        query = """
            SELECT a.date, a.attendance 
            FROM attendance a
            JOIN student_info s ON a.roll_no = s.roll_no
            WHERE a.date BETWEEN %s AND %s
        """
        params = [start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')]

        if selected_attendance_range:
            min_percent, max_percent = selected_attendance_range
            query += """
                AND a.roll_no IN (
                    SELECT sub.roll_no
                    FROM (
                        SELECT a2.roll_no,
                               COUNT(CASE WHEN a2.attendance = 'P' THEN 1 END) * 100.0 / COUNT(*) AS percentage
                        FROM attendance a2
                        WHERE a2.date BETWEEN %s AND %s
                        GROUP BY a2.roll_no
                        HAVING percentage BETWEEN %s AND %s
                    ) sub
                )
            """
            params.extend([start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'), min_percent, max_percent])

        cursor.execute(query, params)
        data = cursor.fetchall()
        conn.close()

        if not data:
            toast("No data for heatmap.")
            return

        df = pd.DataFrame(data, columns=["Date", "Attendance"])
        df['Date'] = pd.to_datetime(df['Date'])
        df['Day'] = df['Date'].dt.date
        df['Count'] = df['Attendance'].map({'P': 1, 'A': 0})

        heatmap_df = df.groupby('Day').agg({'Count': 'sum'}).reset_index()
        heatmap_df = heatmap_df.set_index('Day')

        plt.figure(figsize=(5, 3.5))
        sns.heatmap(heatmap_df.T, cmap='YlGnBu', cbar=True, linewidths=0.5, annot=True, fmt='.0f', annot_kws={"size": 8})
        plt.title("Daily Present Count", fontsize=12)
        plt.yticks(rotation=0, fontsize=8)
        plt.xticks(rotation=45, fontsize=8)
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        image = CoreImage(buf, ext='png')
        self.root.ids.screen_manager.get_screen("dashboard").ids.heatmap_graph.texture = image.texture
        buf.close()

    def load_dashboard_summary(self):
        screen = self.root.ids.screen_manager.get_screen("dashboard")
        conn = mysql.connector.connect(host="localhost", user="root", password="0000", database="COGNITOAI")
        cursor = conn.cursor()

        # Total Students
        cursor.execute("SELECT COUNT(*) FROM student_info")
        screen.ids.total_students.text = str(cursor.fetchone()[0])

        # Total Attendance Records
        cursor.execute("SELECT COUNT(*) FROM attendance")
        screen.ids.total_records.text = str(cursor.fetchone()[0])

        # Class Average Attendance
        cursor.execute("""
            SELECT AVG(sub.att_rate) FROM (
                SELECT COUNT(CASE WHEN attendance = 'P' THEN 1 END) / COUNT(*) * 100 as att_rate
                FROM attendance GROUP BY roll_no
            ) as sub
        """)
        avg = cursor.fetchone()[0]
        screen.ids.class_avg.text = f"{round(avg or 0, 2)}%"

        # Load top 5 students
        cursor.execute("""
            SELECT s.name, s.roll_no,
                COUNT(CASE WHEN a.attendance = 'P' THEN 1 END) AS present_days,
                COUNT(*) AS total_days,
                COUNT(CASE WHEN a.attendance = 'P' THEN 1 END) * 100.0 / COUNT(*) AS percentage
            FROM student_info s
            JOIN attendance a ON s.roll_no = a.roll_no
            GROUP BY s.roll_no
            ORDER BY present_days DESC
            LIMIT 5

        """)
        data = cursor.fetchall()
        conn.close()

        icons = ['medal', 'medal-outline', 'medal-outline', 'star-outline', 'star-outline']
        colors = [
            (1, 0.84, 0, 1),     # Gold
            (0.75, 0.75, 0.75, 1),  # Silver
            (0.8, 0.5, 0.2, 1),  # Bronze
            (0.3, 0.5, 0.9, 1),  # Blue
            (0.3, 0.8, 0.3, 1)   # Green
        ]

        leaderboard = screen.ids.leaderboard_cards  # ✅ Fix: define it here
        leaderboard.clear_widgets()  # Optional: clear previous entries

        for i, row in enumerate(data):

            name, roll, present_days, total_days, percentage = row


            card = MDCard(
                orientation='horizontal',
                padding="8dp",
                size_hint_y=None,
                height="48dp",
                md_bg_color=(1, 1, 1, 0.05),
                radius=[12, 12, 12, 12]
            )

            icon = MDIconButton(
                icon=icons[i],
                theme_text_color="Custom",
                text_color=colors[i],
                icon_size="24sp"
            )

            name_label = MDLabel(
                text=f"{name} ({roll})",
                halign="left",
                theme_text_color="Primary"
            )

            count_label = MDLabel(
                text=f"{present_days} Days | {percentage:.1f}%",
                halign="right",
                theme_text_color="Secondary"
            )


            card.add_widget(icon)
            card.add_widget(name_label)
            card.add_widget(count_label)
            leaderboard.add_widget(card)


    def load_attendance_records(self):
        screen = self.root.ids.screen_manager.get_screen("dashboard")
        attendance_list = screen.ids.attendance_list
        attendance_list.clear_widgets()

        conn = mysql.connector.connect(host="localhost", user="root", password="0000", database="COGNITOAI")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.date, a.roll_no, s.name, a.attendance
            FROM attendance a
            JOIN student_info s ON a.roll_no = s.roll_no
            ORDER BY a.date DESC
            LIMIT 50
        """)
        data = cursor.fetchall()
        conn.close()

        from kivymd.uix.list import OneLineAvatarIconListItem, IconLeftWidget

        for date_, roll, name, status in data:
            icon = "check-circle" if status == 'P' else "close-circle"
            icon_color = (0, 0.6, 0, 1) if status == 'P' else (0.8, 0, 0, 1)

            item = OneLineAvatarIconListItem(text=f"{date_} - {name} ({roll}) - {status}")
            item.add_widget(IconLeftWidget(icon=icon, theme_text_color="Custom", text_color=icon_color))
            attendance_list.add_widget(item)

    def load_editable_attendance(self):
        from kivymd.uix.list import TwoLineRightIconListItem, IconRightWidget
        screen = self.root.ids.screen_manager.get_screen("dashboard")
        editable_list = screen.ids.edit_attendance_list
        editable_list.clear_widgets()

        today = datetime.now().strftime('%Y-%m-%d')

        conn = mysql.connector.connect(host="localhost", user="root", password="0000", database="COGNITOAI")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.roll_no, s.name, a.attendance
            FROM attendance a
            JOIN student_info s ON a.roll_no = s.roll_no
            WHERE a.date = %s
            ORDER BY s.roll_no
        """, (today,))
        records = cursor.fetchall()
        conn.close()

        for roll, name, status in records:
            item = TwoLineRightIconListItem(
                text=f"{name} ({roll})",
                secondary_text=f"Status: {'Present' if status == 'P' else 'Absent'}"
            )

            icon = IconRightWidget(
                icon='swap-horizontal',  # looks like a toggle
                on_release=lambda instance, r=roll, n=name, s=status: self.confirm_toggle_attendance(r, n, s)

            )

            item.add_widget(icon)
            editable_list.add_widget(item)

    def load_attendance_range_list(self):
        screen = self.root.ids.screen_manager.get_screen("dashboard")
        attendance_list = screen.ids.attendance_range_list
        attendance_list.clear_widgets()

        start_date = screen.start_date
        end_date = screen.end_date
        selected_course = screen.selected_course
        selected_attendance_range = screen.selected_attendance_range

        # Set default date range if not provided
        if not start_date or not end_date:
            conn = mysql.connector.connect(host="localhost", user="root", password="0000", database="COGNITOAI")
            cursor = conn.cursor()
            cursor.execute("SELECT MIN(date), MAX(date) FROM attendance")
            result = cursor.fetchone()
            conn.close()
            start_date = result[0] if result and result[0] else datetime(2024, 1, 1).date()
            end_date = result[1] if result and result[1] else datetime.now().date()

        conn = mysql.connector.connect(host="localhost", user="root", password="0000", database="COGNITOAI")
        cursor = conn.cursor()

        query = """
            SELECT s.roll_no, s.name, s.course,
                COUNT(CASE WHEN a.attendance = 'P' THEN 1 END) * 100.0 / COUNT(*) AS percentage
            FROM student_info s
            LEFT JOIN attendance a ON s.roll_no = a.roll_no
            WHERE a.date BETWEEN %s AND %s
        """
        params = [start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')]

        if selected_course:
            query += " AND s.course = %s"
            params.append(selected_course)

        query += " GROUP BY s.roll_no, s.name, s.course HAVING percentage IS NOT NULL"

        cursor.execute(query, params)
        data = cursor.fetchall()
        conn.close()

        from kivymd.uix.list import OneLineAvatarIconListItem, IconLeftWidget

        filtered_data = []
        if selected_attendance_range:
            min_percent, max_percent = selected_attendance_range
            filtered_data = [
                row for row in data
                if min_percent <= row[3] <= max_percent
            ]
        else:
            filtered_data = data

        for roll, name, course, percentage in filtered_data:
            icon = "account"
            item = OneLineAvatarIconListItem(
                text=f"{name} ({roll}) - {course} - {percentage:.1f}%"
            )
            item.add_widget(IconLeftWidget(icon=icon))
            attendance_list.add_widget(item)

        if not filtered_data:
            item = OneLineAvatarIconListItem(text="No students found for the selected range.")
            item.add_widget(IconLeftWidget(icon="information-outline"))
            attendance_list.add_widget(item)

    def toggle_attendance(self, roll_no, current_status):
        today = datetime.now().strftime('%Y-%m-%d')
        new_status = 'A' if current_status == 'P' else 'P'

        conn = mysql.connector.connect(host="localhost", user="root", password="0000", database="COGNITOAI")
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE attendance SET attendance = %s
            WHERE roll_no = %s AND date = %s
        """, (new_status, roll_no, today))
        conn.commit()
        conn.close()

        toast(f"{roll_no} marked as {'Present' if new_status == 'P' else 'Absent'}")
        self.load_editable_attendance()  # Refresh the list
        self.load_attendance_records()   # Refresh main display
    
    def confirm_toggle_attendance(self, roll_no, name, current_status):
        new_status = 'A' if current_status == 'P' else 'P'
        status_label = "Absent" if new_status == 'A' else "Present"

        dialog = MDDialog(
            title="Confirm Attendance Update",
            text=f"You are about to mark {name} ({roll_no}) as {status_label}.\nDo you want to continue?",
            buttons=[
                MDFlatButton(text="Cancel", on_release=lambda x: dialog.dismiss()),
                MDRaisedButton(
                    text="Confirm",
                    on_release=lambda x: self.finalize_attendance_toggle(dialog, roll_no, new_status)
                ),
            ]
        )
        dialog.open()

    def finalize_attendance_toggle(self, dialog, roll_no, new_status):
        today = datetime.now().strftime('%Y-%m-%d')

        conn = mysql.connector.connect(host="localhost", user="root", password="0000", database="COGNITOAI")
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE attendance SET attendance = %s
            WHERE roll_no = %s AND date = %s
        """, (new_status, roll_no, today))
        conn.commit()
        conn.close()

        dialog.dismiss()
        toast(f"{roll_no} marked as {'Present' if new_status == 'P' else 'Absent'}")
        self.load_editable_attendance()
        self.load_attendance_records()

    def start_add_student_camera(self):
        if not hasattr(self, 'add_student_capture') or not self.add_student_capture:
            self.add_student_capture = cv2.VideoCapture(0)
            Clock.schedule_interval(self.update_add_student_camera, 1.0 / 30.0)
        toast("Camera started.")

    def update_add_student_camera(self, dt):
        if not hasattr(self, 'add_student_capture') or not self.add_student_capture:
            return
        ret, frame = self.add_student_capture.read()
        if ret:
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(cv2.flip(frame, 0).tobytes(), colorfmt='bgr', bufferfmt='ubyte')
            self.root.ids.screen_manager.get_screen("add_student").ids.add_student_camera_feed.texture = texture

    def stop_add_student_camera(self):
        if hasattr(self, 'add_student_capture') and self.add_student_capture:
            self.add_student_capture.release()
            self.add_student_capture = None
            Clock.unschedule(self.update_add_student_camera)
            self.root.ids.screen_manager.get_screen("add_student").ids.add_student_camera_feed.texture = None

    def upload_face_image(self):
        filechooser.open_file(on_selection=self.process_uploaded_face_image)

    def process_uploaded_face_image(self, selection):
        if selection:
            image_path = selection[0]
            image = cv2.imread(image_path)
            if image is None:
                toast("Invalid image file.")
                return
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            encodings = face_recognition.face_encodings(rgb)
            if not encodings:
                toast("No face detected in the image.")
                return
            self.face_image = image
            # Update camera feed to show uploaded image
            texture = Texture.create(size=(image.shape[1], image.shape[0]), colorfmt='bgr')
            texture.blit_buffer(cv2.flip(image, 0).tobytes(), colorfmt='bgr', bufferfmt='ubyte')
            self.root.ids.screen_manager.get_screen("add_student").ids.add_student_camera_feed.texture = texture
            toast("Face image uploaded successfully!")
    
    def capture_face_for_add(self):
        if hasattr(self, 'add_student_capture') and self.add_student_capture:
            ret, frame = self.add_student_capture.read()
            if not ret:
                toast("Failed to capture from camera.")
                return
            self.stop_add_student_camera()
        else:
            toast("Please start the camera first.")
            return

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        encodings = face_recognition.face_encodings(rgb)

        if not encodings:
            toast("No face detected. Try again.")
            return

        self.face_image = frame
        # Update camera feed to show captured image
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(cv2.flip(frame, 0).tobytes(), colorfmt='bgr', bufferfmt='ubyte')
        self.root.ids.screen_manager.get_screen("add_student").ids.add_student_camera_feed.texture = texture
        toast("Face captured successfully!")

    def encode_face(self, image_path):
        try:
            img = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(img)
            return encodings if encodings else None
        except Exception as e:
            print(f"Error encoding face from {image_path}: {e}")
            return None

    def save_new_student(self):
        screen = self.root.ids.screen_manager.get_screen("add_student")
        roll = screen.ids.add_roll.text.strip()
        name = screen.ids.add_name.text.strip()
        course = screen.ids.add_course.text.strip()
        dob = screen.ids.add_dob.text.strip()

        if not roll or not name or not course or not dob or not hasattr(self, 'face_image'):
            toast("Please fill all fields and capture or upload a face")
            return

        # Validate DOB format
        try:
            datetime.strptime(dob, '%Y-%m-%d')
        except ValueError:
            toast("Invalid DOB format. Use YYYY-MM-DD.")
            return

        conn = mysql.connector.connect(host="localhost", user="root", password="0000", database="COGNITOAI")
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM student_info WHERE roll_no = %s", (roll,))
            if cursor.fetchone():
                toast("Student with this roll number already exists.")
                conn.close()
                return

            # Ensure 'faces' directory exists
            os.makedirs("faces", exist_ok=True)

            # Save face image
            image_path = f"faces/{roll}.jpg"
            cv2.imwrite(image_path, self.face_image)

            # Encode face
            face_encodings = self.encode_face(image_path)
            if face_encodings is None:
                toast("No face detected in saved image.")
                os.remove(image_path)
                conn.close()
                return

            # Use .tobytes() for consistency with StoreFaceDialog
            face_data = face_encodings[0].tobytes()

            cursor.execute("""
                INSERT INTO student_info (roll_no, name, course, dob, face_id)
                VALUES (%s, %s, %s, %s, %s)
            """, (roll, name, course, dob, face_data))

            conn.commit()
            toast("Student added successfully!")

            # Clear input fields and reset face_image
            screen.ids.add_roll.text = ""
            screen.ids.add_name.text = ""
            screen.ids.add_course.text = ""
            screen.ids.add_dob.text = ""
            delattr(self, 'face_image')
            self.root.ids.screen_manager.get_screen("add_student").ids.add_student_camera_feed.texture = None

        except mysql.connector.Error as e:
            toast(f"Database error: {e}")
            if os.path.exists(image_path):
                os.remove(image_path)
        finally:
            conn.close()
    def check_roll_availability(self, roll_no):
        roll_no = roll_no.strip()
        if not roll_no:
            return

        conn = mysql.connector.connect(host="localhost", user="root", password="0000", database="COGNITOAI")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM student_info WHERE roll_no = %s", (roll_no,))
        exists = cursor.fetchone()
        conn.close()

        if exists:
            toast("This roll number already exists! Please choose another.")
            # Optionally, clear the field:
            self.root.ids.screen_manager.get_screen("add_student").ids.add_roll.text = ""

    def show_about(self):
        about_dialog = MDDialog(
            title="About CognitoAI",
            text=(
                "CognitoAI is a Facial Recognition-based Attendance System.\n\n"
                "Developed using Python, KivyMD, OpenCV, and MySQL.\n\n"
                "Version: 1.0\nAuthor: Prasoon Tripathi and Akshay Maurya\nContact: admin@cognitoai.com"
            ),
            buttons=[MDFlatButton(text="Close", on_release=lambda x: about_dialog.dismiss())]
        )
        about_dialog.open()


if __name__ == '__main__':
    CognitoAIApp().run()
