import customtkinter as ctk
import threading
import api

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
ORANGE = "#FF9600"
RED = "#EA2B2B"
GREEN = "#58CC02"


class StudentPage(ctk.CTk):
    """Dashboard for a student -- sidebar tabs and main content area.

    tabs: profile, classes, rankings, play (quiz), settings
    all data now comes from the flask backend via api.py -- no more hardcoded stuff
    """

    def __init__(self, user: dict, on_logout=None):
        super().__init__()
        self.title("Teacher's Pet - Student Dashboard")
        self.geometry("900x650")
        self.configure(fg_color=BG_COLOR)

        self.user = user
        self.user_id = user["id"]
        self.on_logout = on_logout  

        # current question being displayed in quiz tab
        self.current_question = None

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

        # play button -- new quiz feature
        self.play_btn = ctk.CTkButton(
            sidebar, text="  🎮  Play",
            command=self.show_quiz, **btn_style
        )
        self.play_btn.pack(fill="x", padx=10, pady=3)

        self.streaks_btn = ctk.CTkButton(
            sidebar, text="  🏅  Streaks",
            command = self.show_streaks, **btn_style
        )
        self.streaks_btn.pack(fill="x", padx=10, pady=3)

        self.settings_btn = ctk.CTkButton(
            sidebar, text="  ⚙️  Settings",
            command=self.show_settings, **btn_style
        )
        self.settings_btn.pack(fill="x", padx=10, pady=3)

    def _set_active_btn(self, active_btn):
        """highlight the active sidebar button and reset the othres"""
        all_btns = [self.profile_btn, self.classes_btn, self.rank_btn,
                    self.play_btn, self.streaks_btn, self.settings_btn]
        for btn in all_btns:
            btn.configure(fg_color="transparent", text_color=TEXT_LIGHT)
        active_btn.configure(fg_color=PURPLE_LIGHT, text_color=PURPLE)

    def _clear_main(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def _run_async(self, fn, callback):
        """run a blocking api call in background thread so ui doesnt freeze"""
        def worker():
            result = fn()
            self.after(0, lambda: callback(result))
        threading.Thread(target=worker, daemon=True).start()

    # -- profile tab --------------------------------------------

    def show_profile(self):
        self._clear_main()
        self._set_active_btn(self.profile_btn)

        # header with username
        header = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        header.pack(fill="x", pady=(5,15))

        ctk.CTkLabel(
            header, text=self.user.get("username", ""),
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=TEXT_COLOR
        ).pack(anchor="w")
        ctk.CTkLabel(
            header, text="Student Account",
            font=ctk.CTkFont(size=14), text_color=TEXT_LIGHT
        ).pack(anchor="w")

        # stats row -- start w/ loading placeholders
        stats_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        stats_frame.pack(fill="x", pady=10)
        stats_frame.columnconfigure((0,1,2), weight=1)

        # points card
        points_card = ctk.CTkFrame(stats_frame, fg_color=CARD_BG, corner_radius=20)
        points_card.grid(row=0, column=0, padx=5, sticky="nsew")
        ctk.CTkLabel(points_card, text="🏆", font=ctk.CTkFont(size=28)).pack(pady=(15,5))
        ctk.CTkLabel(points_card, text="Total Points", text_color=TEXT_LIGHT,
                     font=ctk.CTkFont(size=12, weight="bold")).pack()
        self.points_lbl = ctk.CTkLabel(points_card, text="...", text_color=ORANGE,
                     font=ctk.CTkFont(size=24, weight="bold"))
        self.points_lbl.pack(pady=(0,15))

        # games card
        games_card = ctk.CTkFrame(stats_frame, fg_color=CARD_BG, corner_radius=20)
        games_card.grid(row=0, column=1, padx=5, sticky="nsew")
        ctk.CTkLabel(games_card, text="🎯", font=ctk.CTkFont(size=28)).pack(pady=(15,5))
        ctk.CTkLabel(games_card, text="Games Played", text_color=TEXT_LIGHT,
                      font=ctk.CTkFont(size=12, weight="bold")).pack()
        self.games_lbl = ctk.CTkLabel(games_card, text="...", text_color=PURPLE,
                     font=ctk.CTkFont(size=24, weight="bold"))
        self.games_lbl.pack(pady=(0,15))

        # streak card
        streak_card = ctk.CTkFrame(stats_frame, fg_color=CARD_BG, corner_radius=20)
        streak_card.grid(row=0, column=2, padx=5, sticky="nsew")
        ctk.CTkLabel(streak_card, text="🔥", font=ctk.CTkFont(size=28)).pack(pady=(15,5))
        ctk.CTkLabel(streak_card, text="Streak", text_color=TEXT_LIGHT,
                     font=ctk.CTkFont(size=12, weight="bold")).pack()
        self.streak_lbl = ctk.CTkLabel(streak_card, text="...", text_color=RED,
                     font=ctk.CTkFont(size=24, weight="bold"))
        self.streak_lbl.pack(pady=(0,15))

        # about me seciton
        about_card = ctk.CTkFrame(self.main_frame, fg_color=CARD_BG, corner_radius=20)
        about_card.pack(fill="x", pady=(15, 10))

        ctk.CTkLabel(about_card, text="About Me",
                     font=ctk.CTkFont(size=18, weight="bold"),
                     text_color=TEXT_COLOR).pack(anchor="w", padx=20, pady=(15,5))

        self.about_lbl = ctk.CTkLabel(about_card, text="Loading...",
                     font=ctk.CTkFont(size=14), text_color=TEXT_LIGHT,
                     wraplength=500, justify="left")
        self.about_lbl.pack(anchor="w", padx=20, pady=(0,15))

        # logout button
        logout_btn = ctk.CTkButton(
            about_card, text="🚪  Logout",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=RED, hover_color="#c91f1f",
            corner_radius=12, height=36,
            command=self._handle_logout
        )
        logout_btn.pack(anchor="e", padx=20, pady=(10, 15))

        # fetch real stats in background
        self._run_async(
            lambda: api.get_stats(self.user_id),
            self._on_stats_loaded
        )

    def _on_stats_loaded(self, stats_data):
        """callback -- update stat labels once api call finishes"""
        if not stats_data:
            self.points_lbl.configure(text="--")
            self.games_lbl.configure(text="--")
            self.streak_lbl.configure(text="--")
            self.about_lbl.configure(text="Could not load stats")
            return
        self.points_lbl.configure(text=str(stats_data.get("points", 0)))
        self.games_lbl.configure(text=str(stats_data.get("games_played", 0)))
        self.streak_lbl.configure(text=f"{stats_data.get('streak', 0)} Days")
        self.about_lbl.configure(text=stats_data.get("description", ""))

    def _handle_logout(self):
        """handle logout - save session data and return to login"""
        api.logout(self.user_id)
        # Defer logout to allow button animation to complete
        self.after(100, lambda: self.on_logout() if self.on_logout else None)

    # -- classes tab --------------------------------------------

    def show_classes(self):
        self._clear_main()
        self._set_active_btn(self.classes_btn)

        ctk.CTkLabel(
            self.main_frame, text="My Classes",
            font=ctk.CTkFont(size=26, weight="bold"), text_color=TEXT_COLOR
        ).pack(anchor="w", pady=(5, 15))

        # join class card at top
        join_card = ctk.CTkFrame(self.main_frame, fg_color=CARD_BG, corner_radius=20)
        join_card.pack(fill="x", pady=(0,10))

        join_inner = ctk.CTkFrame(join_card, fg_color="transparent")
        join_inner.pack(fill="x", padx=20, pady=15)

        ctk.CTkLabel(join_inner, text="Join a Class",
                     font=ctk.CTkFont(size=15, weight="bold"),
                     text_color=TEXT_COLOR).pack(anchor="w", pady=(0,8))

        join_row = ctk.CTkFrame(join_inner, fg_color="transparent")
        join_row.pack(fill="x")

        self.join_entry = ctk.CTkEntry(join_row, placeholder_text="Enter class code",
                                       corner_radius=12, height=38,
                                       fg_color=BG_COLOR, border_color=PURPLE_LIGHT,
                                       border_width=2, font=ctk.CTkFont(size=13))
        self.join_entry.pack(side="left", expand=True, fill="x", padx=(0,8))

        ctk.CTkButton(join_row, text="Join", width=80,
                      fg_color=PURPLE, hover_color=PURPLE_DARK,
                      corner_radius=12, height=38,
                      font=ctk.CTkFont(size=13, weight="bold"),
                      command=self._handle_join_class).pack(side="left")

        self.join_msg = ctk.CTkLabel(join_inner, text="", font=ctk.CTkFont(size=12),
                                     text_color=TEXT_LIGHT)
        self.join_msg.pack(anchor="w", pady=(6,0))

        # container for the class list -- populated by async call
        self.classes_container = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.classes_container.pack(fill="x")

        ctk.CTkLabel(self.classes_container, text="Loading...",
                     font=ctk.CTkFont(size=14), text_color=TEXT_LIGHT).pack(pady=20)

        self._run_async(
            lambda: api.get_classes(self.user_id),
            self._on_classes_loaded
        )

    def _handle_join_class(self):
        code = self.join_entry.get().strip().upper()
        if not code:
            return
        res = api.join_class(code, self.user_id)
        if res:
            self.join_msg.configure(text="Joined! Refreshing...", text_color=GREEN)
            # refresh the class list
            self._run_async(
                lambda: api.get_classes(self.user_id),
                self._on_classes_loaded
            )
        else:
            self.join_msg.configure(text="Code not found or already enrolled.", text_color=RED)

    def _on_classes_loaded(self, data):
        """rebuild class cards once we get the data back"""
        # check if the widget is still there -- if user clicked away it wont be
        # and we'll get a crash so we just stop here if its gone
        if not self.classes_container.winfo_exists():
          return

        for w in self.classes_container.winfo_children():
            w.destroy()

        if not data:
            ctk.CTkLabel(self.classes_container, text="No classes found.",
                         font=ctk.CTkFont(size=14), text_color=TEXT_LIGHT).pack(pady=20)
            return

        # students see enrolled list
        class_list = data.get("enrolled", [])
        if not class_list:
            ctk.CTkLabel(self.classes_container, text="You haven't joined any classes yet.",
                         font=ctk.CTkFont(size=14), text_color=TEXT_LIGHT).pack(pady=20)
            return

        for cls in class_list:
            card = ctk.CTkFrame(self.classes_container, fg_color=CARD_BG, corner_radius=20)
            card.pack(fill="x", pady=6)

            # class header row
            header_frame = ctk.CTkFrame(card, fg_color="transparent")
            header_frame.pack(fill="x", padx=20, pady=15)

            ctk.CTkLabel(
                header_frame, text=cls["name"],
                font=ctk.CTkFont(size=18, weight="bold"), text_color=TEXT_COLOR
            ).pack(side="left")

            # show join code next to name
            ctk.CTkLabel(
                header_frame, text=f"Code: {cls['code']}",
                font=ctk.CTkFont(size=12), text_color=TEXT_LIGHT
            ).pack(side="left", padx=(12,0))

            # toggle button for expanding
            toggle_btn = ctk.CTkButton(
                header_frame, text="Show ▼", width=80,
                fg_color=PURPLE_LIGHT, text_color=PURPLE,
                hover_color="#ddd8f0", corner_radius=12,
                font=ctk.CTkFont(size=12, weight="bold"),
                command=lambda c=cls, card_ref=card: self._toggle_class(c["id"], card_ref)
            )
            toggle_btn.pack(side="right")

            # hidden body frame
            body = ctk.CTkFrame(card, fg_color=BG_COLOR, corner_radius=12)
            card.body = body
            card.showing = False

    def _toggle_class(self, class_id, card):
        """show or hide member list for a class"""
        if card.showing:
            card.body.pack_forget()
            card.showing = False
            for w in card.body.winfo_children():
                w.destroy()
        else:
            members = api.get_class_members(class_id)
            if not members:
                ctk.CTkLabel(card.body, text="No members found.",
                             font=ctk.CTkFont(size=13), text_color=TEXT_LIGHT
                             ).pack(anchor="w", padx=20, pady=10)
            else:
                for m in members:
                    row = ctk.CTkFrame(card.body, fg_color="transparent")
                    row.pack(fill="x", padx=20, pady=3)
                    ctk.CTkLabel(row, text=m["username"],
                                 font=ctk.CTkFont(size=14, weight="bold"),
                                 text_color=TEXT_COLOR).pack(side="left")
                    ctk.CTkLabel(row, text=f"{m['points']} pts",
                                 font=ctk.CTkFont(size=13), text_color=ORANGE
                                 ).pack(side="right")

            card.body.pack(fill="x", padx=15, pady=(0,10))
            card.showing = True

    # -- rankings tab -------------------------------------------

    def show_rankings(self):
        self._clear_main()
        self._set_active_btn(self.rank_btn)

        ctk.CTkLabel(
            self.main_frame, text="Global Rankings",
            font=ctk.CTkFont(size=26, weight="bold"), text_color=TEXT_COLOR
        ).pack(anchor="w", pady=(5,15))

        # loading placeholder
        self.rank_container = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.rank_container.pack(fill="x")
        ctk.CTkLabel(self.rank_container, text="Loading...",
                     font=ctk.CTkFont(size=14), text_color=TEXT_LIGHT).pack(pady=20)

        self._run_async(api.get_rankings, self._on_rankings_loaded)

    def _on_rankings_loaded(self, ranking_data):
        for w in self.rank_container.winfo_children():
            w.destroy()

        if not ranking_data:
            ctk.CTkLabel(self.rank_container, text="Could not load rankings.",
                         font=ctk.CTkFont(size=14), text_color=TEXT_LIGHT).pack(pady=20)
            return

        medals = ["🥇", "🥈", "🥉"]
        for i, entry in enumerate(ranking_data):
            row = ctk.CTkFrame(self.rank_container, fg_color=CARD_BG, corner_radius=16)
            row.pack(fill="x", pady=4)

            # highlihgt if this is the current user
            is_me = entry["id"] == self.user_id
            if is_me:
                row.configure(border_width=2, border_color=PURPLE)

            inner = ctk.CTkFrame(row, fg_color="transparent")
            inner.pack(fill="x", padx=15, pady=12)

            medal = medals[i] if i < 3 else f"  #{i+1}"
            ctk.CTkLabel(inner, text=medal, font=ctk.CTkFont(size=20),
                        width=50).pack(side="left")

            name_txt = entry["username"] + (" (You)" if is_me else "")
            ctk.CTkLabel(inner, text=name_txt,
                         font=ctk.CTkFont(size=16, weight="bold"),
                         text_color=PURPLE if is_me else TEXT_COLOR).pack(side="left", padx=10)
            ctk.CTkLabel(inner, text=f"{entry['points']} pts",
                        font=ctk.CTkFont(size=14, weight="bold"),
                        text_color=ORANGE).pack(side="right")

    # -- quiz tab -----------------------------------------------

    def show_quiz(self):
        self._clear_main()
        self._set_active_btn(self.play_btn)

        ctk.CTkLabel(
            self.main_frame, text="Play",
            font=ctk.CTkFont(size=26, weight="bold"), text_color=TEXT_COLOR
        ).pack(anchor="w", pady=(5,15))

        quiz_card = ctk.CTkFrame(self.main_frame, fg_color=CARD_BG, corner_radius=20)
        quiz_card.pack(fill="x", pady=5)

        inner = ctk.CTkFrame(quiz_card, fg_color="transparent")
        inner.pack(fill="x", padx=25, pady=25)

        # difficulty selector
        ctk.CTkLabel(inner, text="Difficulty",
                     font=ctk.CTkFont(size=14, weight="bold"),
                     text_color=TEXT_COLOR).pack(anchor="w", pady=(0,8))

        diff_frame = ctk.CTkFrame(inner, fg_color="transparent")
        diff_frame.pack(anchor="w", pady=(0,15))

        self.diff_var = ctk.StringVar(value="easy")

        # tried using a segmented button but it was buggy so just using 3 btns
        # self.diff_seg = ctk.CTkSegmentedButton(inner, values=["easy","medium","hard"])

        self.diff_btns = {}
        diff_colors = {"easy": GREEN, "medium": ORANGE, "hard": RED}
        for d in ["easy", "medium", "hard"]:
            btn = ctk.CTkButton(diff_frame, text=d.capitalize(), width=90,
                                corner_radius=12, height=34,
                                font=ctk.CTkFont(size=13, weight="bold"),
                                fg_color=diff_colors[d] if d=="easy" else "transparent",
                                text_color="white" if d=="easy" else TEXT_LIGHT,
                                hover_color=PURPLE_LIGHT,
                                border_width=2, border_color=PURPLE_LIGHT,
                                command=lambda val=d: self._select_difficulty(val))
            btn.pack(side="left", padx=(0,6))
            self.diff_btns[d] = btn

        # new question button
        ctk.CTkButton(inner, text="New Question",
                      font=ctk.CTkFont(size=14, weight="bold"),
                      fg_color=PURPLE, hover_color=PURPLE_DARK,
                      corner_radius=16, height=40,
                      command=self._fetch_question).pack(anchor="w", pady=(0,15))

        # question display area
        self.question_lbl = ctk.CTkLabel(inner, text="Press 'New Question' to start!",
                                         font=ctk.CTkFont(size=16),
                                         text_color=TEXT_COLOR,
                                         wraplength=500, justify="left")
        self.question_lbl.pack(anchor="w", pady=(0,15))

        # answer input
        ctk.CTkLabel(inner, text="Your Answer",
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color=TEXT_LIGHT).pack(anchor="w", pady=(0,5))
        self.answer_entry = ctk.CTkEntry(inner, placeholder_text="Type your answer here",
                                         corner_radius=12, height=40,
                                         fg_color=BG_COLOR, border_color=PURPLE_LIGHT,
                                         border_width=2, font=ctk.CTkFont(size=14))
        self.answer_entry.pack(fill="x", pady=(0,10))

        ctk.CTkButton(inner, text="Submit Answer",
                      font=ctk.CTkFont(size=14, weight="bold"),
                      fg_color=PURPLE, hover_color=PURPLE_DARK,
                      corner_radius=16, height=40,
                      command=self._submit_answer).pack(anchor="w", pady=(0,12))

        # result feedback label
        self.result_lbl = ctk.CTkLabel(inner, text="",
                                       font=ctk.CTkFont(size=15, weight="bold"),
                                       text_color=GREEN)
        self.result_lbl.pack(anchor="w")

        # live points display
        self.live_pts_lbl = ctk.CTkLabel(inner, text=f"Your points: {self.user.get('points', 0)}",
                                         font=ctk.CTkFont(size=13),
                                         text_color=TEXT_LIGHT)
        self.live_pts_lbl.pack(anchor="w", pady=(6,0))

    def _select_difficulty(self, val):
        """highlight selected difficulty btn"""
        self.diff_var.set(val)
        diff_colors = {"easy": GREEN, "medium": ORANGE, "hard": RED}
        for d, btn in self.diff_btns.items():
            if d == val:
                btn.configure(fg_color=diff_colors[d], text_color="white", border_width=0)
            else:
                btn.configure(fg_color="transparent", text_color=TEXT_LIGHT,
                              border_width=2, border_color=PURPLE_LIGHT)

    def _fetch_question(self):
        diff = self.diff_var.get()
        self.question_lbl.configure(text="Loading question...")
        self.result_lbl.configure(text="")
        self.answer_entry.delete(0, "end")

        def do_fetch():
            return api.get_question(diff)

        def on_done(q_data):
            if not q_data:
                self.question_lbl.configure(text="Could not load question. Is the backend running?")
                return
            self.current_question = q_data
            self.question_lbl.configure(text=q_data["question"])

        self._run_async(do_fetch, on_done)

    def _submit_answer(self):
        if not self.current_question:
            return
        ans_txt = self.answer_entry.get().strip()
        if not ans_txt:
            return

        res = api.submit_answer(self.user_id, self.current_question["id"], ans_txt)
        if not res:
            self.result_lbl.configure(text="Error submitting answer.", text_color=RED)
            return

        pts_earned = res.get("points_earned", 0)
        total_pts = res.get("total_points", self.user.get("points", 0))
        self.user["points"] = total_pts

        if res.get("exact"):
            self.result_lbl.configure(text=f"Correct! +{pts_earned} points", text_color=GREEN)
            # Auto-load next question if provided
            if "next_question" in res:
                self.current_question = res["next_question"]
                self.question_lbl.configure(text=res["next_question"]["question"])
                self.answer_entry.delete(0, "end")  # clear input for next answer
        elif pts_earned > 0:
            self.result_lbl.configure(text=f"Close! +{pts_earned} points", text_color=ORANGE)
        else:
            correct_ans = res.get("correct_answer", "?")
            self.result_lbl.configure(
                text=f"Incorrect. Answer was {correct_ans}", text_color=RED)

        self.live_pts_lbl.configure(text=f"Your points: {total_pts}")


    def show_streaks(self):
        self._clear_main()
        self._set_active_btn(self.streaks_btn)

        ctk.CTkLabel(
            self.main_frame, text="Streak Badges",
            font=ctk.CTkFont(size=26, weight="bold"), text_color=TEXT_COLOR
        ).pack(anchor="w", pady=(5, 5))

        ctk.CTkLabel(
            self.main_frame, text="Earn badges by answering questions correctly in a row!",
            font=ctk.CTkFont(size=13), text_color=TEXT_LIGHT
        ).pack(anchor="w", pady=(0, 15))

        # fetch badge data from backend
        data = api.get_badges(self.user_id)
        if not data:
            ctk.CTkLabel(self.main_frame, text="Could not load badges.",
                        text_color=RED).pack()
            return

        answer_streak = data.get("answer_streak", 0)

        # show current streak
        streak_card = ctk.CTkFrame(self.main_frame, fg_color=CARD_BG, corner_radius=20)
        streak_card.pack(fill="x", pady=(0, 15))
        ctk.CTkLabel(streak_card, text=f"🔥 Current Answer Streak: {answer_streak}",
                    font=ctk.CTkFont(size=16, weight="bold"),
                    text_color=ORANGE).pack(padx=20, pady=15)

        # badge definitions
        badges = [
            (5,   "🥉", "5 in a Row"),
            (10,  "🥈", "10 in a Row"),
            (20,  "🥇", "20 in a Row"),
            (50,  "🌟", "50 in a Row"),
            (75,  "💫", "75 in a Row"),
            (100, "🏆", "100 in a Row"),
            (150, "👑", "150 in a Row"),
            (200, "🔥", "200 in a Row"),
        ]

        # badge grid -- 4 columns
        grid = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        grid.pack(fill="x")
        for i in range(4):
            grid.columnconfigure(i, weight=1)

        for idx, (threshold, emoji, label) in enumerate(badges):
            unlocked = data.get(f"badge_{threshold}", 0) == 1
            card = ctk.CTkFrame(grid,
                                fg_color=CARD_BG if unlocked else BG_COLOR,
                                corner_radius=20,
                                border_width=2,
                                border_color=PURPLE if unlocked else PURPLE_LIGHT)
            card.grid(row=idx//4, column=idx%4, padx=8, pady=8, sticky="nsew")

            ctk.CTkLabel(card, text=emoji if unlocked else "🔒",
                        font=ctk.CTkFont(size=32)).pack(pady=(15, 5))
            ctk.CTkLabel(card, text=label,
                        font=ctk.CTkFont(size=12, weight="bold"),
                        text_color=TEXT_COLOR if unlocked else TEXT_LIGHT).pack()
            ctk.CTkLabel(card, text="Unlocked!" if unlocked else f"Reach {threshold}",
                        font=ctk.CTkFont(size=11),
                        text_color=GREEN if unlocked else TEXT_LIGHT).pack(pady=(2, 15))

    # -- settings tab -------------------------------------------

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
        desc_box.insert("1.0", self.user.get("description", ""))
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

        # save status label
        self.save_msg = ctk.CTkLabel(card, text="", font=ctk.CTkFont(size=12),
                                     text_color=GREEN)
        self.save_msg.pack(anchor="w", padx=20)

        # save btn -- now actually calls backend
        def do_save():
            new_desc = desc_box.get("1.0", "end").strip()
            new_pw = pw_entry.get().strip()
            kwargs = {"description": new_desc}
            if new_pw:
                kwargs["password"] = new_pw
            res = api.update_user(self.user_id, **kwargs)
            if res:
                self.user["description"] = new_desc
                self.save_msg.configure(text="Saved!", text_color=GREEN)
            else:
                self.save_msg.configure(text="Save failed.", text_color=RED)

        ctk.CTkButton(
            card, text="💾  Save Changes",
              font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=PURPLE, hover_color=PURPLE_DARK,
            corner_radius=20, height=42,
            command=do_save
        ).pack(anchor="e", padx=20, pady=(10, 20))


def main():
    # example data; in a real application this would come from the server or
    # login flow
    temp_user = {
        "id": 1,
        "username": "student1",
        "role": "student",
        "points": 0,
        "streak": 0,
        "description": "",
    }

    # class progress data (to be updaetd w/ real api calls)
    app = StudentPage(temp_user)
    app.mainloop()


if __name__ == "__main__":
     main()
