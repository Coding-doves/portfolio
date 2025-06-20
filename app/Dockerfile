# Create the base environment
FROM python:3.12-slim

# Set up working directory  naming it app
WORKDIR /app

# Copy dependency list from requirements.txt file to the working directory
COPY requirements.txt .
COPY entrypoint.sh .

# Install dependency in working directory
RUN pip install --no-cache-dir -r requirements.txt

# Copy all code/project from folder into the working directory
COPY . .
RUN chmod +x /app/entrypoint.sh
# Set entrypoint
ENTRYPOINT ["./entrypoint.sh"]

# Expose the port on which the app will run
EXPOSE 8093

# Entrypoint.sh script for db tables set-up using alembic 
CMD ["/app/entrypoint.sh"]
