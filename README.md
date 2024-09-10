This README provides an overview of the project, including team details, relevant links, tasks completed, tech stack, key features, and steps to run the project locally.

## Team Details

**Team Name:** ERROR 404 : CHANGE FOUND?

**Project Title** -Online Chatbot based ticketing system

**Team Leader:** [@HARSHDIPSAHA](https://github.com/HARSHDIPSAHA)

**Team Members:**

- **ANSHUMAN RAJ** - 2023UCD3053 - [@SAVAGECAT05](https://github.com/SAVAGECAT05)
- **HEMANK KAUSHIK** - 2023UEI2867 - [@HEMANKKAUSHIK](https://github.com/HEMANKKAUSHIK)
- **KANISHK SHARMA** - 2023UCD2175 - [@GHOSTDOG007](https://github.com/GHOSTDOG007)
- **ANSHIKA SINGH** - 2023UCA1946 - [@CUBIX33](https://github.com/CUBIX33)
- **HARSHDIP SAHA** - 2023UCA1897 - [@HARSHDIPSAHA](https://github.com/HARSHDIPSAHA)
- **AMAN BIHARI** - 2023UCA1910 - [@CODEBREAKER32](https://github.com/CODEBREAKER32)

- **Live Deployment:** [View Deployment](https://willowy-toffee-89c6b8.netlify.app/)
  (backend deployment is removed due to insufficient aws credits)


**Run locally**
## Local Setup Instructions (Write for both windows and macos)

Follow these steps to run the project locally

1. **Clone the Repository**
   ```bash
   git clone https://github.com/HARSHDIPSAHA/SIH1648_ERROR_404_CHANGE_FOUND
   cd REPO_DIRECTORY
   ```

# Django Backend 

This project is a Django-based backend for managing diabetes patient data, providing user authentication, patient data handling, and integration with machine learning models for outcome predictions and recommendations.
### 1. Clone the repository
 ```bash
git clone <https://github.com/HARSHDIPSAHA/SIH1648_ERROR_404_CHANGE_FOUND>
```
### 2. Create and activate a virtual environment
 ```bash
python3 -m venv venv
source venv/bin/activate
``` 
For Windows, use `venv\Scripts\activate`

### 2. Install the dependencies
 ```bash
pip install -r requirements.txt
```
### 3. Setup the Django project (migrate database and create superuser)
 ```bash
python manage.py migrate
```
### 3. Start the development server
 ```bash

python manage.py createsuperuser
```
### 4. Run the server
 ```bash
python manage.py runserver
```
# REACT FRONTEND 
## Prerequisites
- Node.js (v14.x or later)
- npm (v6.x or later) or yarn.

## Setup instructions 

### 1. Clone the repository 
```bash
git clone <https://github.com/HARSHDIPSAHA/SIH1648_ERROR_404_CHANGE_FOUND>

```
### 2. Install the dependencies 
 ```bash
npm install
npm install react-scripts 
npm install react-router-dom
```
```bash
npm start
```
### 4. Build for production (optional)
 ```bash
npm run build
```
### 5. For Backend Integration 
```bash 
npm install axios

