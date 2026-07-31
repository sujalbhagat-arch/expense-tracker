import customtkinter as ctk
from tkinter import messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv


class AnalyticsPage:

    def __init__(self, parent, user):
        self.app = parent
        self.user = user
        self.is_destroyed = False

        # Window Setup
        self.window = ctk.CTkToplevel(parent)
        self.window.title("Financial Analytics & Insights")
        self.window.geometry("750x650")
        self.window.grab_set()
        
        # Handle graceful close
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

        # Title Header
        ctk.CTkLabel(
            self.window,
            text="📊 Expense Analytics",
            font=("Arial", 20, "bold")
        ).pack(pady=(15, 10))

        # Top Export Bar
        export_frame = ctk.CTkFrame(self.window, fg_color="transparent")
        export_frame.pack(fill="x", padx=20, pady=(0, 10))

        ctk.CTkButton(
            export_frame,
            text="📄 Export CSV",
            fg_color="#10b981",
            hover_color="#059669",
            command=self.export_csv
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            export_frame,
            text="📕 Export PDF Report",
            fg_color="#ef4444",
            hover_color="#dc2626",
            command=self.export_pdf
        ).pack(side="right", padx=10)

        # Scrollable Frame for Charts
        self.scroll_frame = ctk.CTkScrollableFrame(self.window, corner_radius=12)
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=(0, 15))

        # Render Charts
        self.render_charts()

    def on_close(self):
        self.is_destroyed = True
        plt.close("all")
        self.window.destroy()

    def render_charts(self):
        if self.is_destroyed:
            return

        # Safely fetch category breakdown from DB
        if hasattr(self.app.db, "get_category_breakdown"):
            category_data = self.app.db.get_category_breakdown(self.user[0])
        else:
            expenses = self.app.db.get_filtered_expenses(self.user[0], "All")
            category_data = {}
            for exp in expenses:
                category_data[exp[2]] = category_data.get(exp[2], 0.0) + exp[1]

        if not category_data:
            ctk.CTkLabel(
                self.scroll_frame,
                text="No expense data available to display charts.",
                font=("Arial", 14),
                text_color="#a1a1aa"
            ).pack(pady=50)
            return

        categories = list(category_data.keys())
        amounts = list(category_data.values())

        # Match Theme Background
        mode = ctk.get_appearance_mode()
        bg_color = "#18181b" if mode == "Dark" else "#f4f4f5"
        text_color = "white" if mode == "Dark" else "black"

        plt.style.use("dark_background" if mode == "Dark" else "default")
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.5, 3.8), facecolor=bg_color)

        # 1. Pie Chart
        colors = ["#3b82f6", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6", "#ec4899", "#14b8a6"]
        ax1.set_facecolor(bg_color)
        ax1.pie(
            amounts,
            labels=categories,
            autopct="%1.1f%%",
            startangle=140,
            colors=colors[:len(categories)],
            textprops={"color": text_color, "fontsize": 9}
        )
        ax1.set_title("Category Share", color=text_color, fontsize=11, fontweight="bold")

        # 2. Bar Chart
        ax2.set_facecolor(bg_color)
        ax2.bar(categories, amounts, color="#3b82f6", width=0.5)
        ax2.set_title("Category Totals (₹)", color=text_color, fontsize=11, fontweight="bold")
        ax2.tick_params(colors=text_color, labelsize=8)
        plt.xticks(rotation=20)

        ax2.spines["top"].set_visible(False)
        ax2.spines["right"].set_visible(False)
        ax2.spines["left"].set_color("#3f3f46" if mode == "Dark" else "#e4e4e7")
        ax2.spines["bottom"].set_color("#3f3f46" if mode == "Dark" else "#e4e4e7")

        fig.tight_layout()

        if self.is_destroyed:
            plt.close(fig)
            return

        # Embed into Canvas
        canvas = FigureCanvasTkAgg(fig, master=self.scroll_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, pady=10)

    def export_csv(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")],
            title="Save Expense Report CSV"
        )
        if file_path:
            expenses = self.app.db.get_filtered_expenses(self.user[0], "All")
            with open(file_path, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Amount (INR)", "Category", "Description", "Date", "Payment Method"])
                for exp in expenses:
                    writer.writerow(exp)
            messagebox.showinfo("Success", "CSV report exported successfully!")

    def export_pdf(self):
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.pdfgen import canvas
        except ImportError:
            messagebox.showerror("Error", "ReportLab missing! Run: pip install reportlab")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")],
            title="Save Expense Report PDF"
        )
        if file_path:
            expenses = self.app.db.get_filtered_expenses(self.user[0], "All")
            c = canvas.Canvas(file_path, pagesize=letter)
            c.setFont("Helvetica-Bold", 18)
            c.drawString(50, 750, f"Expense Report - {self.user[1]}")
            c.setFont("Helvetica", 10)
            c.drawString(50, 735, "---------------------------------------------------------------------------------------------------")

            y = 710
            c.setFont("Helvetica-Bold", 10)
            c.drawString(50, y, "Date")
            c.drawString(130, y, "Category")
            c.drawString(250, y, "Payment")
            c.drawString(360, y, "Amount (INR)")
            c.drawString(460, y, "Description")

            y -= 20
            c.setFont("Helvetica", 9)
            for exp in expenses:
                if y < 50:
                    c.showPage()
                    y = 750
                c.drawString(50, y, str(exp[4]))
                c.drawString(130, y, str(exp[2]))
                c.drawString(250, y, str(exp[5] if len(exp) > 5 else "UPI"))
                c.drawString(360, y, f"Rs. {exp[1]:.2f}")
                c.drawString(460, y, str(exp[3])[:20])
                y -= 18

            c.save()
            messagebox.showinfo("Success", "PDF report exported successfully!")