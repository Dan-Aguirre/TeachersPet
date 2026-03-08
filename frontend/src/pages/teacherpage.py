import tkinter as tk
from tkinter import ttk


class TeacherPage(tk.Tk):
    """Simple Tkinter dashboard for a teacher with a sidebar and dynamic content.

    The sidebar has three buttons: Profile, Classes and Settings.  Clicking one
    of the buttons clears the main content area and rebuilds it with the
    appropriate widgets.  ``teacher_info`` and ``classes_data`` are injected so
    that the class can be used in a real application or for testing.
    """

    def __init__(self, teacher_info: dict, classes_data: dict):
        super().__init__()
        self.title("Teacher Dashboard")
        self.geometry("800x600")
        self.teacher_info = teacher_info
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
            text=f"Username: {self.teacher_info.get('username', '')}",
        ).pack(anchor="w", padx=20)
        tk.Label(
            self.main_frame,
            text=f"Password: {'*' * len(self.teacher_info.get('password', ''))}",
        ).pack(anchor="w", padx=20)
        tk.Label(self.main_frame, text="Description:").pack(anchor="w", padx=20, pady=(10, 0))

        desc = tk.Text(self.main_frame, height=5, width=50)
        desc.insert("1.0", self.teacher_info.get("description", ""))
        desc.config(state="disabled")
        desc.pack(anchor="w", padx=20)

    def show_classes(self) -> None:
        self._clear_main()
        tk.Label(self.main_frame, text="Classes", font=("Arial", 16)).pack(pady=10)

        # for each class we create a container with a header and a body that can
        # be shown/hidden (the "dropdown").
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
        """Expand or collapse the student details for a class."""
        if container.showing:
            container.body.pack_forget()
            container.showing = False
            # destroy old widgets so we can rebuild fresh next time
            for w in container.body.winfo_children():
                w.destroy()
        else:
            students = self.classes_data.get(class_name, [])
            tk.Label(
                container.body,
                text=f"Number of students: {len(students)}",
            ).pack(anchor="w", padx=20, pady=2)
            for name, progress in students:
                tk.Label(
                    container.body, text=f"{name}: {progress}"
                ).pack(anchor="w", padx=40)
            container.body.pack(fill="x")
            container.showing = True

    def show_settings(self) -> None:
        self._clear_main()
        tk.Label(self.main_frame, text="Settings", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.main_frame, text="(settings placeholder)").pack(pady=20)


def main() -> None:
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
