import customtkinter as ctk
from studentpage import StudentPage
from teacherpage import TeacherPage
import api

# apperance
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# colors (same pallete as student/teacher pages)
PURPLE = "#7c5cfc"
PURPLE_DARK = "#5a3fd6"
PURPLE_LIGHT = "#ebe5ff"
BG_COLOR = "#f3f1fa"
CARD_BG = "#ffffff"
TEXT_COLOR = "#2d2b3a"
TEXT_LIGHT = "#7e7b91"
ERROR_RED = "#EA2B2B"
GREEN = "#58CC02"

SPECIAL_CHARS = set(['<', '>', '"', "'", ';', '\\', '{', '}', ':', '|', '`'])

#Checks if the input has any of the special characters defined above
def invalid_check(text: str) -> bool:
    return any(ch in SPECIAL_CHARS for ch in text)


class LoginPage(ctk.CTk):
    """Login and registration screen for Teacher's Pet.

    Shows a centered card with username/password fields.
    Can toggle between login and register views.
    On success, opens the appropriate dashboard (student or teacher).
    """

    def __init__(self):
        super().__init__()
        self.title("Teacher's Pet")
        self.geometry("560x760")
        self.configure(fg_color=BG_COLOR)
        self.resizable(False, False)

        # center everthing in the window
        self.container = ctk.CTkFrame(self, fg_color=BG_COLOR)
        self.container.place(relx=0.5, rely=0.04, anchor="n")

        self._build_login_view()

    def _clear(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def _build_login_view(self):
        self._clear()

        # icon area
        icon_frame = ctk.CTkFrame(self.container, fg_color=PURPLE,
                                  corner_radius=20, width=80, height=80)
        icon_frame.pack(pady=(0, 10))
        icon_frame.pack_propagate(False)
        ctk.CTkLabel(icon_frame, text="📖", font=ctk.CTkFont(size=36),
                     text_color="white").place(relx=0.5, rely=0.5, anchor="center")

        # title
        ctk.CTkLabel(self.container, text="Teacher's Pet",
                     font=ctk.CTkFont(size=28, weight="bold"),
                     text_color=TEXT_COLOR).pack(pady=(5, 2))
        ctk.CTkLabel(self.container, text="Sign in to start your practice",
                     font=ctk.CTkFont(size=14),
                     text_color=TEXT_LIGHT).pack(pady=(0, 20))

        # card
        card = ctk.CTkFrame(self.container, fg_color=CARD_BG,
                            corner_radius=24, width=360)
        card.pack(padx=20)

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(padx=30, pady=30, fill="x")

        # username
        ctk.CTkLabel(inner, text="USERNAME",
                     font=ctk.CTkFont(size=12, weight="bold"),
                     text_color=TEXT_LIGHT).pack(anchor="w", pady=(0, 4))
        self.login_user = ctk.CTkEntry(inner, placeholder_text="Enter your username",
                                       corner_radius=14, height=44,
                                       fg_color=BG_COLOR, border_color=PURPLE_LIGHT,
                                       border_width=2, font=ctk.CTkFont(size=14))
        self.login_user.pack(fill="x", pady=(0, 14))

        # password
        ctk.CTkLabel(inner, text="PASSWORD",
                     font=ctk.CTkFont(size=12, weight="bold"),
                     text_color=TEXT_LIGHT).pack(anchor="w", pady=(0, 4))
        self.login_pass = ctk.CTkEntry(inner, placeholder_text="Enter your password",
                                       show="*", corner_radius=14, height=44,
                                       fg_color=BG_COLOR, border_color=PURPLE_LIGHT,
                                       border_width=2, font=ctk.CTkFont(size=14))
        self.login_pass.pack(fill="x", pady=(0, 6))

        # error label (hidden untill needed)
        self.login_error = ctk.CTkLabel(inner, text="",
                                        font=ctk.CTkFont(size=12),
                                        text_color=ERROR_RED)
        self.login_error.pack(anchor="w", pady=(0, 8))

        # login button
        ctk.CTkButton(inner, text="Log In",
                      font=ctk.CTkFont(size=15, weight="bold"),
                      fg_color=PURPLE, hover_color=PURPLE_DARK,
                      corner_radius=18, height=46,
                      command=self._handle_login).pack(fill="x", pady=(4, 0))

        # divider line
        div_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        div_frame.pack(fill="x", padx=40, pady=18)
        ctk.CTkFrame(div_frame, fg_color=PURPLE_LIGHT, height=2).pack(fill="x")

        # switch to register
        ctk.CTkButton(self.container, text="Create an Account",
                      font=ctk.CTkFont(size=14, weight="bold"),
                      fg_color="transparent", text_color=PURPLE,
                      hover_color=PURPLE_LIGHT, corner_radius=18,
                      height=42, border_width=2, border_color=PURPLE_LIGHT,
                      command=self._build_register_view).pack(padx=40, fill="x")

    def _handle_login(self):
        username = self.login_user.get().strip()
        password = self.login_pass.get().strip()

        if not username or not password:
            self.login_error.configure(text="Please fill in all fields.")
            return
        
        # check if user input a special character before sending it to backend
        if invalid_check(username) or invalid_check(password):
            self.login_error.configure(text="Invalid characters in username or passoword.")
            return
        

        # call real backend instead of mock dict
        usr_data = api.login(username, password)
        if not usr_data:
            self.login_error.configure(text="Wrong username or password.")
            return

        self._open_dashboard(usr_data)

    def _build_register_view(self):
        self._clear()

        # icon area
        icon_frame = ctk.CTkFrame(self.container, fg_color=GREEN,
                                  corner_radius=20, width=80, height=80)
        icon_frame.pack(pady=(0, 10))
        icon_frame.pack_propagate(False)
        ctk.CTkLabel(icon_frame, text="✏️", font=ctk.CTkFont(size=36),
                     text_color="white").place(relx=0.5, rely=0.5, anchor="center")

        # title
        ctk.CTkLabel(self.container, text="Create Account",
                     font=ctk.CTkFont(size=28, weight="bold"),
                     text_color=TEXT_COLOR).pack(pady=(5, 2))
        ctk.CTkLabel(self.container, text="Join Teacher's Pet today",
                     font=ctk.CTkFont(size=14),
                     text_color=TEXT_LIGHT).pack(pady=(0, 20))

        # card
        card = ctk.CTkFrame(self.container, fg_color=CARD_BG,
                            corner_radius=24, width=360)
        card.pack(padx=20)

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(padx=30, pady=30, fill="x")

        # username
        ctk.CTkLabel(inner, text="USERNAME",
                     font=ctk.CTkFont(size=12, weight="bold"),
                     text_color=TEXT_LIGHT).pack(anchor="w", pady=(0, 4))
        self.reg_user = ctk.CTkEntry(inner, placeholder_text="Choose a username",
                                     corner_radius=14, height=44,
                                     fg_color=BG_COLOR, border_color=PURPLE_LIGHT,
                                     border_width=2, font=ctk.CTkFont(size=14))
        self.reg_user.pack(fill="x", pady=(0, 14))

        # password
        ctk.CTkLabel(inner, text="PASSWORD",
                     font=ctk.CTkFont(size=12, weight="bold"),
                     text_color=TEXT_LIGHT).pack(anchor="w", pady=(0, 4))
        self.reg_pass = ctk.CTkEntry(inner, placeholder_text="Choose a password",
                                     show="*", corner_radius=14, height=44,
                                     fg_color=BG_COLOR, border_color=PURPLE_LIGHT,
                                     border_width=2, font=ctk.CTkFont(size=14))
        self.reg_pass.pack(fill="x", pady=(0, 14))

        # role selecter
        ctk.CTkLabel(inner, text="I AM A...",
                     font=ctk.CTkFont(size=12, weight="bold"),
                     text_color=TEXT_LIGHT).pack(anchor="w", pady=(0, 6))

        role_frame = ctk.CTkFrame(inner, fg_color="transparent")
        role_frame.pack(fill="x", pady=(0, 6))
        role_frame.columnconfigure((0, 1), weight=1)

        self.role_var = ctk.StringVar(value="student")

        self.student_role_btn = ctk.CTkButton(
            role_frame, text="🎓 Student",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=PURPLE, text_color="white",
            hover_color=PURPLE_DARK, corner_radius=14, height=40,
            command=lambda: self._select_role("student"))
        self.student_role_btn.grid(row=0, column=0, padx=(0, 5), sticky="ew")

        self.teacher_role_btn = ctk.CTkButton(
            role_frame, text="👩‍🏫 Teacher",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="transparent", text_color=TEXT_LIGHT,
            hover_color=PURPLE_LIGHT, corner_radius=14, height=40,
            border_width=2, border_color=PURPLE_LIGHT,
            command=lambda: self._select_role("teacher"))
        self.teacher_role_btn.grid(row=0, column=1, padx=(5, 0), sticky="ew")

        # error label
        self.reg_error = ctk.CTkLabel(inner, text="",
                                      font=ctk.CTkFont(size=12),
                                      text_color=ERROR_RED)
        self.reg_error.pack(anchor="w", pady=(4, 8))

        # register btn
        ctk.CTkButton(inner, text="Create Account",
                      font=ctk.CTkFont(size=15, weight="bold"),
                      fg_color=GREEN, hover_color="#46A302",
                      corner_radius=18, height=46,
                      command=self._handle_register).pack(fill="x", pady=(4, 0))

        # divider line
        div_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        div_frame.pack(fill="x", padx=40, pady=18)
        ctk.CTkFrame(div_frame, fg_color=PURPLE_LIGHT, height=2).pack(fill="x")

        # back to login
        ctk.CTkButton(self.container, text="Already have an account? Log In",
                      font=ctk.CTkFont(size=14, weight="bold"),
                      fg_color="transparent", text_color=PURPLE,
                      hover_color=PURPLE_LIGHT, corner_radius=18,
                      height=42, border_width=2, border_color=PURPLE_LIGHT,
                      command=self._build_login_view).pack(padx=40, fill="x")

    def _select_role(self, role):
        self.role_var.set(role)
        if role == "student":
            self.student_role_btn.configure(fg_color=PURPLE, text_color="white",
                                           border_width=0)
            self.teacher_role_btn.configure(fg_color="transparent", text_color=TEXT_LIGHT,
                                           border_width=2, border_color=PURPLE_LIGHT)
        else:
            self.teacher_role_btn.configure(fg_color=PURPLE, text_color="white",
                                           border_width=0)
            self.student_role_btn.configure(fg_color="transparent", text_color=TEXT_LIGHT,
                                           border_width=2, border_color=PURPLE_LIGHT)

    def _handle_register(self):
        username = self.reg_user.get().strip()
        password = self.reg_pass.get().strip()
        role = self.role_var.get()

        if invalid_check(username) or invalid_check(password):
            self.reg_error.configure(text="Invalid characters in username or password.")
            return

        if not username or not password:
            self.reg_error.configure(text="Please fill in all fields.")
            return

        # register w/ backend -- returns new user dict on success
        usr_data = api.register(username, password, role)
        if not usr_data:
            self.reg_error.configure(text="Username already taken.")
            return

        self._open_dashboard(usr_data)

    def _open_dashboard(self, user):
        """close login and open the right dashboard based on role"""
        self.withdraw()

        # route to right page based on role
        if user["role"] == "teacher":
            dashboard = TeacherPage(user)
        else:
            dashboard = StudentPage(user)

        dashboard.protocol("WM_DELETE_WINDOW",
                           lambda: self._on_dashboard_close(dashboard))
        dashboard.mainloop()

    def _on_dashboard_close(self, dashboard):
        """When dashboard closes, quit the whole app."""
        dashboard.destroy()
        self.destroy()


def main():
    app = LoginPage()
    app.mainloop()


if __name__ == "__main__":
    main()
