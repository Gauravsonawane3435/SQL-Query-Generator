# ⚡ SQLGen - AI-Powered SQL Query Generator

**SQLGen** is a modern, high-performance web application that transforms natural language descriptions into optimized, secure, and production-ready SQL queries. Powered by Google's Gemini 1.5 Flash AI, it supports multiple SQL dialects and provides instant explanations for the generated code.

![SQLGen Preview](https://via.placeholder.com/800x450?text=SQLGen+Project+Banner)

---

## 🚀 Key Features

- **Natural Language to SQL:** Write what you want in plain English, and get the code instantly.
- **Multiple Dialects:** Supports MySQL, PostgreSQL, SQLite, SQL Server, and Oracle.
- **AI-Powered Explanations:** Every query comes with a breakdown of how it works.
- **Syntax Highlighting:** Beautiful code presentation using Prism.js.
- **One-Click Copy:** Quickly copy the generated SQL to your clipboard.
- **Responsive Design:** Premium UI that works perfectly on desktop and mobile.

---

## 🛠️ Technology Stack

### **Frontend**
- **HTML5 & Vanilla CSS3:** For a lightweight, fast, and custom-styled user interface.
- **Modern Typography:** Uses *Inter* for UI and *JetBrains Mono* for code.
- **Vanilla JavaScript (ES6+):** Handles UI logic, state management, and API communication.
- **Prism.js:** Provides professional-grade syntax highlighting for SQL.

### **Backend**
- **FastAPI:** A modern, high-performance Python web framework for building APIs.
- **Uvicorn:** ASGI server for serving the application with extreme speed.
- **Python-dotenv:** Secure management of environment variables and API keys.

### **AI Engine**
- **Google Gemini 1.5 Flash:** Used for intelligent query generation and logical explanation.
- **Google Generative AI SDK:** Seamless integration with Google's latest LLM models.

---

## 🔄 Project Workflow

The application follows a streamlined Request-Response architecture:

1.  **User Input:** The user enters a natural language prompt (e.g., *"Show me users with more than 5 orders"*) and selects their preferred SQL dialect.
2.  **API Gateway:** The frontend sends an asynchronous POST request to the FastAPI `/generate` endpoint.
3.  **Prompt Engineering:** The backend constructs a structured system prompt that instructs the Gemini model to return a precise JSON response containing both the `sql` and `explanation`.
4.  **AI Inference:** Gemini processes the request, ensuring the SQL follows the specific syntax rules of the selected dialect.
5.  **Data Parsing:** The backend validates and parses the AI's response, handling any formatting anomalies to ensure clean data.
6.  **UI Feedback:** The frontend receives the response, triggers the Prism.js highlighter, and displays the result with a smooth animation.

---

## 💻 Installation & Setup

### **Prerequisites**
- Python 3.9+
- A Google Gemini API Key ([Get it here](https://aistudio.google.com/app/apikey))

### **Steps**

1.  **Clone the Repository:**
    ```bash
    git clone <your-repo-link>
    cd sql-query-generator
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment Variables:**
    Create a `.env` file in the root directory and add your API key:
    ```env
    GOOGLE_API_KEY=your_gemini_api_key_here
    ```

4.  **Run the Application:**
    ```bash
    python main.py
    ```

5.  **Access the Dashboard:**
    Open your browser and navigate to `http://localhost:8000`

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

---

Made with ❤️ by https://github.com/Gauravsonawane3435/SQL-Query-Generator.git
