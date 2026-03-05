-PART 01 -

# KW Sustainability Data API

## Overview

The **KW Sustainability Data API is a backend service designed to automate the ingestion, extraction, and analysis of sustainability and ESG (Environmental, Social, and Governance) data from unstructured documents.

Organizations often publish sustainability reports in formats such as **PDFs or Excel spreadsheets**. Extracting structured ESG metrics from these documents manually is time-consuming and error-prone. This project demonstrates how a backend system can automate this workflow using **Large Language Models (LLMs)** to extract meaningful sustainability data and store it in a **relational database** for querying and analysis.

The system allows users to upload sustainability reports, automatically extracts ESG metrics such as **carbon emissions, energy consumption, water usage, and waste generation**, and stores them in a structured format. The extracted data can then be accessed through REST APIs and summarized through an insights endpoint.

This project was developed as part of the **KW Backend Engineering Take-Home Assignment**.

---

## Key Capabilities

* Upload sustainability reports in **PDF or Excel format**
* Automatically extract ESG metrics using an **LLM-based extraction pipeline**
* Store structured sustainability data in a **PostgreSQL relational database**
* Secure API access using **JWT authentication**
* Query and filter extracted sustainability records
* Generate high-level sustainability insights across uploaded reports

The goal of this system is to demonstrate how modern backend systems can combine **document processing, AI-based data extraction, and API-driven architectures** to transform unstructured sustainability reporting data into structured, queryable datasets.

------------------------PART 02 -----------------------------

## Problem Background

Companies increasingly publish sustainability and ESG (Environmental, Social, and Governance) reports to communicate their environmental impact and sustainability commitments. These reports often contain valuable metrics such as:

* Scope 1, Scope 2, and Scope 3 carbon emissions
* Energy consumption and renewable energy usage
* Water withdrawal and water consumption
* Waste generation and recycling rates
* Sustainability targets and commitments

However, these reports are typically distributed as **PDF documents or spreadsheets**, making the data difficult to aggregate, analyze, or compare across organizations.

Organizations that analyze sustainability data frequently face the following challenges:

1. **Unstructured data formats**
   Sustainability reports contain structured information embedded in long narrative documents, tables, and charts.

2. **Manual data extraction**
   Analysts often manually read reports and copy relevant metrics into spreadsheets or internal systems.

3. **Inconsistent reporting formats**
   Different companies report sustainability metrics using different terminology, formats, and units.

4. **Limited automation**
   Traditional data pipelines struggle to extract structured insights from unstructured documents.

Large Language Models (LLMs) provide a powerful solution to this problem by enabling systems to interpret and extract structured data from complex documents.

This project demonstrates how a backend system can use an LLM to:

* Parse sustainability reports
* Identify relevant ESG metrics
* Convert extracted values into structured database records
* Provide APIs to query and summarize the extracted data

The result is a system that transforms **unstructured sustainability reports into structured ESG datasets that can be queried programmatically.**

------------------------PART 03 ----------------------------


## System Architecture

The system follows a modular backend architecture designed to handle document ingestion, AI-powered extraction, and structured data storage.

The workflow of the system is shown below.

User → API → File Parser → LLM Extraction → Database → Query & Insights API

When a user uploads a sustainability report, the backend processes the document in multiple stages.

1. **Document Upload**

Users upload sustainability reports through the REST API. The system supports both PDF and Excel files. Uploaded files are stored temporarily while the extraction pipeline processes them.

2. **Document Parsing**

The backend parses the uploaded file and extracts raw text content.

For PDFs, the system extracts text from document pages.
For Excel files, the system reads spreadsheet data and converts it into textual format.

The goal of this stage is to convert the original file into a clean text representation that can be processed by the LLM.

3. **Text Chunking**

Large sustainability reports may contain hundreds of pages. To ensure reliable processing, the document text is divided into smaller chunks.

Each chunk is sent to the LLM individually to improve extraction accuracy and avoid token limits.

4. **LLM-Based Data Extraction**

The system uses a Large Language Model to analyze the document text and identify relevant sustainability metrics.

The LLM extracts structured information such as:

* Carbon emissions (Scope 1, Scope 2, Scope 3)
* Energy consumption metrics
* Water usage
* Waste generation
* Company name
* Reporting year

The extracted data is returned in structured JSON format.

