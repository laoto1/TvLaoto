FROM python:3.11-slim

# System deps for Playwright Chromium
RUN apt-get update && apt-get install -y --no-install-recommends \
    libnss3 libx11-xcb1 libxcomposite1 libxcursor1 libxdamage1 \
    libxext6 libxi6 libxtst6 libcups2 libxss1 libxrandr2 \
    libasound2 libpangocairo-1.0-0 libatk1.0-0 libatk-bridge2.0-0 \
    libgtk-3-0 libgbm1 libdrm2 libxshmfence1 fonts-noto-cjk \
    curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Chromium for Playwright
RUN playwright install chromium && playwright install-deps chromium

COPY . .

# HuggingFace Spaces expects port 7860
EXPOSE 7860

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]

