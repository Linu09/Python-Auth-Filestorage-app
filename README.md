<a name="readme-top"></a>

# Python Login System with GCP Integration


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>
<!-- ABOUT THE PROJECT -->

## About The Project
<img width="544" alt="image" src="https://github.com/Linu09/Python-Auth-Filestorage-app/assets/38865727/396c3098-5912-4d26-a608-3239dd07964f">
<img width="474" alt="image" src="https://github.com/Linu09/Python-Auth-Filestorage-app/assets/38865727/444b97f6-7057-4546-a25d-52ab5162e8f7">


This project demonstrates a simple web application using Flask for user authentication and Google Cloud Platform (GCP) services for storage and data persistence. Users can sign up, log in, upload files, and download files associated with their accounts.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

Various Tools and Technoloies used for  building this project

* Python3
* gcloud CLI
* GCP BigQuery
* GCP Container Registry
* GitHub Repos + Actions
* GCP Storage Bucket
* HTML/CSS

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

Follow these steps to get the project up and running on your local machine.

### Prerequisites

Before running the application, make sure you have the following:

- Python installed (version 3.x recommended)
- Google Cloud Platform account with Cloud Storage and BigQuery enabled
- GCP Service Account credentials JSON file
- Dataset & bucket created in google cloud
- All the above data passed into the python fil

### Installation

1. Clone the repo & get inside the repo
   ```sh
   git clone https://github.com/Linu09/Python-Auth-Filestorage-app.git
   ```
2. Enable venv
      ```sh
   venv/bin/activate
   ```
3. Install the Required Python Packages
      ```sh
   pip install -r requirements.txt
   ```
4. Run app.py
      ```sh
   python app.py
   ```
5. Output will look like below and you will be able to access the application over http://127.0.0.1:5000
 ```sh
 * Serving Flask app 'app-2'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
```


