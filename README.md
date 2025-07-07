QuickSum AI
=======================

A Streamlit-powered web application that performs text summarization using pre-trained Transformer models from Hugging Face. Users can input text manually or upload documents (.txt, .pdf, .docx) to generate concise summaries. The app supports multiple summarization models and can handle long texts by chunking them for better summarization quality.

---

Features
--------

- Manual Text Input: Paste or type text directly for summarization.
- File Upload: Upload multiple text files (.txt, .pdf, .docx) for batch summarization.
- Multiple Models: Choose from several pre-trained summarization models including:
  - BART Large CNN (facebook/bart-large-cnn)
  - T5 Small (t5-small)
  - DistilBART CNN (sshleifer/distilbart-cnn-12-6)
- Long Text Support: Automatically splits long documents into chunks before summarizing.
- Customizable Summary Length: Adjust maximum and minimum summary lengths via sliders.
- Download Summaries: Download generated summaries as .txt files.
- Clean and Duplicate-Free Summaries: Removes duplicate sentences and cleans input text.
- User-Friendly Interface: Intuitive tabs for manual input and file uploads with progress spinners.

---

Demo
----


![working](https://github.com/user-attachments/assets/efdcc6be-b65b-4c3b-83c3-13220774270d)


---

Installation
------------

Prerequisites:

- Python 3.7+
- pip package manager

Install dependencies:

    pip install streamlit transformers PyPDF2 python-docx

(Optional, for tunneling with ngrok):

    pip install pyngrok

---

Usage
-----

1. Clone the repository:

    git clone https://github.com/Faran18/QuickSum-AI.git

2. Run the Streamlit app:

    streamlit run app.py

3. Open your browser at the URL shown in the terminal (or use Ngrok).

4. Use the sidebar to select the summarization model.

5. Use the tabs to enter text manually or upload files for summarization.

---

How It Works
------------

- The app uses Hugging Face's transformers pipeline for summarization.
- For inputs longer than 1024 words, the text is split into chunks and each chunk is summarized separately.
- Summaries are cleaned to remove duplicate sentences and excessive whitespace.
- Supports .txt, .pdf, and .docx file uploads with text extraction handled by PyPDF2 and python-docx.
- Caches loaded models to improve performance on repeated summarizations.

---

Supported Models
----------------

| Model Name       | Hugging Face Model ID               | Advantage                          |
|------------------|-----------------------------------|--------------------------------|
| BART Large CNN   | facebook/bart-large-cnn           | Strong summarization baseline  |
| T5 Small         | t5-small                         | Lightweight, faster inference  |
| DistilBART CNN   | sshleifer/distilbart-cnn-12-6     | Smaller, faster variant         |

You can easily add more models by updating the SUMMARIZATION_MODELS dictionary in app.py.

---

Troubleshooting
---------------

- Missing ScriptRunContext warnings:  
  Run the app using `streamlit run app.py` to avoid these warnings.

- Model download slow or fails:  
  Ensure you have a stable internet connection. Models are cached locally after first download.

- File upload issues:  
  Supported file types are .txt, .pdf, .docx. Ensure files are not corrupted.

---


Optional Ngrok Authentication Setup
--------------------------

Before running the app, you need to set your ngrok authentication token. This token authorizes your ngrok client to create secure tunnels.

The following steps are used in the codebase to set up the token:

1. **Set the environment variable in Python:**

    ```
    import os
    os.environ["NGROK_AUTH_TOKEN"] = "your-ngrok-auth-token"
    ```

2. **Write the token to a `.env` file:**

    ```
    with open(".env", "w") as f:
        f.write('NGROK_AUTH_TOKEN=your-ngrok-auth-token')
    print(".env file created")
    ```

Replace `"your-ngrok-auth-token"` with your actual token from your ngrok dashboard.

This setup ensures that when the app runs, ngrok can authenticate and create a public URL to share your locally running Streamlit app.

---

