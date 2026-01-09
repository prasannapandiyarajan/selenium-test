FROM selenium/standalone-chrome:latest

# Install Python
USER root
RUN apt-get update && apt-get install -y python3 python3-pip
WORKDIR /home/seluser/project

# Copy project
COPY . .

# Install Python deps
RUN pip3 install selenium pytest pytest-html

# Default command to run tests
CMD ["pytest", "test_e2eTestFramework.py", "--browser_name", "chrome", "--html=reports/report.html", "--self-contained-html"]