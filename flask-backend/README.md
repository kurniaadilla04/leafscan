# Flask Backend Demo Project

This is a simple Flask backend application designed for a demo project. It provides a structure for handling HTTP requests, managing data models, and serving static files.

## Project Structure

```
flask-backend
├── app
│   ├── __init__.py
│   ├── routes.py
│   ├── models.py
│   └── static
│       └── uploads
├── config.py
├── requirements.txt
└── README.md
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd flask-backend
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Configuration

Edit the `config.py` file to set up your configuration settings, such as database connection details and environment variables.

## Running the Application

To run the Flask application, use the following command:
```
flask run
```

Make sure to set the `FLASK_APP` environment variable to `app` before running the command.

## Usage

- The application defines various routes in `app/routes.py` that handle different HTTP requests.
- Data models are defined in `app/models.py` to interact with the database.
- Uploaded files are stored in the `app/static/uploads` directory.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.