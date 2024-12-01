# Healthcare Log Processing with Hadoop

## Project Overview
A scalable, Hadoop-based solution for processing and analyzing healthcare ETL log files. This project transforms unstructured log data into a normalized SQL database, enabling efficient analysis of ETL processes, data transformations, and system patterns.

### Key Features
- Processes large-scale healthcare ETL log files using Hadoop/PySpark
- Extracts stored procedures and database operations from log text
- Creates normalized SQL mapping database for analysis
- Runs in containerized environment using Docker
- Enables tracking of data transformations and ETL patterns

### Business Value
- **Data Analysis**: Transform raw logs into structured, queryable data
- **Pattern Recognition**: Identify common ETL patterns and transformations
- **Process Monitoring**: Track and analyze ETL operations
- **Scalability**: Handle large volumes of log data efficiently
- **Maintainability**: Containerized solution for easy deployment

## Prerequisites

### Required Software
1. **Python 3.11.x**
   - Download from [Python.org](https://www.python.org/downloads/)
   - During installation:
     - Check "Add Python to PATH"
     - Choose "Customize installation"
     - Select all optional features

2. **Docker Desktop**
   - Requirements:
     - Windows 10/11 Home, Pro, Enterprise, or Education
     - WSL 2 (Windows Subsystem for Linux)
     - 8GB RAM minimum (16GB recommended)
   - Installation:
     - Download [Docker Desktop](https://www.docker.com/products/docker-desktop/)
     - Choose AMD64 version for Intel/AMD processors
     - Follow installation prompts
     - Accept Docker Subscription Service Agreement (free for personal use)

3. **WSL 2 Setup**
   ```powershell
   # Run in PowerShell as Administrator
   dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
   dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
   wsl --install -d Ubuntu
   wsl --set-default-version 2
   ```

4. **VSCode Extensions**
   - Python
   - Docker
   - Remote Development

## Project Structure
```
healthcare_hadoop/
├── data/                  # Directory for database files
├── src/
│   ├── config.py         # Configuration settings
│   ├── db_setup.py       # Database initialization
│   └── log_processor.py  # Main processing logic
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Multi-container Docker setup
├── requirements.txt      # Python dependencies
└── README.md            # Project documentation
```

## Installation & Setup

1. **Clone the Repository**
   ```bash
   git clone [your-repository-url]
   cd healthcare_hadoop
   ```

2. **Set Up Python Environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # On Windows:
   .\venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Initialize Databases**
   ```bash
   python src/db_setup.py
   ```

4. **Docker Setup**
   ```bash
   # Build and start containers
   docker-compose up -d
   ```

## Usage

1. **Process Log Files**
   ```bash
   python src/log_processor.py
   ```

2. **View Results**
   - Check the mapping database in `data/target.db`
   - Use SQL queries to analyze extracted data

## Development

### Local Development
1. Use VSCode with Python extension
2. Set up Python interpreter from virtual environment
3. Use integrated terminal for commands
4. Debug with VSCode's debugging tools

### Docker Development
1. Build development container:
   ```bash
   docker-compose -f docker-compose.dev.yml build
   ```
2. Start development environment:
   ```bash
   docker-compose -f docker-compose.dev.yml up
   ```

## Troubleshooting

### Common Issues

1. **Docker Desktop Not Starting**
   - Verify WSL 2 installation
   - Check system requirements
   - Run as administrator
   - Restart Docker service

2. **Python Environment Issues**
   - Verify Python installation
   - Check PATH environment variable
   - Recreate virtual environment

3. **Database Connection Issues**
   - Check database files in data directory
   - Verify permissions
   - Check connection strings in config.py

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Thanks to the Apache Hadoop and Spark communities
- Healthcare data warehouse team for project requirements
- Contributors and maintainers
