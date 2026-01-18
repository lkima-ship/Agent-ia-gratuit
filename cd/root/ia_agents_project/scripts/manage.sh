cat > /root/ai_agents_project/scripts/manage.sh << 'EOF'
#!/bin/bash

# Script de gestion du système d'agents IA

set -e

PROJECT_DIR="/root/ai_agents_project"
VENV_DIR="$PROJECT_DIR/venv"
SRC_DIR="$PROJECT_DIR/src"

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_environment() {
    log_info "Checking environment..."
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        log_error "Python3 is not installed"
        return 1
    fi
    
    # Check pip
    if ! command -v pip3 &> /dev/null; then
        log_error "pip3 is not installed"
        return 1
    fi
    
    # Check project structure
    if [ ! -d "$PROJECT_DIR" ]; then
        log_error "Project directory not found: $PROJECT_DIR"
        return 1
    fi
    
    log_success "Environment check passed"
    return 0
}

install_dependencies() {
    log_info "Installing dependencies..."
    
    cd "$PROJECT_DIR"
    
    # Create virtual environment if not exists
    if [ ! -d "$VENV_DIR" ]; then
        log_info "Creating virtual environment..."
        python3 -m venv "$VENV_DIR"
    fi
    
    # Activate virtual environment
    source "$VENV_DIR/bin/activate"
    
    # Install requirements
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
    else
        # Install basic dependencies
        pip install flask flask-cors
    fi
    
    log_success "Dependencies installed"
}

start_api() {
    log_info "Starting API server..."
    
    cd "$PROJECT_DIR"
    
    # Check if API is already running
    if pgrep -f "python.*main\.py" > /dev/null; then
        log_warning "API is already running"
        return 0
    fi
    
    # Activate virtual environment
    if [ -d "$VENV_DIR" ]; then
        source "$VENV_DIR/bin/activate"
    fi
    
    # Start the API
    cd "$SRC_DIR"
    python3 main.py > "$PROJECT_DIR/api.log" 2>&1 &
    API_PID=$!
    
    # Wait and check
    sleep 3
    if pgrep -f "python.*main\.py" > /dev/null; then
        log_success "API started successfully (PID: $API_PID)"
        log_info "Logs: $PROJECT_DIR/api.log"
        log_info "URL: http://localhost:5002"
    else
        log_error "Failed to start API"
        tail -20 "$PROJECT_DIR/api.log"
        return 1
    fi
}

stop_api() {
    log_info "Stopping API server..."
    
    pkill -f "python.*main\.py" 2>/dev/null && \
        log_success "API stopped" || \
        log_warning "No API process found"
}

status_api() {
    log_info "Checking API status..."
    
    if pgrep -f "python.*main\.py" > /dev/null; then
        log_success "API is RUNNING"
        
        # Test the API
        if curl -s http://localhost:5002/api/status > /dev/null; then
            log_success "API is responding"
            echo ""
            curl -s http://localhost:5002/api/status | python3 -m json.tool
        else
            log_warning "API is not responding on port 5002"
        fi
    else
        log_warning "API is NOT running"
    fi
}

backup_project() {
    log_info "Creating backup..."
    
    BACKUP_FILE="/tmp/ai_agents_backup_$(date +%Y%m%d_%H%M%S).tar.gz"
    
    cd "$PROJECT_DIR/.."
    tar -czf "$BACKUP_FILE" "$(basename $PROJECT_DIR)"
    
    if [ -f "$BACKUP_FILE" ]; then
        log_success "Backup created: $BACKUP_FILE"
        ls -lh "$BACKUP_FILE"
    else
        log_error "Backup failed"
    fi
}

setup_git() {
    log_info "Setting up Git repository..."
    
    cd "$PROJECT_DIR"
    
    if [ ! -d ".git" ]; then
        git init
        echo "*.log" > .gitignore
        echo "__pycache__/" >> .gitignore
        echo "venv/" >> .gitignore
        
        git add .
        git commit -m "Initial commit: AI Agents System"
        
        log_success "Git repository initialized"
        log_info "To connect to GitHub:"
        log_info "  git remote add origin https://github.com/username/repo.git"
        log_info "  git push -u origin main"
    else
        log_info "Git repository already exists"
    fi
}

show_help() {
    echo "AI Agents System Management Script"
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  install    - Install dependencies"
    echo "  start      - Start the API server"
    echo "  stop       - Stop the API server"
    echo "  restart    - Restart the API server"
    echo "  status     - Check system status"
    echo "  backup     - Create backup"
    echo "  git        - Setup Git repository"
    echo "  help       - Show this help"
    echo ""
}

# Main execution
case "$1" in
    "install")
        check_environment
        install_dependencies
        ;;
    "start")
        check_environment
        start_api
        ;;
    "stop")
        stop_api
        ;;
    "restart")
        stop_api
        sleep 2
        start_api
        ;;
    "status")
        check_environment
        status_api
        ;;
    "backup")
        backup_project
        ;;
    "git")
        setup_git
        ;;
    "help"|"")
        show_help
        ;;
    *)
        log_error "Unknown command: $1"
        show_help
        exit 1
        ;;
esac

exit 0
EOF

chmod +x /root/ai_agents_project/scripts/manage.sh
