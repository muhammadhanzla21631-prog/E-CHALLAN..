
from fpdf import FPDF
from datetime import datetime

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'E-Challan System - Project Report', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 6, title, 0, 1, 'L', 1)
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Arial', '', 10)
        self.multi_cell(0, 5, body)
        self.ln()

    def bullet_point(self, text):
        self.set_font('Arial', '', 10)
        self.cell(5)
        self.cell(0, 5, f"- {text}", 0, 1)

def create_report():
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    
    # Title Info
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 5, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 0, 1, 'R')
    pdf.ln(10)

    # 1. Project Overview
    pdf.chapter_title("1. Project Overview")
    pdf.chapter_body(
        "The E-Challan System is a comprehensive solution designed to automate traffic violation detection and management. "
        "It consists of a robust Backend API, a dynamic Web Frontend for monitoring and analytics, and an Android Application for mobile access."
    )

    # 2. Backend (FastAPI)
    pdf.chapter_title("2. Backend (FastAPI)")
    pdf.chapter_body("The backend is built using FastAPI and SQLModel, providing a high-performance REST API.")
    
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(0, 6, "Key Features:", 0, 1)
    pdf.bullet_point("Core API: Camera management, Challan issuance, and Image Prediction.")
    pdf.bullet_point("Authentication: User Registration and Login with secure password hashing.")
    pdf.bullet_point("Database: SQLite database with SQLModel ORM for efficient data handling.")
    pdf.bullet_point("Analytics: Endpoints for violation stats, revenue, and camera performance.")
    pdf.bullet_point("User Management: Profile viewing and updating.")
    pdf.bullet_point("Challan Management: Detailed history, filtering, and vehicle lookup.")
    pdf.bullet_point("Payments: Payment processing simulation and history tracking.")
    pdf.bullet_point("Appeals System: Users can submit appeals; Admins can review them.")
    pdf.bullet_point("Search: Universal search across vehicles, challans, and cameras.")
    pdf.bullet_point("Camera Health: Monitoring system for camera status and maintenance.")
    pdf.bullet_point("Notifications: Integration with FCM (Push), Email (Gmail), and WhatsApp (Twilio).")
    pdf.bullet_point("Testing Infrastructure: Automated Python script to verify API health, analytics, and prediction endpoints.")
    pdf.ln(2)

    # 3. Frontend (Web)
    pdf.chapter_title("3. Frontend (Web)")
    pdf.chapter_body("The web interface is built with HTML, CSS, and Vanilla JavaScript, utilizing Leaflet for mapping.")
    
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(0, 6, "Key Features:", 0, 1)
    pdf.bullet_point("Interactive Map: Real-time camera visualization using Leaflet.js.")
    pdf.bullet_point("Live Monitoring: Simulated activity feed and real-time statistics.")
    pdf.bullet_point("Violation Detection: 'Over Speed' and 'Slow Speed' alerts with visual warnings.")
    pdf.bullet_point("Dashboard: Analytics charts for violation trends and camera performance.")
    pdf.bullet_point("Vehicle Lookup: Search tool for vehicle history and fines.")
    pdf.bullet_point("Theme Support: Toggle between Light and Dark modes.")
    pdf.bullet_point("Voice Alerts: Text-to-speech notifications for critical events.")
    pdf.bullet_point("Image Upload: Interface to upload evidence and get AI predictions.")
    pdf.ln(2)

    # 4. Android Application
    pdf.chapter_title("4. Android Application")
    pdf.chapter_body("The Android app is developed using Kotlin and Jetpack Compose.")
    
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(0, 6, "Key Features:", 0, 1)
    pdf.bullet_point("Modern UI: Built with Jetpack Compose for a responsive interface.")
    pdf.bullet_point("Google Maps Integration: Displays traffic cameras on a native map.")
    pdf.bullet_point("Real-time Data: Fetches camera data directly from the Backend API.")
    pdf.bullet_point("Marker System: Visual markers for camera locations.")
    pdf.ln(2)

    # 5. Conclusion
    pdf.chapter_title("5. Conclusion")
    pdf.chapter_body(
        "The project has successfully implemented the core pillars of a modern traffic management system. "
        "The integration between the Backend, Web Frontend, and Android App ensures a seamless flow of data "
        "and real-time responsiveness."
    )

    output_path = "Project_Completion_Report.pdf"
    pdf.output(output_path, 'F')
    print(f"Report generated: {output_path}")

if __name__ == "__main__":
    create_report()
