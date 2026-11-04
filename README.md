# NHRIS — National Health Risk Intelligence System

> **AI-Powered National Healthcare Monitoring & Early Warning Platform**  
> *Detect Early. Respond Faster. Protect Lives.*

## Overview

**National Health Risk Intelligence System (NHRIS)** is an AI-powered healthcare intelligence platform designed to monitor population health trends, detect emerging disease outbreaks, identify hospital overload risks, and generate early warnings for healthcare authorities.

The platform integrates healthcare data from hospitals, laboratories, and clinics through distributed data processing pipelines. It analyzes incoming health records, identifies abnormal patterns using machine learning, and generates actionable intelligence through automated alerts, an AI assistant, and voice-based interaction.

NHRIS aims to transform fragmented healthcare data into actionable public health intelligence.

## Problem Statement

Healthcare institutions generate enormous volumes of patient and operational data. However, identifying early indicators of disease outbreaks and healthcare infrastructure stress remains challenging.

This can result in:

- Delayed detection of infectious disease outbreaks.
- Unexpected hospital capacity shortages.
- Insufficient oxygen and critical care resources.
- Delayed emergency response and intervention.
- Limited visibility into regional healthcare risks.

## Solution

NHRIS provides a centralized intelligence platform that continuously analyzes healthcare data to identify emerging risks.

### Core Capabilities

| Capability | Description |
|---|---|
| Outbreak Detection | Identifies unusual increases in regional disease indicators. |
| Fever Spike Monitoring | Detects abnormal fever patterns across geographical regions. |
| Oxygen Risk Detection | Identifies unusual oxygen saturation patterns. |
| Hospital Overload Prediction | Highlights hospitals experiencing potential capacity pressure. |
| Regional Risk Analysis | Identifies geographical clusters of abnormal health indicators. |
| Automated Alerts | Generates notifications for identified high-risk patterns. |
| AI Healthcare Assistant | Enables natural-language queries about healthcare intelligence. |
| Voice Interaction | Supports voice-based interaction through Sarvam AI. |

## System Architecture

```text
       Hospitals / Labs / Clinics
                   |
                   v
            Data Ingestion
                   |
                   v
        Apache Spark Processing
                   |
                   v
             Delta Lake
                   |
                   v
          AI Risk Detection
          (Isolation Forest)
                   |
          +--------+--------+
          |        |        |
          v        v        v
        Alerts   Analytics  Risk Insights
          |        |        |
          +--------+--------+
                   |
                   v
          AI Assistant (ADK)
                   |
                   v
          Voice Interface
                   |
                   v
        Healthcare Dashboard
```

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Data analytics and risk detection |
| Apache Spark | Distributed healthcare data processing |
| Delta Lake | Reliable, versioned data storage |
| Apache Airflow | Workflow orchestration and scheduling |
| Isolation Forest | Machine learning-based anomaly detection |
| Docker | Containerization and deployment |
| Google Agent Development Kit | AI assistant development |
| Sarvam AI | Voice interaction |
| Streamlit | Healthcare monitoring dashboard |

## Repository Structure

```text
NHRIS/
│
├── airflow/
│   └── dags/
│       └── nhris_pipeline.py
│
├── spark/
│   └── jobs/
│       ├── process_health_data.py
│       └── stream_process_health_data.py
│
├── data_generator/
│   ├── generate_data.py
│   └── generate_data_stream.py
│
├── schemas/
│   └── delta_tables.md
│
├── api/
│   └── app.py
│
├── agent/
│   ├── google_adk_agent.py
│   └── nhris_adk_agent/
│       └── agent.py
│
├── voice/
│   └── sarvam_voice.py
│
├── dashboard/
│   ├── app.py
│   └── cli_demo.py
│
├── docker-compose.yml
└── README.md
```

## Getting Started

### Prerequisites

Ensure the following tools are installed:

- Python 3.10+
- Apache Spark
- Java
- Docker and Docker Compose
- Apache Airflow (if running independently)

### 1. Clone the Repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd NHRIS
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Generate Sample Healthcare Data

```bash
python data_generator/generate_data.py
```

### 4. Execute the Spark Processing Pipeline

```bash
spark-submit \
  --packages io.delta:delta-spark_2.12:3.2.0 \
  spark/jobs/process_health_data.py
```

### 5. View Generated Alerts

```bash
python dashboard/cli_demo.py
```

### 6. Launch the Monitoring Dashboard

```bash
streamlit run dashboard/app.py
```

## Real-Time Streaming Demo

NHRIS also supports a streaming data-processing workflow for continuously generated healthcare data.

**Step 1 — Start the streaming data generator**

```bash
python data_generator/generate_data_stream.py
```

**Step 2 — Start the Spark streaming processor**

```bash
spark-submit \
  --packages io.delta:delta-spark_2.12:3.2.0 \
  spark/jobs/stream_process_health_data.py
```

This demonstrates continuous data ingestion and processing for near-real-time healthcare risk monitoring.

## Docker Deployment

For a simplified demonstration, launch the platform using Docker Compose.

```bash
docker compose up --build
```

### Available Services

| Service | Local URL |
|---|---|
| Airflow UI | http://localhost:8080 |
| Backend API | http://localhost:8000 |
| ADK Agent API | http://localhost:8002 |

*Service availability depends on the Docker Compose configuration and successful container initialization.*

## AI Healthcare Assistant

The NHRIS AI assistant allows healthcare authorities to interact with processed healthcare intelligence using natural-language queries.

### Example Queries

- Which regions show abnormal fever cases today?
- Which hospitals are experiencing potential overload?
- Show the high-risk districts.
- Identify unusual regional health patterns.
- Summarize the latest healthcare risk alerts.

The assistant is designed to make complex healthcare analytics more accessible to decision-makers.

## Machine Learning & Risk Detection

NHRIS uses the **Isolation Forest** algorithm for unsupervised anomaly detection.

The model identifies unusual patterns in healthcare indicators that may represent emerging risks.

### Detection Workflow

1. Ingest healthcare records.
2. Process and transform incoming data using Apache Spark.
3. Store processed datasets in Delta Lake.
4. Extract relevant healthcare indicators.
5. Apply Isolation Forest anomaly detection.
6. Identify abnormal patterns.
7. Generate risk insights and alerts.

**Important:** Anomaly detection identifies unusual patterns, not confirmed disease outbreaks or clinical diagnoses. Alerts require validation by qualified public health professionals.

## Future Enhancements

- Integration with real hospital and laboratory data feeds.
- Apache Kafka for scalable streaming ingestion.
- Advanced outbreak forecasting models.
- Geospatial disease cluster visualization.
- Predictive hospital bed and ICU capacity monitoring.
- Integration with public health surveillance systems.
- Role-based access control for healthcare authorities.
- Automated alert delivery and escalation workflows.
- Advanced multilingual voice interaction.

## Project Vision

NHRIS envisions a connected healthcare intelligence ecosystem where distributed healthcare data can be transformed into early warnings, predictive insights, and actionable information.

By combining distributed computing, machine learning, AI agents, and voice technology, the platform aims to support faster and more informed public health decision-making.

## Disclaimer

NHRIS is an experimental healthcare intelligence and monitoring platform intended for demonstration and research purposes. It does not replace professional medical judgment, clinical diagnosis, or official public health surveillance systems.

## License

Add your preferred open-source license before distributing this project.

---

**NHRIS — National Health Risk Intelligence System**

*Turning Healthcare Data into Early Warnings and Actionable Intelligence.*
