#!/bin/bash

# ===========================================
# ContentForge - Local Development Script
# ===========================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "  ____            _             _   _____                    "
echo " / ___|___  _ __ | |_ ___ _ __ | |_|  ___|__  _ __ __ _  ___ "
echo "| |   / _ \| '_ \| __/ _ \ '_ \| __| |_ / _ \| '__/ _\` |/ _ \\"
echo "| |__| (_) | | | | ||  __/ | | | |_|  _| (_) | | | (_| |  __/"
echo " \____\___/|_| |_|\__\___|_| |_|\__|_|  \___/|_|  \__, |\___|"
echo "                                                  |___/      "
echo -e "${NC}"
echo ""

# Check .env file
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  .env dosyası bulunamadı. .env.example'dan oluşturuluyor...${NC}"
    cp .env.example .env
    echo -e "${RED}❌ Lütfen .env dosyasını düzenleyip API key'leri ekleyin!${NC}"
    exit 1
fi

# Export environment variables
export $(cat .env | grep -v '^#' | xargs)

# Function to cleanup
cleanup() {
    echo -e "\n${YELLOW}🛑 Servisler durduruluyor...${NC}"
    kill $BACKEND_PID 2>/dev/null || true
    kill $FRONTEND_PID 2>/dev/null || true
    exit 0
}

trap cleanup SIGINT SIGTERM

# Start Backend
echo -e "${GREEN}🚀 Backend başlatılıyor...${NC}"
cd backend

if [ ! -d "venv" ]; then
    echo -e "${YELLOW}📦 Virtual environment oluşturuluyor...${NC}"
    python3 -m venv venv
fi

source venv/bin/activate
pip install -q -r requirements.txt

python run_api.py &
BACKEND_PID=$!
cd ..

sleep 3

# Start Frontend
echo -e "${GREEN}🚀 Frontend başlatılıyor...${NC}"
cd frontend

if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}📦 Node modülleri yükleniyor...${NC}"
    npm install
fi

npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo -e "${GREEN}✅ ContentForge başlatıldı!${NC}"
echo ""
echo -e "   ${BLUE}Frontend:${NC} http://localhost:3000"
echo -e "   ${BLUE}Backend:${NC}  http://localhost:8000"
echo -e "   ${BLUE}API Docs:${NC} http://localhost:8000/docs"
echo ""
echo -e "${YELLOW}Durdurmak için Ctrl+C${NC}"
echo ""

# Wait for processes
wait
