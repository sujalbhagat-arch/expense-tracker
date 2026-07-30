import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from exporter import DataExporter


class AnalyticsPage:

    def __init__(self, app, user):
        self.app = app
        self.user = user

        # Popup Window Setup
        self.window = ctk.CTkToplevel(app)
        self.window.title("📊 Financial Analytics & Insights")
        self.window.geometry("850x600")
        self.window.grab_set()

        # Handle window close protocol gracefully to prevent bgerror/memory leaks
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

        # Title
        title = ctk.CTkLabel(
            self.window,
            text="📊 Expense Analytics",
            font=("Arial", 24, "bold")
        )
        title.pack(pady=(15, 5))

        # Export Buttons Frame
        self.export_frame = ctk.CTkFrame(self.window, fg_color="transparent")
        self.export_frame.pack(pady=5)

        self.csv_btn = ctk.CTkButton(
            self.export_frame,
            text="📄 Export CSV",
            width=140,
            height=32,
            fg_color="#27ae60",
            hover_color="#1e8449",
            command=self.export_csv
        )
        self.csv_btn.grid(row=0, column=0, padx=10)

        self.pdf_btn = ctk.CTkButton(
            self.export_frame,
            text="📕 Export PDF Report",
            width=140,
            height=32,
            fg_color="#c0392b",
            hover_color="#962d22",
            command=self.export_pdf
        )
        self.pdf_btn.grid(row=0, column=1, padx=10)

        # Main Scrollable Frame for Charts
        self.charts_frame = ctk.CTkScrollableFrame(self.window)
        self.charts_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Matplotlib Dark Theme
        plt.style.use("dark_background")

        # Render Charts
        self.render_charts()

    def render_charts(self):
        user_id = self.user[0]

        category_data = self.app.db.get_category_breakdown(user_id)
        monthly_data = self.app.db.get_monthly_spending(user_id)

        if not category_data and not monthly_data:
            no_data_label = ctk.CTkLabel(
                self.charts_frame,
                text="No expenses recorded yet. Add some expenses to view charts!",
                font=("Arial", 16)
            )
            no_data_label.pack(pady=50)
            return

        grid_frame = ctk.CTkFrame(self.charts_frame, fg_color="transparent")
        grid_frame.pack(fill="both", expand=True)

        # Chart 1: Category Breakdown (Pie Chart)
        if category_data:
            categories = [item[0] for item in category_data]
            amounts = [item[1] for item in category_data]

            fig1, ax1 = plt.subplots(figsize=(4.2, 3.6), dpi=100)
            fig1.patch.set_facecolor('#2b2b2b')
            ax1.set_facecolor('#2b2b2b')

            ax1.pie(
                amounts,
                labels=categories,
                autopct='%1.1f%%',
                startangle=140,
                textprops={'color': 'white', 'fontsize': 10}
            )
            ax1.set_title("Spending by Category", color="white", fontsize=14, fontweight="bold")

            canvas1 = FigureCanvasTkAgg(fig1, master=grid_frame)
            canvas1.draw()
            widget1 = canvas1.get_tk_widget()
            widget1.grid(row=0, column=0, padx=10, pady=10)

        # Chart 2: Monthly Spending Trend (Bar Chart)
        if monthly_data:
            months = list(monthly_data.keys())
            amounts = list(monthly_data.values())

            fig2, ax2 = plt.subplots(figsize=(4.2, 3.6), dpi=100)
            fig2.patch.set_facecolor('#2b2b2b')
            ax2.set_facecolor('#2b2b2b')

            ax2.bar(months, amounts, color="#3498db", width=0.5)
            ax2.set_title("Monthly Spending Trend", color="white", fontsize=14, fontweight="bold")
            ax2.set_ylabel("Amount (₹)", color="white")
            ax2.tick_params(colors='white')

            fig2.tight_layout()

            canvas2 = FigureCanvasTkAgg(fig2, master=grid_frame)
            canvas2.draw()
            widget2 = canvas2.get_tk_widget()
            widget2.grid(row=0, column=1, padx=10, pady=10)

    # --------------------------------------------------
    # Export Callbacks
    # --------------------------------------------------
    def export_csv(self):
        expenses = self.app.db.get_all_user_expenses(self.user[0])
        DataExporter.export_to_csv(expenses)

    def export_pdf(self):
        expenses = self.app.db.get_all_user_expenses(self.user[0])
        DataExporter.export_to_pdf(expenses, self.user[1])

    # --------------------------------------------------
    # Clean Close Handler
    # --------------------------------------------------
    def on_close(self):
        plt.close('all')  # Free Matplotlib figure memory
        self.window.destroy()