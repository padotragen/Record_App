Got it! Here's the full `README.md` file presented in **one single code block** without breaking across messages:

````markdown
# Record_App 🎵

A Flask web application to display your personal album collection using the [Discogs API](https://www.discogs.com/developers). Built with Flask, Jinja2, HTML, CSS, and JavaScript, this app provides a clean and simple interface to explore your music library.

## 🔧 Features

- Pulls your collection directly from Discogs
- Displays album cover art and metadata
- Lightweight and customizable UI
- Uses Discogs' official API with your personal user token

## 🧰 Technologies Used

- Python 3
- Flask
- Jinja2 templating
- HTML/CSS
- JavaScript
- [`python3-discogs-client`](https://github.com/joalla/discogs_client)

## 📦 Prerequisites

- Python 3.x installed on your system
- A Discogs account and a generated User Token (see [Authentication Docs](https://www.discogs.com/developers#page:authentication))

## 🛠️ Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/padotragen/Record_App.git
   cd Record_App
   ```

2. **Create and activate a virtual environment (optional but recommended):**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required Python packages:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your environment variables:**

   - Copy the example file:

     ```bash
     cp .env.example .env
     ```

   - Edit `.env` and add your Discogs User Token. Instructions to generate this token can be found [here](https://www.discogs.com/developers#page:authentication).

## 🚀 Running the App

Once everything is set up, run the Flask server:

```bash
flask run
```

Navigate to `http://localhost:5000` in your browser to view your record collection!

## 🤝 Contributing

Feel free to fork the project and submit pull requests. Suggestions and bug reports are always welcome!

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.
````
