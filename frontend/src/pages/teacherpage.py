import customtkinter as ctk
import threading
import api

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
ORANGE = "#FF9600"
RED = "#EA2B2B"


class TeacherPage(ctk.CTk):
    """Teacher dashboard with sidebar and dynamic content area.

    sidebar has 3 buttons: profile, classes, settings
    all data now comes from the backend via api.py -- no more hardcoded stuff
    """

    def __init__(self, user: dict):
        super().__init__()
        self.title("Teacher's Pet - Teacher Dashboard")
        self.geometry("900x650")
        self.configure(fg_color=BG_COLOR)

        self.user = user
        self.user_id = user["id"]

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

    def _run_async(self, fn, callback):
        """run blocking api call in bg thread -- keeps ui from freezing"""
        def worker():
            result = fn()
            self.after(0, lambda: callback(result))
        threading.Thread(target=worker, daemon=True).start()

    # -- profile tab --------------------------------------------

    def show_profile(self):
        self._clear_main()
        self._set_active(self.profile_btn)

        # welcom header
        header_card = ctk.CTkFrame(self.main_frame, fg_color=CARD_BG, corner_radius=20)
        header_card.pack(fill="x", pady=(5, 15))

        inner = ctk.CTkFrame(header_card, fg_color="transparent")
        inner.pack(fill="x", padx=20, pady=20)

        ctk.CTkLabel(
            inner, text=f"Welcome, {self.user.get('username', '')}",
            font=ctk.CTkFont(size=26, weight="bold"), text_color=TEXT_COLOR
        ).pack(anchor="w")

        desc = self.user.get("description", "")
        ctk.CTkLabel(
            inner, text=f'"{desc}"',
            font=ctk.CTkFont(size=14), text_color=TEXT_LIGHT,
            wraplength=500, justify="left"
        ).pack(anchor="w", pady=(8,0))

        # quick stats
        stats = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        stats.pack(fill="x", pady=5)
        stats.columnconfigure((0,1), weight=1)

        # classes count card
        c1 = ctk.CTkFrame(stats, fg_color=CARD_BG, corner_radius=20)
        c1.grid(row=0, column=0, padx=5, sticky="nsew")
        ctk.CTkLabel(c1, text="📚", font=ctk.CTkFont(size=28)).pack(pady=(15,5))
        ctk.CTkLabel(c1, text="My Classes", text_color=TEXT_LIGHT,
                     font=ctk.CTkFont(size=12, weight="bold")).pack()
        self.classes_count_lbl = ctk.CTkLabel(c1, text="...", text_color=PURPLE,
                     font=ctk.CTkFont(size=24, weight="bold"))
        self.classes_count_lbl.pack(pady=(0,15))

        # total studnets card
        c2 = ctk.CTkFrame(stats, fg_color=CARD_BG, corner_radius=20)
        c2.grid(row=0, column=1, padx=5, sticky="nsew")
        ctk.CTkLabel(c2, text="👥", font=ctk.CTkFont(size=28)).pack(pady=(15,5))
        ctk.CTkLabel(c2, text="Total Students", text_color=TEXT_LIGHT,
                      font=ctk.CTkFont(size=12, weight="bold")).pack()
        self.students_count_lbl = ctk.CTkLabel(c2, text="...", text_color=ORANGE,
                     font=ctk.CTkFont(size=24, weight="bold"))
        self.students_count_lbl.pack(pady=(0,15))

        # fetch classes and count students for each
        self._run_async(
            lambda: api.get_classes(self.user_id),
            self._on_profile_classes_loaded
        )

    def _on_profile_classes_loaded(self, data):
        """get class count then fetch member counts for each"""
        if not data:
            self.classes_count_lbl.configure(text="0")
            self.students_count_lbl.configure(text="0")
            return

        class_list = data.get("teaching", [])
        self.classes_count_lbl.configure(text=str(len(class_list)))

        if not class_list:
            self.students_count_lbl.configure(text="0")
            return

        # fetch member count for all classes -- just count totals
        total_students = 0
        for cls in class_list:
            members = api.get_class_members(cls["id"])
            if members:
                total_students += len(members)

        self.students_count_lbl.configure(text=str(total_students))

    # -- classes tab --------------------------------------------

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
            command=self._create_class
        ).pack(side="right")

        # container for class cards
        self.classes_container = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.classes_container.pack(fill="x")

        ctk.CTkLabel(self.classes_container, text="Loading...",
                     font=ctk.CTkFont(size=14), text_color=TEXT_LIGHT).pack(pady=20)

        self._run_async(
            lambda: api.get_classes(self.user_id),
            self._on_classes_loaded
        )

    def _create_class(self):
        """open a simple dialog to enter class name then call backend"""
        dialog = ctk.CTkInputDialog(text="Enter a name for the new class:",
                                    title="Create Class")
        class_name = dialog.get_input()
        if not class_name or not class_name.strip():
            return

        new_cls = api.create_class(self.user_id, class_name.strip())
        if new_cls:
            # refresh the class list
            self._run_async(
                lambda: api.get_classes(self.user_id),
                self._on_classes_loaded
            )
        else:
            # tried showing a messagebox here but it was causing issues
            # ctk.messagebox.showerror("Error", "could not create class")
            pass

    def _on_classes_loaded(self, data):
        """rebuild class cards from api response"""
        for w in self.classes_container.winfo_children():
            w.destroy()

        if not data:
            ctk.CTkLabel(self.classes_container, text="Could not load classes.",
                         font=ctk.CTkFont(size=14), text_color=TEXT_LIGHT).pack(pady=20)
            return

        class_list = data.get("teaching", [])
        if not class_list:
            ctk.CTkLabel(self.classes_container, text="No classes yet. Create one above!",
                         font=ctk.CTkFont(size=14), text_color=TEXT_LIGHT).pack(pady=20)
            return

        # for each class we create a container with a header and a body that can
        # be shown/hidden (the "dropdown").
        for cls in class_list:
            card = ctk.CTkFrame(self.classes_container, fg_color=CARD_BG, corner_radius=20)
            card.pack(fill="x", pady=6)

            header = ctk.CTkFrame(card, fg_color="transparent")
            header.pack(fill="x", padx=20, pady=15)

            ctk.CTkLabel(
                header, text=cls["name"],
                font=ctk.CTkFont(size=18, weight="bold"),
                text_color=TEXT_COLOR
            ).pack(side="left")

            ctk.CTkLabel(
                header, text=f"Code: {cls['code']}",
                font=ctk.CTkFont(size=13, weight="bold"), text_color=PURPLE
            ).pack(side="left", padx=(15,0))

            toggle = ctk.CTkButton(
                header, text="Show ▼", width=80,
                fg_color=PURPLE_LIGHT, text_color=PURPLE,
                hover_color="#ddd8f0", corner_radius=12,
                font=ctk.CTkFont(size=12, weight="bold"),
                command=lambda c=cls, card_ref=card: self._toggle_class(c["id"], card_ref)
            )
            toggle.pack(side="right")

            body = ctk.CTkFrame(card, fg_color=BG_COLOR, corner_radius=12)
            card.body = body
            card.showing = False

    def _toggle_class(self, class_id, card):
        """Expand or collapse the student details for a class."""
        if card.showing:
            card.body.pack_forget()
            card.showing = False
            # destroy old widgets so we can rebuild fresh next time
            for w in card.body.winfo_children():
                w.destroy()
        else:
            members = api.get_class_members(class_id)

            if not members:
                ctk.CTkLabel(card.body, text="No students enrolled yet.",
                             font=ctk.CTkFont(size=13, weight="bold"),
                             text_color=TEXT_LIGHT).pack(anchor="w", padx=20, pady=(10,5))
            else:
                # show studnet count at top
                ctk.CTkLabel(
                    card.body, text=f"Enrolled: {len(members)} students",
                    font=ctk.CTkFont(size=13, weight="bold"),
                    text_color=TEXT_LIGHT
                ).pack(anchor="w", padx=20, pady=(10,5))

                # list each student with thier progress
                for m in members:
                    row = ctk.CTkFrame(card.body, fg_color="transparent")
                    row.pack(fill="x", padx=20, pady=3)

                    ctk.CTkLabel(
                        row, text=m["username"],
                        font=ctk.CTkFont(size=14, weight="bold"),
                        text_color=TEXT_COLOR
                    ).pack(side="left")

                    ctk.CTkLabel(
                        row, text=f"{m['points']} pts",
                        font=ctk.CTkFont(size=14, weight="bold"),
                        text_color=GREEN
                    ).pack(side="right")

            card.body.pack(fill="x", padx=15, pady=(0,10))
            card.showing = True

    # -- settings tab -------------------------------------------

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
        desc_box.insert("1.0", self.user.get("description", ""))
        desc_box.pack(fill="x", padx=20, pady=(0,15))

        self.save_msg = ctk.CTkLabel(card, text="", font=ctk.CTkFont(size=12),
                                     text_color=GREEN)
        self.save_msg.pack(anchor="w", padx=20)

        def do_save():
            new_desc = desc_box.get("1.0", "end").strip()
            res = api.update_user(self.user_id, description=new_desc)
            if res:
                self.user["description"] = new_desc
                self.save_msg.configure(text="Saved!", text_color=GREEN)
            else:
                self.save_msg.configure(text="Save failed.", text_color=RED)

        ctk.CTkButton(
            card, text="💾  Save",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=PURPLE, hover_color=PURPLE_DARK,
            corner_radius=20, height=42,
            command=do_save
        ).pack(anchor="e", padx=20, pady=(5,20))


def main():
    # example data; in a real application this would come from the server or
    # login flow
    temp_user = {
        "id": 1,
        "username": "teacher1",
        "role": "teacher",
        "points": 0,
        "streak": 0,
        "description": "",
    }

    app = TeacherPage(temp_user)
    app.mainloop()


if __name__ == "__main__":
    main()
