from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'E-Challan Project Report', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

    def chapter_title(self, num, label):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 6, f'{num} : {label}', 0, 1, 'L', 1)
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 5, body)
        self.ln()

pdf = PDF()
pdf.alias_nb_pages()
pdf.add_page()

# 1. Project Overview
pdf.chapter_title('1. Project Overview', 'Project Introduction')
pdf.chapter_body(
    "Yeh project aik 'Smart E-Challan System' hai jo traffic violations ko detect karne, "
    "challan issue karne, aur users ko manage karne ke liye banaya gaya hai. "
    "Ismein FastAPI backend aur HTML/JS frontend use kiya gaya hai."
)

# 2. Current Features
pdf.chapter_title('2. Maujooda Features (Current Features)', 'Backend & Frontend')
pdf.chapter_body(
    "Backend (FastAPI):\n"
    "- User Management: User Profile dekhna aur update karna (Name, Phone, CNIC).\n"
    "- Challan System: Naya Challan issue karna, Challan History dekhna.\n"
    "- Payment System: Challan pay karne ki sahulat (Mock integration).\n"
    "- Appeals System: Ghalat challan ke khilaf appeal submit karna.\n"
    "- Analytics Dashboard: Total Revenue, Violations, aur Camera Health.\n"
    "- Search & Export: Universal Search, CSV Export.\n\n"
    "Frontend (HTML/JS):\n"
    "- Utility Functions: 40+ functions jo API se baat karte hain.\n"
    "- Validation: Pakistani formats (CNIC, Phone) ke mutabiq validation.\n"
    "- UI Components: Toast Notifications, Loading spinners.\n"
    "- Demo Page: Interactive page jahan saary features test kiye ja sakte hain."
)

# 3. Future Features
pdf.chapter_title('3. Jo Abhi Daalny Hain (Future Features)', 'To-Do List')
pdf.chapter_body(
    "Project ko mazeed professional aur complete banane ke liye yeh cheezein abhi daalni chahiye:\n"
    "1. Real Payment Gateway Integration (Stripe/JazzCash).\n"
    "2. Live Camera Feed (RTSP Stream).\n"
    "3. Admin Panel UI (Separate Dashboard).\n"
    "4. SMS/Email Alerts.\n"
    "5. Android App Integration.\n"
    "6. AI Model Improvement (ANPR).\n"
    "7. Deployment (Docker)."
)

# 4. Expected Usage
pdf.chapter_title('4. Expected Usage (Istemal Ka Tareeqa)', 'How to Run')
pdf.chapter_body(
    "Step 1: Backend Chalana\n"
    "Terminal mein: 'cd backend' phir 'python main.py'\n"
    "Is se server http://localhost:8000 par start ho jaye ga.\n\n"
    "Step 2: Frontend Test Karna\n"
    "Browser mein 'frontend/demo.html' file kholain.\n"
    "- Login karein\n"
    "- Search karein\n"
    "- Pay Challan karein\n"
    "- Appeal submit karein"
)

pdf.output('E_Challan_Report.pdf', 'F')
print("PDF generated successfully: E_Challan_Report.pdf")
