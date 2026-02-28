# ── Stage 1: Builder ──────────────────────────────────────────────────────────
FROM python:3.9-slim AS builder

WORKDIR /build

# Install dependencies in a separate layer (better cache usage)
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# ── Stage 2: Production image ─────────────────────────────────────────────────
FROM python:3.9-slim AS production

# Security: run as non-root user
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

WORKDIR /app

# Copy only the installed packages from builder
COPY --from=builder /root/.local /home/appuser/.local

# Copy application source
COPY app/ .

# Ensure scripts in .local are usable
ENV PATH=/home/appuser/.local/bin:$PATH

USER appuser

EXPOSE 8000

# Graceful shutdown support with --timeout-graceful-shutdown
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", \
     "--workers", "2", "--timeout-graceful-shutdown", "30"]
