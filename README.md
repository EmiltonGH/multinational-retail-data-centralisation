# Multinational Retail Data Centralisation

## Table of Contents
- Description
- Installation
- Usage
- File Structure
- License

## Description
You work for a multinational company that sells various goods across the globe.
Currently, their sales data is spread across many different data sources making it not easily accessible or analysable by current members of the team.
In an effort to become more data-driven, your organisation would like to make its sales data accessible from one centralised location.
Your first goal will be to produce a system that stores the current company data in a database 
so that it's accessed from one centralised location and acts as a single source of truth for sales data.
You will then query the database to get up-to-date metrics for the business.

The primary aim of this project is to address the challenges associated with managing retail data across multiple locations. 
By centralizing data, the project aims to:
- Enhance data accuracy: Ensure that retail data is consistent and accurate across all branches.
- Improve decision-making: Provide a unified platform for analyzing data, enabling better-informed business decisions.
- Simplify data management: Streamline the process of collecting and managing retail data, reducing operational complexities.

Throughout the development of the Multinational Retail Data Centralisation project, we gained valuable insights into:
- Data centralization techniques: Strategies for efficiently consolidating and organizing data from diverse sources.
- Python scripting for data management: Leveraging Python to create the `MRDC_Project.py` script for data processing and analysis.
- Collaborative development: Understanding the importance of collaboration in a version-controlled environment using Git and GitHub.

This project serves as both a practical solution for multinational retail data management and 
a learning experience in the realms of data science, scripting, and collaborative software development.

## Installation instructions
Before you start using the Multinational Retail Data Centralisation project, ensure that you have the following prerequisites installed:
- Python: [Download and install Python](https://www.python.org/downloads/)
- To run this project locally, follow these steps:
  Clone the repository:
   ```bash
    git clone https://github.com/EmiltonGH/multinational-retail-data-centralisation.git
- Before you run the script,please make sure to install all required packages :
  - tabula
  - jpype
  - yaml
  - sqlalchemy
  - pandas 
  - datetime
  - requests
  - boto3
  - BytesIO

## Usage instructions
- Navigate to the Project Directory: cd multinational-retail-data-centralisation
- Run the MRDC_Project Script:  python MRDC_Project.py
- AWS Services Integration:
  - As this script interacts with AWS services such as S3 for storage, DynamoDB for database operations
    you would need an AWS account to set up and configure these services.
  - As this script makes API calls to AWS services using AWS SDKs or libraries,
    you need AWS credentials (Access Key ID and Secret Access Key) associated with an AWS account.
  - As this script needs to authenticate and authorize against AWS services,
    you would typically use AWS Identity and Access Management (IAM) roles, which are associated with your AWS account.

## File structure of the project
multinational-retail-data-centralisation/
|-- MRDC_Project.py
|-- README.md



