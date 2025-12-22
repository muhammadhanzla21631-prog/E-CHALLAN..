from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'E-Challan Project - Remaining Tasks', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

    def section_title(self, title):
        self.set_font('Arial', 'B', 14)
        self.set_fill_color(230, 230, 230)
        self.cell(0, 10, title, 0, 1, 'L', 1)
        self.ln(4)

    def task_item(self, task, description):
        self.set_font('Arial', 'B', 11)
        self.cell(10)
        self.cell(0, 6, f"- {task}", 0, 1)
        self.set_font('Arial', '', 10)
        self.cell(15)
        self.multi_cell(0, 5, description)
        self.ln(3)

pdf = PDF()
pdf.alias_nb_pages()
pdf.add_page()

# Frontend Tasks
pdf.section_title('1. Frontend Development (HTML/JS/CSS)')
pdf.task_item("Payment Integration UI", "Create a dedicated page or modal for paying challans. Connect it to the '/api/payment' endpoint and handle success/failure states.")
pdf.task_item("Appeals Interface", "Build a form for users to submit appeals against challans (Reason, Evidence). Add a view to track appeal status.")
pdf.task_item("User Profile Dashboard", "Implement a profile page where users can view and update their details (Name, Phone, CNIC) using the '/api/user/{id}' endpoints.")
pdf.task_item("Challan History View", "Create a detailed list view (Table/Grid) of all past challans with filtering capabilities (Paid, Unpaid, Date).")
pdf.task_item("Admin Panel", "Develop a separate, protected dashboard for admins to add cameras, review appeals, and view system health statistics.")
pdf.task_item("Live Camera Feed Component", "Implement a video player component to display RTSP streams (or mock streams) for selected cameras.")

# Backend Tasks
pdf.section_title('2. Backend Development (FastAPI/Python)')
pdf.task_item("Real Payment Gateway", "Replace the current mock payment implementation with a real gateway integration like Stripe or JazzCash.")
pdf.task_item("Notification System", "Integrate SMTP (Email) or Twilio (SMS) to send real alerts for challan issuance and payment confirmation.")
pdf.task_item("Advanced AI Model", "Improve 'predictors.py' to use a more robust ANPR (Automatic Number Plate Recognition) model like EasyOCR or a custom-trained YOLO model.")
pdf.task_item("Dockerization", "Create a 'Dockerfile' and 'docker-compose.yml' to containerize the application for easy deployment.")
pdf.task_item("Security Enhancements", "Implement proper JWT (JSON Web Token) authentication and add rate limiting to API endpoints to prevent abuse.")
pdf.task_item("Unit Testing", "Write comprehensive unit tests using 'pytest' for all API endpoints to ensure reliability.")

# Android Tasks
pdf.section_title('3. Android App Development (Kotlin)')
pdf.task_item("Map Integration", "Implement Google Maps or Leaflet (via WebView) to display camera locations on the mobile app.")
pdf.task_item("Challan List & Detail View", "Create a RecyclerView to display the user's challan history fetched from the backend API.")
pdf.task_item("Push Notifications", "Fully implement Firebase Cloud Messaging (FCM) to handle and display push notifications for new challans.")
pdf.task_item("Profile Management", "Build native screens for viewing and updating user profile information.")
pdf.task_item("Authentication Flow", "Complete the Login and Registration screens with proper API integration and token management.")

pdf.output('Project_Task_Sheet.pdf', 'F')
print("PDF generated successfully: Project_Task_Sheet.pdf")
