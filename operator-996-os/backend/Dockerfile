# ============================================================
# 🧠 Operator-996 Cognitive OS - Backend Dockerfile
# ============================================================

FROM python:3.11-slim
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source code
COPY . .

# Expose API port
EXPOSE 8000

# Run the FastAPI server
CMD ["uvicorn", "backend_main:app", "--host", "0.0.0.0", "--port", "8000"]