5. **Database Storage**

The extracted metrics are stored in a relational PostgreSQL database. The schema is designed to separate different types of sustainability metrics into dedicated tables while linking them to the original document.

This structure enables efficient querying and future extensibility.

6. **API Query Layer**

The stored data can be accessed through multiple API endpoints:

* Document listing and filtering
* Document detail retrieval
* Aggregated sustainability insights

7. **Insights Generation**

The insights endpoint analyzes all stored records and generates a summary of sustainability metrics across uploaded reports.

This allows users to quickly understand trends such as total emissions reported or the number of companies analyzed.

This architecture separates responsibilities across components, making the system easier to maintain, extend, and scale.



------------------------PART 04 ---------------------------
## Features

The KW Sustainability Data API provides a set of backend capabilities designed to automate sustainability report processing and enable structured ESG data analysis.

### Document Upload and Processing

The API allows users to upload sustainability reports in **PDF or Excel format**. Once uploaded, the system automatically parses the document, extracts relevant sustainability information using a Large Language Model (LLM), and stores the extracted metrics in a structured database.

This automation significantly reduces the manual effort required to extract ESG data from large sustainability reports.

### ESG Metric Extraction

The system extracts several categories of sustainability metrics, including:

* **Carbon emissions**

  * Scope 1 emissions
  * Scope 2 emissions
  * Scope 3 emissions

* **Energy metrics**

  * Total energy consumption
  * Renewable energy usage

* **Water metrics**

  * Total water withdrawal
  * Water consumption

* **Waste metrics**

  * Total waste generated
  * Recycling rates

Additional contextual information such as **company name and reporting year** is also extracted from the document.

### Structured Data Storage

All extracted information is stored in a **relational database** designed specifically for sustainability reporting data. Each uploaded document is associated with multiple ESG metric records, enabling efficient querying and analysis.

### Authentication and Secure API Access

The API uses **JWT-based authentication** to secure endpoints. Users must register and authenticate before accessing protected routes such as document upload or analytics endpoints.

This ensures that each user's uploaded documents and extracted data remain securely associated with their account.

### Document Listing and Filtering

Users can retrieve previously uploaded sustainability reports through an API endpoint that supports:

* Pagination
* Filtering by company name
* Efficient record retrieval

This allows users to navigate large datasets of sustainability reports.

### Record Detail Retrieval

The API provides a detailed endpoint for retrieving the full information extracted from a specific document. This includes document metadata and all related ESG metrics.

### Sustainability Insights

An insights endpoint analyzes the data stored in the database and returns a **high-level natural language summary** of sustainability metrics across uploaded reports.

For example, the endpoint can summarize:

* Number of sustainability reports analyzed
* Companies represented in the dataset
* Total emissions reported
* Aggregated energy and environmental metrics

This feature demonstrates how structured sustainability data can be transformed into meaningful insights through backend analytics.

### API Documentation

The project includes **auto-generated Swagger documentation**, which allows developers to explore and test the API endpoints interactively through a browser interface.

This simplifies development, testing, and integration with external systems.



------------------------PART 05 ----------------------------
## Tech Stack

The KW Sustainability Data API is built using modern Python backend technologies and integrates document processing, database management, and AI-powered extraction.

### Backend Framework

**FastAPI**

The API is implemented using FastAPI, a high-performance Python web framework designed for building modern REST APIs. FastAPI provides automatic request validation, built-in dependency injection, and auto-generated API documentation through Swagger.

Key benefits of FastAPI include:

* High performance and asynchronous support
* Automatic OpenAPI documentation
* Built-in request validation using Pydantic
* Easy integration with modern Python tooling

### Programming Language

**Python**

Python was chosen because of its strong ecosystem for backend development, data processing, and AI integration. The language provides excellent libraries for document parsing, database access, and API development.

### Database

**PostgreSQL**

PostgreSQL is used as the relational database for storing extracted sustainability metrics. It provides strong support for structured data storage, indexing, and complex queries.

The schema is designed to store documents separately from sustainability metrics while maintaining relationships between them.

### Database ORM

**SQLAlchemy**

SQLAlchemy is used as the Object Relational Mapper (ORM) to interact with the database. It allows Python classes to represent database tables and simplifies database operations such as querying, inserting, and updating records.

### Database Migrations

