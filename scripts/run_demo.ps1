Write-Host "Generating sample data..."
python data_generator/generate_data.py

Write-Host "Running Spark job..."
python spark/jobs/process_health_data.py

Write-Host "Showing alerts..."
python dashboard/cli_demo.py
