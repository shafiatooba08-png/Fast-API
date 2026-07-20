FROM python:3.12-slim

WORKDIR /app

# Install dependencies first (Docker cache optimization)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create non-root user
RUN useradd -m appuser

# Give ownership
RUN chown -R appuser:appuser /app

# Run application as non-root
USER appuser

EXPOSE 8000

CMD ["gunicorn", "app.main:app", "-k", "uvicorn.workers.UvicornWorker", "--workers", "4", "--bind", "0.0.0.0:8000"]