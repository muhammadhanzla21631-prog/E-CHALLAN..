from fpdf import FPDF
from datetime import datetime

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'E-Challan System - Test Script & QA Plan', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

    def section_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(240, 240, 240)
        self.cell(0, 8, title, 0, 1, 'L', 1)
        self.ln(2)

    def test_case(self, id, title, steps, expected_result):
        self.set_font('Arial', 'B', 10)
        self.cell(0, 6, f"Test Case {id}: {title}", 0, 1)
        
        self.set_font('Arial', '', 10)
        self.multi_cell(0, 5, f"Steps:\n{steps}")
        
        self.set_font('Arial', 'I', 10)
        self.multi_cell(0, 5, f"Expected Result: {expected_result}")
        self.ln(4)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

def create_test_script_pdf():
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    
    # Meta Info
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 5, f"Date: {datetime.now().strftime('%Y-%m-%d')}", 0, 1, 'R')
    pdf.cell(0, 5, "Version: 1.0", 0, 1, 'R')
    pdf.ln(5)

    # 1. Automated Testing
    pdf.section_title("1. Automated API Testing")
    pdf.set_font('Arial', '', 10)
    pdf.multi_cell(0, 5, 
        "We have developed an automated Python script to verify the health and functionality of the Backend API.\n\n"
        "Command to Run:\n"
        "  python backend/test_api.py\n\n"
        "Scope:\n"
        "- Server Connectivity Check\n"
        "- Camera List Retrieval (/api/cameras)\n"
        "- Analytics Dashboard Data (/api/analytics/dashboard)\n"
        "- AI Prediction Endpoint (/predict) with dummy image"
    )
    pdf.ln(5)

    # 2. Manual Testing - Frontend
    pdf.section_title("2. Manual Testing - Web Interface")
    
    pdf.test_case(
        "TC-001", 
        "Map Visualization", 
        "1. Open 'frontend/demo.html' in a browser.\n2. Wait for the map to load.",
        "Map should display centered on Lahore with Green (Active) and Red (Inactive) camera markers."
    )
    
    pdf.test_case(
        "TC-002", 
        "Camera Details", 
        "1. Click on any Green camera marker.\n2. Observe the popup.",
        "A popup should appear showing Camera Location, Status, Traffic Light status, and a 'Get Directions' button."
    )
    
    pdf.test_case(
        "TC-003", 
        "Real-time Notifications", 
        "1. Wait for 15-30 seconds on the dashboard.\n2. Observe the top-right corner.",
        "Toast notifications (e.g., 'Over Speed Detected') should appear automatically, simulating real-time alerts."
    )
    
    pdf.test_case(
        "TC-004", 
        "Dark Mode Toggle", 
        "1. Click the 'Dark Mode' button in the top navigation bar.",
        "The interface should switch to a dark theme, and the map tiles should invert colors to match the theme."
    )

    # 3. Manual Testing - Backend
    pdf.section_title("3. Manual Testing - Backend API")
    
    pdf.test_case(
        "TC-005", 
        "API Documentation Access", 
        "1. Ensure backend is running.\n2. Navigate to 'http://localhost:8000/docs'.",
        "Swagger UI should load, listing all available API endpoints (GET, POST, PUT, DELETE)."
    )
    
    pdf.test_case(
        "TC-006", 
        "Challan History API", 
        "1. Send a GET request to '/api/challans'.",
        "Server should return a JSON list of challan objects with status, amount, and vehicle details."
    )

    output_path = "Project_Test_Script.pdf"
    pdf.output(output_path, 'F')
    print(f"Test Script PDF generated: {output_path}")

if __name__ == "__main__":
    create_test_script_pdf()
