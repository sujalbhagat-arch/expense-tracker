import csv
from tkinter import filedialog, messagebox
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


class DataExporter:

    @staticmethod
    def export_to_csv(expenses):
        """Export expenses list to a CSV file."""
        if not expenses:
            messagebox.showwarning("Warning", "No expenses available to export!")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")],
            title="Save Expense Report as CSV"
        )

        if not file_path:
            return

        try:
            with open(file_path, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["Date", "Category", "Description", "Amount (INR)"])
                for exp in expenses:
                    writer.writerow([exp[0], exp[1], exp[2] or "-", f"{exp[3]:.2f}"])

            messagebox.showinfo("Success", f"CSV Report exported successfully!\nSaved to: {file_path}")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export CSV: {str(e)}")

    @staticmethod
    def export_to_pdf(expenses, username):
        """Export expenses list to a styled PDF report."""
        if not expenses:
            messagebox.showwarning("Warning", "No expenses available to export!")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")],
            title="Save Expense Report as PDF"
        )

        if not file_path:
            return

        try:
            doc = SimpleDocTemplate(file_path, pagesize=letter)
            elements = []
            styles = getSampleStyleSheet()

            # Title & Subtitle
            title_style = ParagraphStyle(
                'ReportTitle',
                parent=styles['Heading1'],
                fontSize=20,
                textColor=colors.HexColor("#2c3e50"),
                spaceAfter=10
            )
            elements.append(Paragraph("💰 Smart Expense Tracker Report", title_style))
            elements.append(Paragraph(f"User: <b>{username}</b>", styles['Normal']))
            elements.append(Spacer(1, 15))

            # Table Data Setup
            table_data = [["Date", "Category", "Description", "Amount (₹)"]]
            total_sum = 0.0

            for exp in expenses:
                amount = float(exp[3])
                total_sum += amount
                table_data.append([
                    str(exp[0]),
                    str(exp[1]),
                    str(exp[2] or "-"),
                    f"₹{amount:.2f}"
                ])

            table_data.append(["", "", "Total Spent:", f"₹{total_sum:.2f}"])

            # Styling the PDF Table
            pdf_table = Table(table_data, colWidths=[100, 120, 180, 100])
            pdf_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#34495e")),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('BACKGROUND', (0, 1), (-1, -2), colors.HexColor("#f8f9fa")),
                ('GRID', (0, 0), (-1, -2), 0.5, colors.HexColor("#bdc3c7")),
                ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                ('LINEABOVE', (2, -1), (3, -1), 1.5, colors.HexColor("#2c3e50")),
            ]))

            elements.append(pdf_table)
            doc.build(elements)

            messagebox.showinfo("Success", f"PDF Report generated successfully!\nSaved to: {file_path}")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export PDF: {str(e)}")