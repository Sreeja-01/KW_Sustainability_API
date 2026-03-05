### KW Sustainability Data API
A FastAPI backend that automates ESG data extraction from sustainability reports (PDF/Excel) using LLMs, stores metrics in PostgreSQL, and provides REST APIs with JWT auth.

### Quick Installation & Setup (UBUNTU)
Clone & Setup Environment

```
git clone https://github.com/Sreeja-01/KW_Sustainability_API.git
cd KW_Sustainability_API
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows
pip install -r requirements.txt
```
### Configure Environment
```
Create .env file:

POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_DB=kw_sustainability
GROQ_API_KEY=your_groq_api_key
SECRET_KEY=super-secret-key
```
### Database Setup
```
# Start PostgreSQL
sudo service postgresql start

# Create DB
sudo -u postgres psql
CREATE DATABASE kw_sustainability;
\q

# Run migrations
alembic upgrade head
```
### Run the App
```
uvicorn app.main:app --reload
```
Open: http://127.0.0.1:8000/docs

### Testing Workflow
- Register/Login → Get JWT token

- Upload PDF/Excel from sample_data/

- Query documents → Check insights

### Key Design Decisions
- FastAPI + Pydantic: Auto-validation, Swagger docs, async performance

- Modular Structure: API routes → Services → Models → Schemas (clean separation)

- PostgreSQL + Normalized Schema: Documents → Carbon/Energy/Water/Waste metrics (efficient querying)

- Chunk-based LLM Processing: Handles large reports, avoids token limits

- JWT Auth: Stateless, user-isolated data

- Groq LLM: Fast, cost-effective extraction from unstructured docs

### Architecture: 
Upload → Parse → Chunk → LLM Extract → Store → Query/Insights API

