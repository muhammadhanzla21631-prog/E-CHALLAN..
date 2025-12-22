from fpdf import FPDF
from datetime import datetime

class PDF(FPDF):
    def header(self):
        # Logo
        # self.image('logo.png', 10, 8, 33)
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Move to the right
        self.cell(80)
        # Title
        self.cell(30, 10, 'E-Challan System Project Report', 0, 0, 'C')
        # Line break
        self.ln(20)

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

    def chapter_title(self, num, label):
        # Arial 12
        self.set_font('Arial', '', 12)
        # Background color
        self.set_fill_color(200, 220, 255)
        # Title
        self.cell(0, 6, 'Section %d : %s' % (num, label), 0, 1, 'L', 1)
        # Line break
        self.ln(4)

    def chapter_body(self, body):
        # Times 12
        self.set_font('Times', '', 12)
        # Output justified text
        self.multi_cell(0, 10, body)
        # Line break
        self.ln()

pdf = PDF()
pdf.alias_nb_pages()
pdf.add_page()

# Title Page
pdf.set_font('Arial', 'B', 24)
pdf.cell(0, 40, 'E-Challan System', 0, 1, 'C')
pdf.set_font('Arial', '', 16)
pdf.cell(0, 10, 'Comprehensive Project Report', 0, 1, 'C')
pdf.cell(0, 10, f'Generated on: {datetime.now().strftime("%Y-%m-%d")}', 0, 1, 'C')
pdf.ln(20)

# Section 1: Introduction
pdf.chapter_title(1, 'Project Overview')
pdf.chapter_body(
    "The E-Challan System is a comprehensive solution designed to automate traffic violation detection, "
    "management, and penalty enforcement. It leverages modern web technologies and machine learning to "
    "create a robust infrastructure for traffic monitoring.\n\n"
    "The system consists of a high-performance FastAPI backend and a responsive, interactive frontend "
    "built with HTML, CSS, and JavaScript."
)

# Section 2: Backend Architecture
pdf.chapter_title(2, 'Backend Architecture')
pdf.chapter_body(
    "Technology Stack: Python, FastAPI, SQLModel (SQLite), TensorFlow Lite.\n\n"
    "Key Features:\n"
    "- RESTful API Design: Structured endpoints for scalability.\n"
    "- Database Management: SQLite database handling Cameras, Users, Challans, Payments, and Appeals.\n"
    "- Machine Learning Integration: TFLite model integration for processing vehicle images and detecting violations (e.g., no helmet, speeding).\n"
    "- Notification System: Multi-channel alerts using FCM (Push), Email, and WhatsApp.\n"
    "- Analytics Engine: Dedicated endpoints for aggregating violation stats, revenue data, and camera health metrics."
)

# Section 3: Frontend Features
pdf.chapter_title(3, 'Frontend Features')
pdf.chapter_body(
    "Technology Stack: HTML5, CSS3, JavaScript (ES6+), Leaflet.js, Chart.js.\n\n"
    "Key Features:\n"
    "- Interactive Map: Real-time visualization of camera locations with status indicators (Active/Inactive).\n"
    "- Dashboard: Live statistics showing total violations, revenue generated, and system health.\n"
    "- Voice Alerts: Integrated text-to-speech engine for audible notifications of system events.\n"
    "- Vehicle Lookup: Public portal for users to check violation history by vehicle number.\n"
    "- Evidence Upload: Interface for uploading images to test the violation detection model.\n"
    "- Dark/Light Mode: User-customizable interface theme.\n"
    "- Routing: Integrated navigation to find directions to specific camera locations."
)

# Section 4: Database Schema
pdf.chapter_title(4, 'Database Schema')
pdf.chapter_body(
    "The system uses a relational database with the following core entities:\n\n"
    "1. Camera: Stores location (lat/lng), address, status, and health score.\n"
    "2. User: Manages authentication, roles (admin/user), and contact info.\n"
    "3. Challan: Records violation details, vehicle info, amount, and payment status.\n"
    "4. Payment: Tracks payment transactions and methods.\n"
    "5. Appeal: Manages user disputes against issued challans."
)

# Section 5: Recent Updates
pdf.chapter_title(5, 'Recent Updates & Achievements')
pdf.chapter_body(
    "- Implemented Voice Alert system for real-time auditory feedback.\n"
    "- Added comprehensive Analytics Dashboard with visual charts.\n"
    "- Integrated Payment and Appeals processing workflows.\n"
    "- Enhanced Map interface with routing and clustering capabilities.\n"
    "- Finalized User Authentication and Profile management."
)

pdf.output('/home/hanzla/e--challan./Project_Report.pdf', 'F')
print("PDF generated successfully.")
