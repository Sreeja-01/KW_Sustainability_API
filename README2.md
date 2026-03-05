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

### Outputs

![0](https://github.com/user-attachments/assets/2ecbcd5a-61df-41bf-bedc-8b36c328ddd7)
![1](https://github.com/user-attachments/assets/9aab3a8d-6c2f-44eb-90a0-78acc5cad56e)
![2](https://github.com/user-attachments/assets/f6bd38e9-af70-4d35-b17c-76abfe89ee39)
![3](https://github.com/user-attachments/assets/62802885-b6f8-4f6c-85e0-25ce7e12d7ad)
![4](https://github.com/user-attachments/assets/90d6ee85-271b-4acf-91bb-47f1ec5976fa)
![5](https://github.com/user-attachments/assets/66854ef8-4d18-41a8-9f66-47880efef67b)
![6](https://github.com/user-attachments/assets/73ca13c8-2b2f-472b-b840-fffbf0911aae)
![7](https://github.com/user-attachments/assets/c329b1e6-12bc-4912-902b-c239f3f874f0)
![8](https://github.com/user-attachments/assets/b0f17991-a9c0-4fe9-9e14-0162e16ddc54)
![9](https://github.com/user-attachments/assets/d57f8c44-fd0a-41b2-af96-6fac07a9f29e)
![10](https://github.com/user-attachments/assets/bbe22aa4-e7c3-4cd7-b8df-9fc7f7f08af1)
![11](https://github.com/user-attachments/assets/d2e8d2dc-aea1-499c-9250-32fc83ea00cd)
![12](https://github.com/user-attachments/assets/827bfd80-6f1b-4c73-a6ad-e30bb60d8726)
![13](https://github.com/user-attachments/assets/f87e4adc-d0a3-4cf1-be72-4f21d767e639)
![14](https://github.com/user-attachments/assets/18b4238c-29e8-46f1-af2e-e3f44032e71f)
![15](https://github.com/user-attachments/assets/fee1a205-6fee-49fa-9926-57926cd8dcaf)
![16](https://github.com/user-attachments/assets/e716afa8-658c-4bdc-b44e-f56c04ce6427)
