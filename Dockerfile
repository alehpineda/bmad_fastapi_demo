# Stage 1: Build stage
FROM python:3.13-slim as builder

# Install uv
RUN pip install uv

# Create and set the working directory
WORKDIR /app

# Copy only the dependency configuration files
COPY pyproject.toml ./

# Install dependencies using uv
RUN uv pip install --system --no-cache --requirement pyproject.toml

# Stage 2: Final stage
FROM python:3.13-slim

# Create a non-root user
RUN useradd --create-home appuser
WORKDIR /home/appuser

# Copy installed packages from the builder stage
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy the application source code
COPY ./app ./app

# Change ownership of the files and switch to the non-root user
RUN chown -R appuser:appuser /home/appuser
USER appuser

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
