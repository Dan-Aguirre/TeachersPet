import customtkinter as ctk


# set the color theme stuff
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# our purple color pallete (got these from the figma)
PURPLE = "#7c5cfc"
PURPLE_DARK = "#5a3fd6"
PURPLE_LIGHT = "#ebe5ff"
BG_COLOR = "#f3f1fa"
CARD_BG = "#ffffff"
TEXT_COLOR = "#2d2b3a"
TEXT_LIGHT = "#7e7b91"


class StudentPage(ctk.CTk):
    """Simple Tkinter dashboard for a student profile with a sidebar tabs and main content.

    Student sidebar will have four tabs: profile, enrolled classes, ranking, and settings. Pretty similar
    to the teacher's page except that the profile tab will have a friends page, the classes tab will only
    show the classes the student is enrolled in and their current progress and not the full roster,
    and the ranking tab will show the student's ranking in each class and overall. Settings page will
    allow student to modify their profile information and manage their friends list.

    IMPORTANT: For now, the data is read-only and hardcoded, but in a real application this
    will be dynamic and the user will be able to directly modify their profile and class
    information.
    """

    def __init__(self, student_info: dict, classes_data: dict):
        super().__init__()
        self.title("Teacher's Pet - Student Dashboard")
        self.geometry("900x650")
        self.configure(fg_color=BG_COLOR)

        self.student_info = student_info
        self.classes_data = classes_data

        self._build_sidebar()

        # main content frame on the right side
        self.main_frame = ctk.CTkScrollableFrame(
            self, fg_color=BG_COLOR,
            corner_radius=0
        )
        self.main_frame.pack(side="right", expand=True, fill="both", padx=(0,10), pady=10)

        # show profile by defualt when app opens
        self.show_profile()

    def _build_sidebar(self):
        sidebar = ctk.CTkFrame(self, width=220, fg_color=CARD_BG, corner_radius=0)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # app title at top of sidebar
        title_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        title_frame.pack(fill="x", padx=15, pady=(20, 30))

        ctk.CTkLabel(
            title_frame, text="🎓 Teacher's Pet",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=PURPLE
        ).pack(anchor="w")

        # sidebar buttons
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

        self.rank_btn = ctk.CTkButton(
            sidebar, text="  🏆  Rankings",
            command=self.show_rankings, **btn_style
        )
        self.rank_btn.pack(fill="x", padx=10, pady=3)

        self.settings_btn = ctk.CTkButton(
            sidebar, text="  ⚙️  Settings",
            command=self.show_settings, **btn_style
        )
        self.settings_btn.pack(fill="x", padx=10, pady=3)

    def _set_active_btn(self, active_btn):
        """highlight the active sidebar button and reset the othres"""
        all_btns = [self.profile_btn, self.classes_btn, self.rank_btn, self.settings_btn]
        for btn in all_btns:
            btn.configure(fg_color="transparent", text_color=TEXT_LIGHT)

        active_btn.configure(fg_color=PURPLE_LIGHT, text_color=PURPLE)

    def _clear_main(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_profile(self):
        self._clear_main()
        self._set_active_btn(self.profile_btn)

        # header with username
        header = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        header.pack(fill="x", pady=(5,15))

        ctk.CTkLabel(
            header, text=self.student_info.get("username", ""),
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=TEXT_COLOR
        ).pack(anchor="w")
        ctk.CTkLabel(
            header, text="Student Account",
            font=ctk.CTkFont(size=14), text_color=TEXT_LIGHT
        ).pack(anchor="w")

        # stats row
        stats_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        stats_frame.pack(fill="x", pady=10)
        stats_frame.columnconfigure((0,1,2), weight=1)

        # points card
        points_card = ctk.CTkFrame(stats_frame, fg_color=CARD_BG, corner_radius=20)
        points_card.grid(row=0, column=0, padx=5, sticky="nsew")
        ctk.CTkLabel(points_card, text="🏆", font=ctk.CTkFont(size=28)).pack(pady=(15,5))
        ctk.CTkLabel(points_card, text="Total Points", text_color=TEXT_LIGHT,
                     font=ctk.CTkFont(size=12, weight="bold")).pack()
        ctk.CTkLabel(points_card, text="1250", text_color="#FF9600",
                     font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(0,15))

        # games card
        games_card = ctk.CTkFrame(stats_frame, fg_color=CARD_BG, corner_radius=20)
        games_card.grid(row=0, column=1, padx=5, sticky="nsew")
        ctk.CTkLabel(games_card, text="🎯", font=ctk.CTkFont(size=28)).pack(pady=(15,5))
        ctk.CTkLabel(games_card, text="Games Played", text_color=TEXT_LIGHT,
                      font=ctk.CTkFont(size=12, weight="bold")).pack()
        ctk.CTkLabel(games_card, text="42", text_color=PURPLE,
                     font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(0,15))

        # streak card
        streak_card = ctk.CTkFrame(stats_frame, fg_color=CARD_BG, corner_radius=20)
        streak_card.grid(row=0, column=2, padx=5, sticky="nsew")
        ctk.CTkLabel(streak_card, text="🔥", font=ctk.CTkFont(size=28)).pack(pady=(15,5))
        ctk.CTkLabel(streak_card, text="Streak", text_color=TEXT_LIGHT,
                     font=ctk.CTkFont(size=12, weight="bold")).pack()
        ctk.CTkLabel(streak_card, text="5 Days", text_color="#EA2B2B",
                     font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(0,15))

        # about me seciton
        about_card = ctk.CTkFrame(self.main_frame, fg_color=CARD_BG, corner_radius=20)
        about_card.pack(fill="x", pady=(15, 10))

        ctk.CTkLabel(about_card, text="About Me",
                     font=ctk.CTkFont(size=18, weight="bold"),
                     text_color=TEXT_COLOR).pack(anchor="w", padx=20, pady=(15,5))

        # grab the descrption text
        desc_txt = self.student_info.get("description", "")
        ctk.CTkLabel(about_card, text=desc_txt,
                     font=ctk.CTkFont(size=14), text_color=TEXT_LIGHT,
                     wraplength=500, justify="left").pack(anchor="w", padx=20, pady=(0,15))

    def show_classes(self):
        self._clear_main()
        self._set_active_btn(self.classes_btn)

        ctk.CTkLabel(
            self.main_frame, text="My Classes",
            font=ctk.CTkFont(size=26, weight="bold"), text_color=TEXT_COLOR
        ).pack(anchor="w", pady=(5, 15))

        # for each class we create a container with a header and a body that can be shown/hidden (the "dropdown").
        for class_name, students in self.classes_data.items():
            card = ctk.CTkFrame(self.main_frame, fg_color=CARD_BG, corner_radius=20)
            card.pack(fill="x", pady=6)

            # class header row
            header_frame = ctk.CTkFrame(card, fg_color="transparent")
            header_frame.pack(fill="x", padx=20, pady=15)

            ctk.CTkLabel(
                header_frame, text=class_name,
                font=ctk.CTkFont(size=18, weight="bold"), text_color=TEXT_COLOR
            ).pack(side="left")

            # toggle button for expanding
            toggle_btn = ctk.CTkButton(
                header_frame, text="Show ▼", width=80,
                fg_color=PURPLE_LIGHT, text_color=PURPLE,
                hover_color="#ddd8f0", corner_radius=12,
                font=ctk.CTkFont(size=12, weight="bold"),
                command=lambda n=class_name, c=card: self._toggle_class(n, c)
            )
            toggle_btn.pack(side="right")

            # hidden body frame
            body = ctk.CTkFrame(card, fg_color=BG_COLOR, corner_radius=12)
            card.body = body
            card.showing = False

    def _toggle_class(self, class_name, card):
        """Show or hide the current student's progress for a given class."""
        if card.showing:
            card.body.pack_forget()
            card.showing = False
            for w in card.body.winfo_children():
                w.destroy()
        else:
            # look up this student's progress within the class list
            student_name = self.student_info.get("username", "")
            students = self.classes_data.get(class_name, [])

            progress = None
            for name, prog in students:
                if name == student_name:
                    progress = prog
                    break

            if progress is None:
                msg = "You are not enrolled in this class."
            else:
                msg = f"Your current progress: {progress}"

            ctk.CTkLabel(
                card.body, text=msg,
                font=ctk.CTkFont(size=14), text_color=TEXT_COLOR
            ).pack(anchor="w", padx=20, pady=10)

            # add a simple progress bar if we hav progress
            if progress is not None:
                try:
                    prog_val = float(progress) / 100.0
                except ValueError:
                    prog_val = 0.0

                pbar = ctk.CTkProgressBar(card.body, progress_color=PURPLE,
                                          fg_color=PURPLE_LIGHT, corner_radius=10)
                pbar.set(prog_val)
                pbar.pack(fill="x", padx=20, pady=(0, 15))

            card.body.pack(fill="x", padx=15, pady=(0,10))
            card.showing = True

    def show_rankings(self):
        self._clear_main()
        self._set_active_btn(self.rank_btn)

        ctk.CTkLabel(
            self.main_frame, text="Global Rankings",
            font=ctk.CTkFont(size=26, weight="bold"), text_color=TEXT_COLOR
        ).pack(anchor="w", pady=(5,15))

        # hardcoded for now, will replace with api later
        mock_rankings = [
            ("🥇", "math_wizard_99", "4500 XP"),
            ("🥈", "algebra_queen", "4200 XP"),
            ("🥉", "geo_master", "3850 XP"),
            ("  #14", "student1 (You)", "1250 XP"),
        ]

        for medal, name, xp in mock_rankings:
            row = ctk.CTkFrame(self.main_frame, fg_color=CARD_BG, corner_radius=16)
            row.pack(fill="x", pady=4)

            # highlihgt current user
            is_me = "You" in name
            if is_me:
                row.configure(border_width=2, border_color=PURPLE)

            inner = ctk.CTkFrame(row, fg_color="transparent")
            inner.pack(fill="x", padx=15, pady=12)

            ctk.CTkLabel(inner, text=medal, font=ctk.CTkFont(size=20),
                        width=50).pack(side="left")
            ctk.CTkLabel(inner, text=name,
                         font=ctk.CTkFont(size=16, weight="bold"),
                         text_color=PURPLE if is_me else TEXT_COLOR).pack(side="left", padx=10)
            ctk.CTkLabel(inner, text=xp, font=ctk.CTkFont(size=14, weight="bold"),
                        text_color="#FF9600").pack(side="right")

    def show_settings(self):
        self._clear_main()
        self._set_active_btn(self.settings_btn)

        ctk.CTkLabel(
            self.main_frame, text="Settings",
            font=ctk.CTkFont(size=26, weight="bold"), text_color=TEXT_COLOR
        ).pack(anchor="w", pady=(5,15))

        card = ctk.CTkFrame(self.main_frame, fg_color=CARD_BG, corner_radius=20)
        card.pack(fill="x", pady=5)

        # descrption field
        ctk.CTkLabel(card, text="About Me Description",
                     font=ctk.CTkFont(size=15, weight="bold"),
                     text_color=TEXT_COLOR).pack(anchor="w", padx=20, pady=(20,5))

        desc_box = ctk.CTkTextbox(card, height=100, corner_radius=12,
                                  fg_color=BG_COLOR, text_color=TEXT_COLOR,
                                  font=ctk.CTkFont(size=13))
        desc_box.insert("1.0", self.student_info.get("description", ""))
        desc_box.pack(fill="x", padx=20, pady=(0,10))

        # pasword field
        ctk.CTkLabel(card, text="Change Password",
                      font=ctk.CTkFont(size=15, weight="bold"),
                      text_color=TEXT_COLOR).pack(anchor="w", padx=20, pady=(10,5))

        pw_entry = ctk.CTkEntry(card, placeholder_text="New Password", show="*",
                                corner_radius=12, fg_color=BG_COLOR,
                                font=ctk.CTkFont(size=13))
        pw_entry.pack(fill="x", padx=20, pady=(0,10))

        ctk.CTkLabel(card, text="Leave blank to keep current password.",
                     font=ctk.CTkFont(size=11), text_color=TEXT_LIGHT
        ).pack(anchor="w", padx=20, pady=(0,5))

        # save btn
        ctk.CTkButton(
            card, text="💾  Save Changes",
              font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=PURPLE, hover_color=PURPLE_DARK,
            corner_radius=20, height=42,
            command=lambda: print("Settings saved!")
        ).pack(anchor="e", padx=20, pady=(10, 20))


def main():
    # example data; in a real application this would come from the server or
    # login flow
    student_info = {
        "username": "student1",
        "password": "password123",
        "description": "Student in SHS! I am taking pre-calculus and advanced geometry.",
    }

    # class progress data (to be updaetd w/ real api calls)
    classes_data = {
        "Pre-Calculus": [("student1", "45")],
        "Advanced Geometry": [("student1", "78")],
    }

    app = StudentPage(student_info, classes_data)
    app.mainloop()


if __name__ == "__main__":
     main()
