import tkinter as tk
from tkinter import messagebox
import csv
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

class TeamProgressTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Team Progress Tracker")

        # Create buttons
        self.analytics_button = tk.Button(root, text="View Analytics", command=self.view_analytics)
        self.analytics_button.pack(pady=10)

        self.insert_button = tk.Button(root, text="Insert Progress", command=self.insert_progress)
        self.insert_button.pack(pady=10)

        # Entry variables
        self.task_name_var = tk.StringVar()
        self.exploring_var = tk.StringVar()
        self.development_var = tk.StringVar()
        self.code_reviews_var = tk.StringVar()


    def view_analytics(self):
        # Create analytics window
        analytics_window = tk.Toplevel(self.root)
        analytics_window.title("View Analytics")

        # Load progress data from the CSV file
        file_path = "progress_data.csv"

        if not os.path.isfile(file_path):
            messagebox.showinfo("No Data", "No progress data available for analytics.")
            return

        # Read progress data from CSV file
        data = []
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)

        # Extract fields for plotting
        task_names = [entry["Task Name"] for entry in data]
        exploring_times = [float(entry["Exploring Time"]) if entry["Exploring Time"].replace('.', '').isdigit() else 0 for entry in data]
        development_times = [float(entry["Development Time"]) if entry["Development Time"].replace('.', '').isdigit() else 0 for entry in data]
        code_reviews_times = [float(entry["Code Reviews Time"]) if entry["Code Reviews Time"].replace('.', '').isdigit() else 0 for entry in data]

        # Plot analytics
        fig, ax = plt.subplots(figsize=(8, 5))
        bar_width = 0.2

        bar1 = ax.bar(task_names, exploring_times, bar_width, label='Exploring Time')
        bar2 = ax.bar(task_names, development_times, bar_width, bottom=exploring_times, label='Development Time')
        bar3 = ax.bar(task_names, code_reviews_times, bar_width,
                      bottom=[sum(x) for x in zip(exploring_times, development_times)], label='Code Reviews Time')

        ax.set_ylabel('Time (hours)')
        ax.set_title('Task Progress Analytics')
        ax.legend()

        # Embed the plot in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=analytics_window)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Add a toolbar (optional)
        toolbar = NavigationToolbar2Tk(canvas, analytics_window)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        plt.show()

    def insert_progress(self):
        # Create login window
        login_window = tk.Toplevel(self.root)
        login_window.title("Login")

        # TODO: Implement login logic
        # Labels and Entry widgets for username and password
        username_label = tk.Label(login_window, text="Username:")
        username_entry = tk.Entry(login_window)

        password_label = tk.Label(login_window, text="Password(Student ID):")
        password_entry = tk.Entry(login_window, show="*")  # Entry for password with asterisks for security

        # Function to validate login credentials
        def validate_login():
            # TODO: Replace the following condition with your actual authentication logic
            usernames = ['venkat', 'seshasai', 'vasu', 'shashank', 'tejas', 'yamini', 'pavan', 'manzar', 'amulya', 'bajan']
            passwords = ['500224127', '500224610', '500225013' , '500211952' , '500223651', '500225031', '500225213', '500223652', '500223510', '500223508']
            if username_entry.get() in usernames and password_entry.get() in passwords:
                login_window.destroy()  # Close the login window if credentials are correct
                self.show_progress_form()  # Proceed to progress insertion
            else:
                messagebox.showerror("Login Failed", "Invalid username or password")

        # Button to submit login credentials
        login_button = tk.Button(login_window, text="Login", command=validate_login)

        # Place widgets using grid
        username_label.grid(row=0, column=0, padx=10, pady=10)
        username_entry.grid(row=0, column=1, padx=10, pady=10)

        password_label.grid(row=1, column=0, padx=10, pady=10)
        password_entry.grid(row=1, column=1, padx=10, pady=10)

        login_button.grid(row=2, column=0, columnspan=2, pady=10)

    # If login is successful, proceed to progress insertion
    def show_progress_form(self):
        progress_window = tk.Toplevel(self.root)
        progress_window.title("Insert Progress")

        task_name_label = tk.Label(progress_window, text="Task Name:")
        task_name_entry = tk.Entry(progress_window, textvariable=self.task_name_var)

        exploring_label = tk.Label(progress_window, text="Time taken in Exploring:")
        exploring_entry = tk.Entry(progress_window, textvariable=self.exploring_var)

        development_label = tk.Label(progress_window, text="Time taken in Development:")
        development_entry = tk.Entry(progress_window, textvariable=self.development_var)

        code_reviews_label = tk.Label(progress_window, text="Time taken in Code Reviews/Changes:")
        code_reviews_entry = tk.Entry(progress_window, textvariable=self.code_reviews_var)

        submit_button = tk.Button(progress_window, text="Submit", command=self.submit_progress)

        # TODO: Place widgets using grid or pack
        # Place widgets using grid
        task_name_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        task_name_entry.grid(row=0, column=1, padx=10, pady=10)

        exploring_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        exploring_entry.grid(row=1, column=1, padx=10, pady=10)

        development_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        development_entry.grid(row=2, column=1, padx=10, pady=10)

        code_reviews_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        code_reviews_entry.grid(row=3, column=1, padx=10, pady=10)

        submit_button.grid(row=4, column=0, columnspan=2, pady=10)

    def submit_progress(self):
        #Get data from entry widgets
        task_name = self.task_name_var.get()
        exploring_time = self.exploring_var.get()
        development_time = self.development_var.get()
        code_reviews_time = self.code_reviews_var.get()

        # Validate that all fields are filled
        if not task_name or not exploring_time or not development_time or not code_reviews_time:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        # Format progress data
        progress_data = [task_name, exploring_time, development_time, code_reviews_time]

        # Save progress data to a CSV file
        file_path = "progress_data.csv"

        # Check if the file already exists
        file_exists = os.path.isfile(file_path)

        with open(file_path, mode='a', newline='') as file:
            writer = csv.writer(file)

            # Write header if the file is newly created
            if not file_exists:
                writer.writerow(["Task Name", "Exploring Time", "Development Time", "Code Reviews Time"])

            # Write progress data
            writer.writerow(progress_data)

        messagebox.showinfo("Success", "Progress submitted successfully!")



if __name__ == "__main__":
    root = tk.Tk()
    app = TeamProgressTracker(root)
    root.mainloop()
