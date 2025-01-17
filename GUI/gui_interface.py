from tkinter import *
from tkinter import messagebox

from customtkinter import *
from PIL import Image
from Database import Database
from program_logic import VersionControlSystem
import Pybind11Module

class VersionControlGUI:
    def __init__(self, root):
        self.username = None
        self.vcs = None
        self.root = root
        self.root.title("Version Control System")
        self.root.geometry("600x480")

        self.side_img_data = Image.open("images/side-img.png")
        self.password_icon_data = Image.open("images/password-icon.png")
        self.google_icon_data = Image.open("images/google-icon.png")
        self.background_data = Image.open("images/back-ground.png")
        self.background_image = CTkImage(dark_image=self.background_data, light_image=self.background_data,
                                         size=(600, 400))

        self.side_img = CTkImage(dark_image=self.side_img_data, light_image=self.side_img_data, size=(300, 480))
        self.password_icon = CTkImage(dark_image=self.password_icon_data, light_image=self.password_icon_data,
                                      size=(17, 17))
        self.google_icon = CTkImage(dark_image=self.google_icon_data, light_image=self.google_icon_data, size=(17, 17))

        self.init_login_menu()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def init_login_menu(self):
        self.clear_window()
        CTkLabel(master=self.root, text="", image=self.side_img).pack(expand=True, side="left")

        # Right frame
        frame = CTkFrame(master=self.root, width=300, height=480, fg_color="#ffffff")
        frame.pack_propagate(0)
        frame.pack(expand=True, side="right")

        CTkLabel(master=frame, text="Welcome Back!", text_color="#601E88", anchor="w",
                 font=("Arial Bold", 24)).pack(anchor="w", pady=(50, 5), padx=(25, 0))
        CTkLabel(master=frame, text="Sign in to your account", text_color="#7E7E7E", anchor="w",
                 font=("Arial Bold", 12)).pack(anchor="w", padx=(25, 0))

        CTkLabel(master=frame, text="  User:", text_color="#601E88", anchor="w",
                 font=("Arial Bold", 14),  compound="left").pack(anchor="w", pady=(38, 0),
                                                                                       padx=(25, 0))
        self.username_entry = CTkEntry(master=frame, width=225, fg_color="#EEEEEE", border_color="#601E88",
                                       border_width=1, text_color="#000000")
        self.username_entry.pack(anchor="w", padx=(25, 0))

        CTkLabel(master=frame, text="  Password:", text_color="#601E88", anchor="w",
                 font=("Arial Bold", 14), image=self.password_icon, compound="left").pack(anchor="w", pady=(21, 0),
                                                                                          padx=(25, 0))
        self.password_entry = CTkEntry(master=frame, width=225, fg_color="#EEEEEE", border_color="#601E88",
                                       border_width=1, text_color="#000000", show="*")
        self.password_entry.pack(anchor="w", padx=(25, 0))

        CTkButton(master=frame, text="Login", fg_color="#601E88", hover_color="#E44982", font=("Arial Bold", 12),
                  text_color="#ffffff", width=225, command=self.authenticate_user).pack(anchor="w", pady=(40, 0),
                                                                                        padx=(25, 0))
        CTkButton(master=frame, text="Register", fg_color="#601E88", hover_color="#E44982", font=("Arial Bold", 12),
                  text_color="#ffffff", width=225, command=lambda: self.init_register_menu()).pack(anchor="w", pady=(40, 0),
                                                                                    padx=(25, 0))


    def init_register_menu(self):
        self.clear_window()

        CTkLabel(master=self.root, text="", image=self.side_img).pack(expand=True, side="left")

        # Right frame
        frame = CTkFrame(master=self.root, width=300, height=480, fg_color="#ffffff")
        frame.pack_propagate(0)
        frame.pack(expand=True, side="right")

        CTkLabel(master=frame, text="Welcome!", text_color="#601E88", anchor="w",
                 font=("Arial Bold", 24)).pack(anchor="w", pady=(50, 5), padx=(25, 0))
        CTkLabel(master=frame, text="Create a new account", text_color="#7E7E7E", anchor="w",
                 font=("Arial Bold", 12)).pack(anchor="w", padx=(25, 0))

        CTkLabel(master=frame, text="  Username:", text_color="#601E88", anchor="w",
                 font=("Arial Bold", 14)).pack(anchor="w", pady=(38, 0), padx=(25, 0))
        self.register_username_entry = CTkEntry(master=frame, width=225, fg_color="#EEEEEE", border_color="#601E88",
                                                border_width=1, text_color="#000000")
        self.register_username_entry.pack(anchor="w", padx=(25, 0))

        CTkLabel(master=frame, text="  Password:", text_color="#601E88", anchor="w",
                 font=("Arial Bold", 14)).pack(anchor="w", pady=(21, 0), padx=(25, 0))
        self.register_password_entry = CTkEntry(master=frame, width=225, fg_color="#EEEEEE", border_color="#601E88",
                                                border_width=1, text_color="#000000", show="*")
        self.register_password_entry.pack(anchor="w", padx=(25, 0))

        CTkLabel(master=frame, text="  Confirm Password:", text_color="#601E88", anchor="w",
                 font=("Arial Bold", 14)).pack(anchor="w", pady=(21, 0), padx=(25, 0))
        self.register_confirm_password_entry = CTkEntry(master=frame, width=225, fg_color="#EEEEEE",
                                                        border_color="#601E88", border_width=1,
                                                        text_color="#000000", show="*")
        self.register_confirm_password_entry.pack(anchor="w", padx=(25, 0))

        CTkButton(master=frame, text="Register", fg_color="#601E88", hover_color="#E44982", font=("Arial Bold", 12),
                  text_color="#ffffff", width=225, command=self.register_user).pack(anchor="w", pady=(40, 0),
                                                                                    padx=(25, 0))

    def register_user(self):
        username = self.register_username_entry.get()
        password = self.register_password_entry.get()
        confirm_password = self.register_confirm_password_entry.get()

        if password != confirm_password:
            messagebox.showerror("Registration Failed", "Passwords do not match")

        elif not username or not password:
            messagebox.showerror("Registration Failed", "All fields are required")
        else:
            db = Database()
            db.add_user(username, password, False)
            messagebox.showinfo("Registration Successful", "Account created successfully!")
            self.init_login_menu()

    def authenticate_user(self):
        self.username = self.username_entry.get()
        password = self.password_entry.get()

        db = Database()
        user_data = db.authenticate_user(self.username, password)

        if user_data:
            if db.is_admin(self.username):
                self.button_list = db.get_all_repositories()
                messagebox.showinfo("Login Successful", "Admin account is logged in!")
                self.init_second_window()
            else:
                tmp = db.get_user_repositories(user_data[0])
                self.button_list = Pybind11Module.selection_sort(tmp)
                messagebox.showinfo("Login Successful", f"Welcome, {self.username}!")
                self.init_second_window()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def init_second_window(self):
        self.clear_frame()

        CTkFrame(master=self.root, fg_color="#000000").place(relwidth=1, relheight=1)

        CTkLabel(master=self.root, image=self.background_image, text="").place(relwidth=1, relheight=1)

        top_frame = CTkFrame(master=self.root, height=50, fg_color="#F0F0F0")
        top_frame.place(relwidth=1, y=0)

        CTkButton(master=top_frame, text="Logout", fg_color="#E44982", text_color="#FFFFFF",
                  width=100, command=self.init_login_menu).pack(side="left", padx=10, pady=10)

        CTkButton(master=top_frame, text="Add", fg_color="#601E88", text_color="#FFFFFF",
                  width=100, command=self.init_repository_menu).pack(side="right", padx=10, pady=10)

        self.button_frame = CTkFrame(master=self.root, fg_color="transparent", width=500, height=300)
        self.button_frame.place(relx=0.5, rely=0.3, anchor="n")

        self.add_new_buttons()

    def add_new_buttons(self):
        for widget in self.button_frame.winfo_children():
            widget.destroy()

        for repo_name in self.button_list:
            CTkButton(
                master=self.button_frame,
                text=repo_name,
                fg_color="#601E88",
                text_color="#FFFFFF",
                command=lambda name=repo_name: self.button_action(name)
            ).pack(pady=5, padx=10, fill="x")

    def button_action(self, button_text):
        if isinstance(button_text, tuple):
            self.vcs = VersionControlSystem(button_text[0])
        else:
            self.vcs = VersionControlSystem(button_text)
        self.init_main_menu()

    def init_repository_menu(self):
        self.clear_window()

        CTkLabel(master=self.root, text="", image=self.side_img).pack(expand=True, side="right")

        frame = CTkFrame(master=self.root, width=300, height=480, fg_color="#ffffff")
        frame.pack_propagate(0)
        frame.pack(expand=True, side="left")

        CTkLabel(master=frame, text="Enter repository name", text_color="#601E88", anchor="w",
                 font=("Arial Bold", 14)).pack(anchor="w", pady=(50, 5), padx=(25, 0))

        self.repository_name_entry = CTkEntry(master=frame, width=225, fg_color="#EEEEEE", border_color="#601E88",
                                              border_width=1, text_color="#000000")
        self.repository_name_entry.pack(anchor="w", padx=(25, 0))

        CTkButton(master=frame, text="Submit", fg_color="#601E88", hover_color="#E44982", font=("Arial Bold", 12),
                  text_color="#ffffff", width=225, command=self.submit_repository).pack(anchor="w", pady=(40, 0),
                                                                                        padx=(25, 0))

    def submit_repository(self):
        repository_name = self.repository_name_entry.get().strip()

        if not repository_name:
            messagebox.showerror("Error", "Please enter a repository name")
            return

        db = Database()
        user_id = db.get_user_id_by_username(self.username)

        db.add_repository(user_id, repository_name)

        self.button_list.append(repository_name)
        self.button_list = Pybind11Module.selection_sort(self.button_list)
        messagebox.showinfo("Successful", "Repository added")
        self.init_second_window()

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def init_main_menu(self):
        self.clear_window()

        self.main_menu_frame = CTkFrame(self.root, fg_color="#ffffff", width=400, height=500, corner_radius=15)
        self.main_menu_frame.pack_propagate(0)
        self.main_menu_frame.pack(pady=50, padx=50, anchor="center")

        CTkButton(
            master=self.main_menu_frame,
            text="Exit",
            fg_color="#E74C3C",
            hover_color="#C0392B",
            text_color="#ffffff",
            font=("Arial Bold", 12),
            corner_radius=8,
            width=70,
            height=25,
            command=self.init_second_window
        ).pack(anchor="nw", padx=10, pady=10)

        CTkLabel(
            self.main_menu_frame,
            text="Version Control System",
            font=("Arial Bold", 16),
            text_color="#601E88"
        ).pack(pady=(20, 10))

        button_style = {
            "master": self.main_menu_frame,
            "fg_color": "#601E88",
            "hover_color": "#8E44AD",
            "text_color": "#ffffff",
            "font": ("Arial Bold", 12),
            "corner_radius": 8,
            "width": 200,
            "height": 35
        }

        CTkButton(**button_style, text="Add File", command=self.add_file_menu).pack(pady=5)
        CTkButton(**button_style, text="Commit Changes", command=self.commit_changes_menu).pack(pady=5)
        CTkButton(**button_style, text="Check Changes", command=self.view_changes_from_file).pack(pady=5)  # Нова кнопка
        CTkButton(**button_style, text="View Logs", command=self.view_logs).pack(pady=5)
        CTkButton(**button_style, text="Clone Repo", command=self.clone_menu).pack(pady=5)
        CTkButton(**button_style, text="Delete Repo", command=self.delete_repo_action).pack(pady=5)

    def delete_repo_action(self):

        if self.vcs.delete_repo():
            db = Database()
            db.delete_repository(self.vcs.get_repository_name())
            self.button_list.remove(self.vcs.get_repository_name())
            messagebox.showinfo("Successful", "Repository deleted")
            self.init_second_window()
        else:
            messagebox.showerror("Error", "Repository not deleted")

    def add_file_menu(self):
        self.clear_window()

        CTkLabel(master=self.root, text="", image=self.side_img).pack(expand=True, side="right")

        frame = CTkFrame(master=self.root, width=300, height=480, fg_color="#ffffff", corner_radius=15)
        frame.pack_propagate(0)
        frame.pack(expand=True, side="left")

        CTkLabel(
            master=frame,
            text="File Path:",
            font=("Arial Bold", 14),
            text_color="#601E88",
            anchor="w"
        ).pack(anchor="w", pady=(50, 5), padx=(25, 0))

        self.file_entry = CTkEntry(
            master=frame,
            width=225,
            fg_color="#EEEEEE",
            border_color="#601E88",
            border_width=1,
            text_color="#000000"
        )
        self.file_entry.pack(anchor="w", padx=(25, 0), pady=(0, 20))

        CTkButton(
            master=frame,
            text="Add",
            fg_color="#601E88",
            hover_color="#8E44AD",
            text_color="#ffffff",
            font=("Arial Bold", 14),
            corner_radius=10,
            width=225,
            height=40,
            command=self.add_file_action
        ).pack(anchor="w", padx=(25, 0), pady=(10, 10))

        CTkButton(
            master=frame,
            text="Back",
            fg_color="#E74C3C",
            hover_color="#C0392B",
            text_color="#ffffff",
            font=("Arial Bold", 14),
            corner_radius=10,
            width=225,
            height=40,
            command=self.init_main_menu
        ).pack(anchor="w", padx=(25, 0), pady=(10, 10))
    def add_file_action(self):
        file_path = self.file_entry.get()
        try:
            file_hash = self.vcs.add_file(file_path)
            messagebox.showinfo("File Added", f"File added with hash: {file_hash}")
            self.init_main_menu()
        except FileNotFoundError as e:
            messagebox.showerror("Error", str(e))

    def commit_changes_menu(self):
        self.clear_window()

        CTkLabel(master=self.root, text="", image=self.side_img).pack(expand=True, side="right")

        frame = CTkFrame(master=self.root, width=300, height=480, fg_color="#ffffff", corner_radius=15)
        frame.pack_propagate(0)
        frame.pack(expand=True, side="left")

        CTkLabel(
            master=frame,
            text="Commit Message:",
            font=("Arial Bold", 14),
            text_color="#601E88",
            anchor="w"
        ).pack(anchor="w", pady=(50, 5), padx=(25, 0))

        self.commit_entry = CTkEntry(
            master=frame,
            width=225,
            fg_color="#EEEEEE",
            border_color="#601E88",
            border_width=1,
            text_color="#000000"
        )
        self.commit_entry.pack(anchor="w", padx=(25, 0), pady=(0, 20))

        CTkButton(
            master=frame,
            text="Commit",
            fg_color="#601E88",
            hover_color="#8E44AD",
            text_color="#ffffff",
            font=("Arial Bold", 14),
            corner_radius=10,
            width=225,
            height=40,
            command=self.commit_action
        ).pack(anchor="w", padx=(25, 0), pady=(10, 10))

        CTkButton(
            master=frame,
            text="Back",
            fg_color="#E74C3C",
            hover_color="#C0392B",
            text_color="#ffffff",
            font=("Arial Bold", 14),
            corner_radius=10,
            width=225,
            height=40,
            command=self.init_main_menu
        ).pack(anchor="w", padx=(25, 0), pady=(10, 10))

    def clone_menu(self):
        self.clear_window()

        CTkLabel(master=self.root, text="", image=self.side_img).pack(expand=True, side="right")

        frame = CTkFrame(master=self.root, width=300, height=480, fg_color="#ffffff", corner_radius=15)
        frame.pack_propagate(0)
        frame.pack(expand=True, side="left")

        CTkLabel(
            master=frame,
            text="Clone Path:",
            font=("Arial Bold", 14),
            text_color="#601E88",
            anchor="w"
        ).pack(anchor="w", pady=(50, 5), padx=(25, 0))

        self.clone_entry = CTkEntry(
            master=frame,
            width=225,
            fg_color="#EEEEEE",
            border_color="#601E88",
            border_width=1,
            text_color="#000000"
        )
        self.clone_entry.pack(anchor="w", padx=(25, 0), pady=(0, 20))

        CTkButton(
            master=frame,
            text="Clone",
            fg_color="#601E88",
            hover_color="#8E44AD",
            text_color="#ffffff",
            font=("Arial Bold", 14),
            corner_radius=10,
            width=225,
            height=40,
            command=self.clone_action
        ).pack(anchor="w", padx=(25, 0), pady=(10, 10))

        CTkButton(
            master=frame,
            text="Back",
            fg_color="#E74C3C",
            hover_color="#C0392B",
            text_color="#ffffff",
            font=("Arial Bold", 14),
            corner_radius=10,
            width=225,
            height=40,
            command=self.init_main_menu
        ).pack(anchor="w", padx=(25, 0), pady=(10, 10))

    def clone_action(self):
        path = self.clone_entry.get()
        try:
            self.vcs.clone_repository(path)
            messagebox.showinfo("Successful", "Clone successful")
            self.init_main_menu()
        except FileNotFoundError as e:
            messagebox.showerror("Error", str(e))

    def commit_action(self):
        message = self.commit_entry.get()

        files = os.listdir(self.vcs.files_dir)
        files = [os.path.join(self.vcs.files_dir, file) for file in files]

        if not files:
            messagebox.showerror("Error", "No files to commit.")
            return

        try:
            commit_data = self.vcs.commit(message, files)
            messagebox.showinfo("Commit Created",
                                f"Commit created:\nVersion: {commit_data['version']}\nMessage: {commit_data['message']}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

        self.init_main_menu()

    def view_logs(self):
        self.clear_window()

        CTkLabel(master=self.root, text="", image=self.side_img).pack(expand=True, side="right")

        frame = CTkFrame(master=self.root, width=300, height=480, fg_color="#ffffff", corner_radius=15)
        frame.pack_propagate(0)
        frame.pack(expand=True, side="left")

        CTkLabel(
            master=frame,
            text="Commit Log:",
            font=("Arial Bold", 14),
            text_color="#601E88",
            anchor="w"
        ).pack(anchor="w", pady=(20, 10), padx=(25, 0))

        log_scrollable_frame = CTkScrollableFrame(master=frame, width=250, height=350)
        log_scrollable_frame.pack(anchor="w", padx=(25, 0), pady=(10, 10))

        commits = self.vcs.get_commits()
        if not commits:
            CTkLabel(
                master=log_scrollable_frame,
                text="No commits found.",
                font=("Arial Bold", 12),
                text_color="#7E7E7E",
                anchor="w"
            ).pack(anchor="w", pady=(10, 0), padx=(10, 0))
        else:
            for commit in commits:
                CTkLabel(
                    master=log_scrollable_frame,
                    text=f"Timestamp: {commit['timestamp']}",
                    font=("Arial Bold", 12),
                    text_color="#FFFFFF",
                    anchor="w"
                ).pack(anchor="w", pady=(5, 0), padx=(10, 0))

                CTkLabel(
                    master=log_scrollable_frame,
                    text=f"Message: {commit['message']}",
                    font=("Arial", 12),
                    text_color="#CCCCCC",
                    anchor="w"
                ).pack(anchor="w", pady=(2, 0), padx=(10, 0))

                CTkLabel(
                    master=log_scrollable_frame,
                    text=f"Files: {', '.join(commit['files'])}",
                    font=("Arial", 12),
                    text_color="#BBBBBB",
                    anchor="w"
                ).pack(anchor="w", pady=(2, 0), padx=(10, 0))

                CTkLabel(
                    master=log_scrollable_frame,
                    text="---",
                    font=("Arial", 12),
                    text_color="#FFFFFF",
                    anchor="w"
                ).pack(anchor="w", pady=(5, 0), padx=(10, 0))

        CTkButton(
            master=frame,
            text="Back",
            fg_color="#E74C3C",
            hover_color="#C0392B",
            text_color="#ffffff",
            font=("Arial Bold", 14),
            corner_radius=10,
            width=225,
            height=40,
            command=self.init_main_menu
        ).pack(anchor="w", padx=(25, 0), pady=(10, 10))

    def view_changes_from_file(self):
        self.clear_window()

        CTkLabel(master=self.root, text="", image=self.side_img).pack(expand=True, side="right")

        frame = CTkFrame(master=self.root, width=400, height=480, fg_color="#ffffff", corner_radius=15)
        frame.pack_propagate(0)
        frame.pack(expand=True, side="left")

        CTkLabel(
            master=frame,
            text="Changes from File:",
            font=("Arial Bold", 14),
            text_color="#601E88",
            anchor="w"
        ).pack(anchor="w", pady=(20, 10), padx=(25, 0))

        # Додаємо Canvas для горизонтальної та вертикальної прокрутки
        canvas = Canvas(master=frame, width=350, height=350, bg="#ffffff", highlightthickness=0)
        canvas.pack(anchor="w", padx=(25, 0), pady=(10, 10), fill="both", expand=True)

        # Створюємо Scrollbar'и
        vertical_scrollbar = Scrollbar(master=frame, orient="vertical", command=canvas.yview)
        vertical_scrollbar.pack(side="right", fill="y")

        horizontal_scrollbar = Scrollbar(master=frame, orient="horizontal", command=canvas.xview)
        horizontal_scrollbar.pack(side="bottom", fill="x")

        canvas.configure(yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)

        # Додаємо Frame для тексту всередині Canvas
        log_scrollable_frame = Frame(master=canvas, bg="#ffffff")
        canvas.create_window((0, 0), window=log_scrollable_frame, anchor="nw")

        # Додаємо текст із файлу
        try:
            with open(self.vcs.changes_file, "r", encoding="cp1251") as file:
                logs = file.readlines()
        except FileNotFoundError:
            Label(
                master=log_scrollable_frame,
                text="Changes file not found.",
                font=("Arial Bold", 12),
                fg="#FFFFFF",
                bg="#601E88",
                anchor="w"
            ).pack(anchor="w", pady=(10, 0), padx=(10, 0))
            return

        if not logs:
            Label(
                master=log_scrollable_frame,
                text="No changes found.",
                font=("Arial Bold", 12),
                fg="#601E88",
                bg="#ffffff",
                anchor="w"
            ).pack(anchor="w", pady=(10, 0), padx=(10, 0))
        else:
            for line in logs:
                line = line.strip()
                if not line:
                    continue

                Label(
                    master=log_scrollable_frame,
                    text=line,
                    font=("Arial", 12),
                    fg="#000000",
                    bg="#ffffff",
                    anchor="w"
                ).pack(anchor="w", pady=(5, 0), padx=(10, 0))

        # Оновлюємо розміри Canvas при зміні вмісту
        log_scrollable_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        CTkButton(
            master=frame,
            text="Back",
            fg_color="#E74C3C",
            hover_color="#C0392B",
            text_color="#ffffff",
            font=("Arial Bold", 14),
            corner_radius=10,
            width=325,
            height=40,
            command=self.init_main_menu
        ).pack(anchor="w", padx=(25, 0), pady=(10, 10))

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def run(self):
        self.root.mainloop()

