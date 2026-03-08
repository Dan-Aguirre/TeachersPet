import tkinter as tk
from tkinter import ttk

# from frontend.src.pages.studentpage import StudentPage


class StudentPage(tk.Tk):
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
        self.title("Sample student Dashboard")
        self.geometry("800x600")
        self.student_info = student_info
        self.classes_data = classes_data
        self._make_sidebar()

        # frame that will hold whatever view is currently active
        self.main_frame = tk.Frame(self, bg="#ffffff")
        self.main_frame.pack(side="right", expand=True, fill="both")

        # start on the profile page
        self.show_profile()

    def _make_sidebar(self) -> None:
        sidebar = tk.Frame(self, width=200, bg="#cccccc")
        sidebar.pack(side="left", fill="y")
        btn_kwargs = {"fill": "x", "padx": 10, "pady": 5}

        tk.Button(sidebar, text="Profile", command=self.show_profile).pack(
            **btn_kwargs
        )
        tk.Button(sidebar, text="Classes", command=self.show_classes).pack(
            **btn_kwargs
        )
        tk.Button(sidebar, text="Rankings", command=self.show_rankings).pack(
            **btn_kwargs
        )
        tk.Button(sidebar, text="Settings", command=self.show_settings).pack(
            **btn_kwargs
        )

    def _clear_main(self) -> None:
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_profile(self) -> None:
        self._clear_main()
        tk.Label(self.main_frame, text="Profile", font=("Arial", 16)).pack(pady=10)
        tk.Label(
            self.main_frame,
            text=f"Username: {self.student_info.get('username', '')}",
        ).pack(anchor="w", padx=20)
        tk.Label(
            self.main_frame,
            text=f"Password: {'*' * len(self.student_info.get('password', ''))}",
        ).pack(anchor="w", padx=20)
        tk.Label(self.main_frame, text="Description:").pack(anchor="w", padx=20, pady=(10, 0))

        desc = tk.Text(self.main_frame, height=5, width=50)
        desc.insert("1.0", self.student_info.get("description", ""))
        desc.config(state="disabled")
        desc.pack(anchor="w", padx=20)

    def show_classes(self) -> None:
        self._clear_main()
        tk.Label(self.main_frame, text="Classes", font=("Arial", 16)).pack(pady=10)

        # for each class we create a container with a header and a body that can be shown/hidden (the "dropdown").
        for class_name, students in self.classes_data.items():
            container = tk.Frame(self.main_frame, bd=1, relief="solid")
            container.pack(fill="x", padx=20, pady=5)

            header = tk.Frame(container)
            header.pack(fill="x")
            tk.Label(header, text=class_name, font=("Arial", 14)).pack(side="left")
            toggle_btn = tk.Button(
                header,
                text="Show",
                command=lambda n=class_name, c=container: self._toggle_class(n, c),
            )
            toggle_btn.pack(side="right")

            body = tk.Frame(container)
            body.pack(fill="x")
            body.pack_forget()  # start hidden
            container.body = body
            container.showing = False

    def _toggle_class(self, class_name: str, container: tk.Frame) -> None:
        """Show or hide the current student's progress for a given class."""
        if container.showing:
            container.body.pack_forget()
            container.showing = False
            for w in container.body.winfo_children():
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

            tk.Label(
                container.body,
                text=msg,
            ).pack(anchor="w", padx=20, pady=2)

            container.body.pack(fill="x")
            container.showing = True

    def show_rankings(self) -> None:
        self._clear_main()
        tk.Label(self.main_frame, text="Rankings", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.main_frame, text="(rankings placeholder)").pack(pady=20)

    def show_settings(self) -> None:
        self._clear_main()
        tk.Label(self.main_frame, text="Settings", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.main_frame, text="(settings placeholder)").pack(pady=20)


def main() -> None:
    # example data; in a real application this would come from the server or
    # login flow
    student_info = {
        "username": "student1",
        "password": "password123",
        "description": "Student in SHS! I am taking pre-calculus and advanced geometry.",
    }

    # in a real application the structure could be different; here we still
    # provide a list of (name, progress) tuples for compatibility with the
    # original design, but only the current student ("student1") will be
    # looked up when the toggle button is pressed.
    classes_data = {
        "Pre-Calculus": [("student1", "45")],
        "Advanced Geometry": [("student1", "78")],
    }

    app = StudentPage(student_info, classes_data)
    app.mainloop()


if __name__ == "__main__":
    main()