**Alembic**

Alembic is used to manage database schema migrations. This allows the database structure to evolve over time while maintaining version control for schema changes.

### AI Extraction

**Groq LLM API**

A Large Language Model is used to extract structured sustainability metrics from unstructured documents. The system sends parsed document text to the LLM, which identifies relevant ESG metrics and returns them in structured JSON format.

### Document Processing

The project includes custom services for processing uploaded files.

For PDF documents, text is extracted from the document content.
For Excel files, spreadsheet data is parsed and converted into text suitable for LLM processing.

### Authentication

**JWT (JSON Web Tokens)**

JWT-based authentication is used to secure API endpoints. Users must authenticate using login credentials, and a signed token is issued to authorize future requests.

### API Documentation

FastAPI automatically generates interactive API documentation using **Swagger UI**. Developers can explore the API endpoints directly through a browser and test requests interactively.

The documentation is available at:

http://127.0.0.1:8000/docs

This enables easy testing of the API without requiring external tools.


------------------------PART 06 -----------------------------
## Project Structure

The project follows a modular backend structure that separates API routes, business logic, database models, and configuration. This separation improves readability, maintainability, and scalability.

The repository is organized as follows:

KW_Backend
│
├── alembic/
│   └── Database migration files
│
├── app/
│   ├── api/
│   │   ├── deps.py
│   │   └── v1/
│   │       ├── routes_auth.py
│   │       ├── routes_documents.py
│   │       └── routes_insights.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── passwords.py
│   │   └── security.py
│   │
│   ├── db/
│   │   ├── base.py
│   │   ├── session.py
│   │   └── init_db.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── document.py
│   │   ├── carbon.py
│   │   ├── energy.py
│   │   ├── water.py
│   │   └── waste.py
│   │
│   ├── schemas/
│   │   ├── auth.py
│   │   ├── document.py
│   │   ├── carbon.py
│   │   ├── energy.py
│   │   ├── water.py
│   │   └── waste.py
│   │
│   ├── services/
│   │   ├── file_parser.py
│   │   └── llm_extractor.py
│   │
│   └── main.py
│
├── sample_data/
│   ├── 2025-Microsoft-Environmental-Sustainability-Report.pdf
│   └── 2024-sustainability-report-data.xlsx
│
├── requirements.txt
├── alembic.ini
├── README.md

### Directory Overview

