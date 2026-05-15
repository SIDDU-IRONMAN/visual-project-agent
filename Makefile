.PHONY: install start stop clean health

# Installation
install:
	uv sync

# Start servers in the background
start:
	@echo "Starting backend on port 8000..."
	uv run uvicorn backend.api:app --host 0.0.0.0 --port 8000 &
	@echo "Starting frontend on port 5500..."
	python3 -m http.server 5500 --directory frontend &
	@echo "Servers are starting. Run 'make health' in a few seconds to verify."

# Stop servers
stop:
	@echo "Stopping servers on ports 8000 and 5500..."
	-lsof -t -i :8000 | xargs kill -9
	-lsof -t -i :5500 | xargs kill -9
	@echo "Servers stopped."

# Cleanup temporary files
clean:
	@echo "Cleaning temporary files and logs..."
	rm -rf temp_uploads/
	rm -f *.log
	rm -rf __pycache__ src/__pycache__ backend/__pycache__
	@echo "Cleanup complete."

# Run health checks
health:
	uv run scripts/health_check.py
