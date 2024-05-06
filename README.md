# SafeGPT-Backend


SafeGPT Backend is a tool designed to anonymize user data using various methods, including Microsoft Presidio Analyzer, Anonymizer Docker containers, and fine-tuned LLM (Large Language Model) models hosted on AWS SageMaker. The backend provides a secure and efficient way to process sensitive user information while preserving privacy.


#### Features

Anonymize user data using Microsoft Presidio Analyzer
Anonymize user data using anonymizer Docker containers
Utilize fine-tuned LLM models on AWS SageMaker for advanced anonymization
Expose a public API for easy integration with external systems
Seamless integration with public LLM APIs such as ChatGPT for sending anonymized data


#### Usage
#### 1) Ensure you have the necessary dependencies installed.
#### 2) Clone the SafeGPT Backend repository to your local machine.
#### 3) Configure the backend settings according to your requirements.
#### 4) Set up environment variables:
```
export ANALYZE_URL=http://localhost:5001/analyze
export ANONYMIZE_URL=http://localhost:5002/anonymize
...
```

#### 5) Run the backend server locally:
```
flask --app app run --debug
```

#### 6) Alternatively, if you want to run the app using Docker containers:
Ensure Docker is installed on your system. You can check by running `docker -v` and it should return something like:
```
Docker Compose version v2.6.0
```
####      Verify Docker Compose is installed by running docker-compose --version.
```
Docker Compose version v2.6.0
```
####      Run the following command to build and start the Docker containers
```
docker-compose up --build
```