**app/api/**
Contains API route definitions. Each file defines a group of related endpoints.

**app/core/**
Contains configuration settings, password hashing utilities, and security-related logic.

**app/db/**
Handles database initialization and session management.

**app/models/**
Defines SQLAlchemy database models that represent tables in the PostgreSQL database.

**app/schemas/**
Defines Pydantic schemas used for request validation and response serialization.

**app/services/**
Contains the business logic for document parsing and LLM-based data extraction.

**sample_data/**
Includes example sustainability documents used for testing the extraction pipeline.

**alembic/**
Contains database migration scripts used to create and update database tables.

This modular structure ensures that API logic, data models, and AI extraction processes remain cleanly separated.



------------------------PART 07 -----------------------------
## Installation and Setup

The following steps describe how to run the KW Sustainability Data API locally.

### 1. Clone the Repository

Clone the project repository from GitHub.

git clone https://github.com/your-username/KW_Backend.git

Navigate into the project directory.

cd KW_Backend

### 2. Create a Virtual Environment

Create a Python virtual environment to isolate project dependencies.

python3 -m venv venv

### 3. Activate the Virtual Environment

Linux or macOS

source venv/bin/activate

Windows

venv\Scripts\activate

### 4. Install Dependencies

Install the required Python packages using pip.

pip install -r requirements.txt

### 5. Configure Environment Variables

Create a `.env` file in the project root directory and add the following configuration.

POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_DB=kw_sustainability

GROQ_API_KEY=your_groq_api_key

SECRET_KEY=super-secret-key

### 6. Start PostgreSQL

Ensure PostgreSQL is installed and running locally.

Start the PostgreSQL service.

sudo service postgresql start

### 7. Create the Database

Open the PostgreSQL console.

sudo -u postgres psql

Create the database used by the application.

CREATE DATABASE kw_sustainability;

Exit the console.

\q

### 8. Run Database Migrations

Apply database migrations using Alembic.

alembic upgrade head

This will create all required database tables.

### 9. Start the API Server

Run the FastAPI application using Uvicorn.

uvicorn app.main:app --reload

The API will start at:

http://127.0.0.1:8000

### 10. Open API Documentation

FastAPI automatically generates interactive API documentation using Swagger UI.

Open the following URL in your browser.

http://127.0.0.1:8000/docs

You can test all API endpoints directly from this interface.

### 11. Test the System

Typical workflow for testing the API:

1. Register a user account
2. Login to obtain a JWT token
3. Authorize requests using the token
4. Upload a sustainability report
5. Query stored documents and ESG insights

Sample documents are available in the `sample_data` directory for testing the extraction pipeline.


------------------------PART 08 -----------------------------
## API Endpoints

The KW Sustainability Data API exposes a set of REST endpoints for authentication, document ingestion, querying stored records, and generating sustainability insights.

All protected endpoints require **JWT authentication** using the `Authorization` header.

Authorization: Bearer <access_token>

### Authentication

These endpoints allow users to register and log in to the system.

#### Register User

POST /api/v1/register

Creates a new user account.

Example request body:

{
"email": "[user@example.com](mailto:user@example.com)",
"password": "SecurePassword123"
}

Successful response:

{
"access_token": "jwt_token",
"token_type": "bearer"
}

#### Login User

POST /api/v1/login

Authenticates an existing user and returns a JWT token.

Example request body:

{
"email": "[user@example.com](mailto:user@example.com)",
"password": "SecurePassword123"
}

Response:

{
"access_token": "jwt_token",
"token_type": "bearer",
"user": {
"id": 1,
"email": "[user@example.com](mailto:user@example.com)"
}
}

### Document Upload

#### Upload Sustainability Document

POST /api/v1/upload

Uploads a sustainability report and extracts ESG metrics using the LLM.

Request type: multipart/form-data

Parameters:

file – sustainability report file (PDF or Excel)

Example response:

{
"id": 1,
"filename": "2025-sustainability-report.pdf",
"company_name": "Example Corp",
"reporting_year": 2025,
"status": "processed"
}

### Document Query Endpoints

#### List Documents

GET /api/v1/documents

Returns a paginated list of uploaded documents.

Query parameters:

skip – number of records to skip
limit – maximum number of records to return
company_name – optional filter by company

Example request:

GET /api/v1/documents?skip=0&limit=10

Example response:

{
"total": 5,
"page": 1,
"page_size": 10,
"has_next": false,
"data": [...]
}

#### Get Document Detail

GET /api/v1/documents/{document_id}

Returns full details of a specific uploaded document and its extracted ESG metrics.

Example request:

GET /api/v1/documents/1

### Sustainability Insights

#### Get Insights

GET /api/v1/insights

Generates a high-level summary of sustainability data across all uploaded reports.

Example response:

{
"total_documents": 10,
"unique_companies": 3,
"reporting_years": [2024, 2025],
"emissions": {
"scope1_total": 92,
"scope2_total": 84,
"scope3_total": 149000
},
"energy": {
"avg_renewable_energy_pct": null
},
"summary": "10 sustainability reports were analyzed across 3 companies."
}

### Root Endpoint

GET /

Returns a simple status message indicating the API is running.

Response:

{
"message": "KW Sustainability API",
"status": "running"
}


------------------------PART 09 -----------------------------
## LLM Extraction Strategy

Sustainability reports often contain important ESG metrics embedded in large narrative documents, tables, and charts. Extracting these values manually can be time-consuming and inconsistent. This project uses a **Large Language Model (LLM)** to automate the extraction of sustainability metrics from unstructured documents.

### Document Processing Pipeline

When a sustainability report is uploaded, the system processes it through several stages.

**1. File Parsing**

The uploaded document is first parsed to extract raw text.

* PDF files are processed using a PDF parsing library that extracts text from document pages.
* Excel files are processed using a spreadsheet parser that converts table data into textual format.

This step converts the document into a plain text representation that can be analyzed by the LLM.

**2. Text Chunking**

Sustainability reports can be very large. To ensure the LLM processes the document effectively and avoids token limits, the extracted text is divided into smaller chunks.

Each chunk contains a portion of the document text and is processed independently by the LLM.

**3. LLM-Based Information Extraction**

Each text chunk is sent to the LLM along with a structured prompt that instructs the model to identify sustainability metrics.

The prompt asks the model to extract information such as:

* Company name
* Reporting year
* Scope 1 carbon emissions
* Scope 2 carbon emissions
* Scope 3 carbon emissions
* Energy consumption metrics
* Renewable energy usage
* Water withdrawal or consumption
* Waste generation

The LLM returns the extracted information in a **structured JSON format**, which simplifies further processing.

**4. Metric Aggregation**

Because each document is processed in multiple chunks, the extracted results are aggregated to build a complete set of metrics for the document.

If the same metric appears in multiple chunks, the system selects the most relevant value.

**5. Data Normalization**

Extracted values are normalized before being stored in the database. This includes:

* Converting values to consistent numeric formats
* Storing measurement units
* Associating each metric with the source document

**6. Database Storage**

The structured data is then stored in relational tables that represent different categories of sustainability metrics.

This allows the extracted ESG data to be queried efficiently using the API.

### Advantages of Using an LLM

Using a Large Language Model provides several advantages compared to traditional rule-based extraction systems.

* Ability to understand context within complex documents
* Flexible handling of different report formats
* Robust extraction from both narrative text and tabular data
* Reduced need for manual data labeling or rigid parsing rules

This approach demonstrates how AI-powered document processing can significantly improve the automation of sustainability data extraction workflows.



------------------------PART 10 ----------------------------
## Design Decisions and Future Improvements

### Design Decisions

Several design choices were made to ensure the system remains maintainable, scalable, and aligned with the requirements of the assignment.

**Modular Backend Architecture**

The project follows a modular architecture where responsibilities are separated into dedicated components:

* API routes handle request and response logic
* Services implement business logic such as file parsing and LLM extraction
* Database models define relational data structures
* Schemas handle request validation and response serialization

This separation improves code readability and allows individual components to evolve independently.

**Relational Database Schema**

A relational schema was chosen to represent sustainability metrics because ESG data contains clear relationships between documents and extracted metrics.

Each uploaded document is stored in the `documents` table and related ESG metrics are stored in separate tables:

* carbon_metrics
* energy_metrics
* water_metrics
* waste_metrics

This normalization ensures efficient querying and prevents data duplication.

**Chunk-Based LLM Processing**

Large sustainability reports often exceed the token limits of LLMs. To address this, the document text is divided into smaller chunks before being sent to the LLM.

Chunking improves extraction reliability and ensures that large reports can still be processed effectively.

**JWT-Based Authentication**

JWT authentication was implemented to secure API endpoints. This approach ensures that each user’s uploaded documents remain associated with their account while allowing stateless API authentication.

**Graceful Handling of Missing Data**

Not all sustainability reports contain the same metrics. The system is designed to handle missing values gracefully by storing available metrics without requiring every ESG field to be present.

This makes the system robust to variations in sustainability reporting formats.

### AI Tools Used

This project was developed with assistance from AI-based development tools for:

* generating code suggestions
* structuring backend components
* refining documentation
* assisting with debugging

All design decisions, architecture choices, and final code integration were reviewed and implemented by the developer.

### Future Improvements

Although the system satisfies the assignment requirements, several enhancements could further improve the platform.

**Improved Metric Standardization**

Future versions could include automatic unit normalization and ESG taxonomy mapping to standard frameworks such as GRI or SASB.

**Advanced Document Parsing**

Some sustainability reports contain charts and scanned pages. Integrating OCR capabilities would allow the system to extract information from image-based documents.

**Improved Insights Engine**

The insights endpoint could be extended to provide more advanced analytics, including trends across reporting years, sustainability benchmarking across companies, and ESG performance comparisons.

**Asynchronous Processing**

Document processing could be moved to a background task queue using tools such as Celery or Redis to support large-scale ingestion workloads.

**Vector Search for Sustainability Reports**

Embedding sustainability report content into a vector database would enable semantic search capabilities, allowing users to query sustainability reports using natural language.

### Conclusion

This project demonstrates how a modern backend system can combine **document processing, AI-based extraction, and relational data modeling** to transform unstructured sustainability reports into structured ESG datasets.

By automating the extraction of sustainability metrics and exposing them through a REST API, the system provides a foundation for building scalable ESG analytics platforms.

