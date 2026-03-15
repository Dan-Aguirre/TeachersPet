import customtkinter as ctk

# apperance config
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# colors (same as student page for consistancy)
PURPLE = "#7c5cfc"
PURPLE_DARK = "#5a3fd6"
PURPLE_LIGHT = "#ebe5ff"
BG_COLOR = "#f3f1fa"
CARD_BG = "#ffffff"
TEXT_COLOR = "#2d2b3a"
TEXT_LIGHT = "#7e7b91"
GREEN = "#58CC02"


class TeacherPage(ctk.CTk):
    """Simple Tkinter dashboard for a teacher with a sidebar and dynamic content.

    The sidebar has three buttons: Profile, Classes and Settings.  Clicking one
    of the buttons clears the main content area and rebuilds it with the
    appropriate widgets.  ``teacher_info`` and ``classes_data`` are injected so
    that the class can be used in a real application or for testing.
    """

    def __init__(self, teacher_info: dict, classes_data: dict):
        super().__init__()
        self.title("Teacher's Pet - Teacher Dashboard")
        self.geometry("900x650")
        self.configure(fg_color=BG_COLOR)

        self.teacher_info = teacher_info
        self.classes_data = classes_data

        self._build_sidebar()

        # main content area
        self.main_frame = ctk.CTkScrollableFrame(
            self, fg_color=BG_COLOR,
            corner_radius=0
        )
        self.main_frame.pack(side="right", expand=True, fill="both", padx=(0,10), pady=10)

        self.show_profile()

    def _build_sidebar(self):
        sidebar = ctk.CTkFrame(self, width=220, fg_color=CARD_BG, corner_radius=0)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # title
        title_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        title_frame.pack(fill="x", padx=15, pady=(20,30))

        ctk.CTkLabel(
            title_frame, text="🎓 Teacher's Pet",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=PURPLE
        ).pack(anchor="w")

        ctk.CTkLabel(
            title_frame, text="Teacher View",
            font=ctk.CTkFont(size=11), text_color=TEXT_LIGHT
        ).pack(anchor="w")

        btn_style = {
            "font": ctk.CTkFont(size=14, weight="bold"),
            "corner_radius": 16,
            "height": 44,
            "anchor": "w",
            "fg_color": "transparent",
            "text_color": TEXT_LIGHT,
            "hover_color": PURPLE_LIGHT,
        }

        self.profile_btn = ctk.CTkButton(
            sidebar, text="  👤  Profile",
            command=self.show_profile, **btn_style
        )
        self.profile_btn.pack(fill="x", padx=10, pady=3)

        self.classes_btn = ctk.CTkButton(
            sidebar, text="  📚  Classes",
            command=self.show_classes, **btn_style
        )
        self.classes_btn.pack(fill="x", padx=10, pady=3)

        self.settings_btn = ctk.CTkButton(
            sidebar, text="  ⚙️  Settings",
            command=self.show_settings, **btn_style
        )
        self.settings_btn.pack(fill="x", padx=10, pady=3)

    def _set_active(self, active):
        """sets which sidebar btn is highlited"""
        btns = [self.profile_btn, self.classes_btn, self.settings_btn]
        for b in btns:
            b.configure(fg_color="transparent", text_color=TEXT_LIGHT)
        active.configure(fg_color=PURPLE_LIGHT, text_color=PURPLE)

    def _clear_main(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_profile(self):
        self._clear_main()
        self._set_active(self.profile_btn)

        # welcom header
        header_card = ctk.CTkFrame(self.main_frame, fg_color=CARD_BG, corner_radius=20)
        header_card.pack(fill="x", pady=(5, 15))

        inner = ctk.CTkFrame(header_card, fg_color="transparent")
        inner.pack(fill="x", padx=20, pady=20)

        ctk.CTkLabel(
            inner, text=f"Welcome, {self.teacher_info.get('username', '')}",
            font=ctk.CTkFont(size=26, weight="bold"), text_color=TEXT_COLOR
        ).pack(anchor="w")

        desc = self.teacher_info.get("description", "")
        ctk.CTkLabel(
            inner, text=f'"{desc}"',
            font=ctk.CTkFont(size=14), text_color=TEXT_LIGHT,
            wraplength=500, justify="left"
        ).pack(anchor="w", pady=(8,0))

        # quick stats
        stats = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        stats.pack(fill="x", pady=5)
        stats.columnconfigure((0,1), weight=1)

        total_students = sum(len(s) for s in self.classes_data.values())
        total_classes = len(self.classes_data)

        # classes count card
        c1 = ctk.CTkFrame(stats, fg_color=CARD_BG, corner_radius=20)
        c1.grid(row=0, column=0, padx=5, sticky="nsew")
        ctk.CTkLabel(c1, text="📚", font=ctk.CTkFont(size=28)).pack(pady=(15,5))
        ctk.CTkLabel(c1, text="My Classes", text_color=TEXT_LIGHT,
                     font=ctk.CTkFont(size=12, weight="bold")).pack()
        ctk.CTkLabel(c1, text=str(total_classes), text_color=PURPLE,
                     font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(0,15))

        # total studnets card
        c2 = ctk.CTkFrame(stats, fg_color=CARD_BG, corner_radius=20)
        c2.grid(row=0, column=1, padx=5, sticky="nsew")
        ctk.CTkLabel(c2, text="👥", font=ctk.CTkFont(size=28)).pack(pady=(15,5))
        ctk.CTkLabel(c2, text="Total Students", text_color=TEXT_LIGHT,
                      font=ctk.CTkFont(size=12, weight="bold")).pack()
        ctk.CTkLabel(c2, text=str(total_students), text_color="#FF9600",
                     font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(0,15))

    def show_classes(self):
        self._clear_main()
        self._set_active(self.classes_btn)

        # header row
        top = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        top.pack(fill="x", pady=(5,15))

        ctk.CTkLabel(
            top, text="My Class Roster",
            font=ctk.CTkFont(size=26, weight="bold"), text_color=TEXT_COLOR
        ).pack(side="left")

        ctk.CTkButton(
            top, text="+ Create Class",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=PURPLE, hover_color=PURPLE_DARK,
            corner_radius=20, height=36,
            command=lambda: print("create class clicked")
        ).pack(side="right")

        # for each class we create a container with a header and a body that can
        # be shown/hidden (the "dropdown").
        for class_name, students in self.classes_data.items():
            card = ctk.CTkFrame(self.main_frame, fg_color=CARD_BG, corner_radius=20)
            card.pack(fill="x", pady=6)

            header = ctk.CTkFrame(card, fg_color="transparent")
            header.pack(fill="x", padx=20, pady=15)

            ctk.CTkLabel(
                header, text=class_name,
                font=ctk.CTkFont(size=18, weight="bold"),
                text_color=TEXT_COLOR
            ).pack(side="left")

            ctk.CTkLabel(
                header, text=f"{len(students)} students",
                font=ctk.CTkFont(size=13), text_color=TEXT_LIGHT
            ).pack(side="left", padx=(15,0))

            toggle = ctk.CTkButton(
                header, text="Show ▼", width=80,
                fg_color=PURPLE_LIGHT, text_color=PURPLE,
                hover_color="#ddd8f0", corner_radius=12,
                font=ctk.CTkFont(size=12, weight="bold"),
                command=lambda n=class_name, c=card: self._toggle_class(n, c)
            )
            toggle.pack(side="right")

            body = ctk.CTkFrame(card, fg_color=BG_COLOR, corner_radius=12)
            card.body = body
            card.showing = False

    def _toggle_class(self, class_name, card):
        """Expand or collapse the student details for a class."""
        if card.showing:
            card.body.pack_forget()
            card.showing = False
            # destroy old widgets so we can rebuild fresh next time
            for w in card.body.winfo_children():
                w.destroy()
        else:
            students = self.classes_data.get(class_name, [])

            # show studnet count at top
            ctk.CTkLabel(
                card.body, text=f"Enrolled: {len(students)} students",
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color=TEXT_LIGHT
            ).pack(anchor="w", padx=20, pady=(10,5))

            # list each student with thier progress
            for name, progress in students:
                row = ctk.CTkFrame(card.body, fg_color="transparent")
                row.pack(fill="x", padx=20, pady=3)

                ctk.CTkLabel(
                    row, text=name,
                    font=ctk.CTkFont(size=14, weight="bold"),
                    text_color=TEXT_COLOR
                ).pack(side="left")

                ctk.CTkLabel(
                    row, text=progress,
                    font=ctk.CTkFont(size=14, weight="bold"),
                    text_color=GREEN
                ).pack(side="right")

            card.body.pack(fill="x", padx=15, pady=(0,10))
            card.showing = True

    def show_settings(self):
        self._clear_main()
        self._set_active(self.settings_btn)

        ctk.CTkLabel(
            self.main_frame, text="Settings",
            font=ctk.CTkFont(size=26, weight="bold"), text_color=TEXT_COLOR
        ).pack(anchor="w", pady=(5,15))

        card = ctk.CTkFrame(self.main_frame, fg_color=CARD_BG, corner_radius=20)
        card.pack(fill="x", pady=5)

        ctk.CTkLabel(card, text="Profile Description",
                     font=ctk.CTkFont(size=15, weight="bold"),
                      text_color=TEXT_COLOR).pack(anchor="w", padx=20, pady=(20,5))

        desc_box = ctk.CTkTextbox(card, height=100, corner_radius=12,
                                  fg_color=BG_COLOR, text_color=TEXT_COLOR,
                                  font=ctk.CTkFont(size=13))
        desc_box.insert("1.0", self.teacher_info.get("description", ""))
        desc_box.pack(fill="x", padx=20, pady=(0,15))

        ctk.CTkButton(
            card, text="💾  Save",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=PURPLE, hover_color=PURPLE_DARK,
            corner_radius=20, height=42,
            command=lambda: print("saved!")
        ).pack(anchor="e", padx=20, pady=(5,20))


def main():
    # example data; in a real application this would come from the server or
    # login flow
    teacher_info = {
        "username": "teacher1",
        "password": "secret",
        "description": "I teach algebra and geometry.",
    }

    classes_data = {
        "Math": [("Alice", "80%"), ("Bob", "90%")],
        "Science": [("Charlie", "70%"), ("Dana", "85%")],
    }

    app = TeacherPage(teacher_info, classes_data)
    app.mainloop()


if __name__ == "__main__":
    main()
