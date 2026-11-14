# 🩸 Blood Donation Prediction System

A machine learning web application that predicts whether a donor is likely to donate blood again, with confidence scoring, donor categorization, and downloadable PDF reports.

---

## 📌 Overview

Blood banks rely on repeat donors, but contacting every donor is time-consuming. This project analyzes a donor's past donation history and estimates the likelihood of a future donation, so outreach can be focused on the right people.

For every prediction, the system provides:

- A likely / not likely classification
- A model confidence score
- A donor category based on donation frequency
- A recommendation for the blood bank
- A downloadable PDF report

---

## ✨ Features

- Machine learning based donor prediction
- Confidence score shown as a progress bar
- Automatic donor categorization (New, Regular, Frequent)
- Recommendation based on the prediction result
- PDF report generation
- Responsive design for desktop, tablet, and mobile

---

## 📥 Input Features

| Feature | Description |
|---------|-------------|
| Months Since Last Donation | Time since the donor's most recent donation |
| Number of Donations | Total number of past donations |
| Total Volume Donated (cc) | Total blood volume donated |
| Months Since First Donation | Time since the donor's first donation |

---

## 🏷️ Donor Categories

| Number of Donations | Category |
|---------------------|----------|
| 5 or fewer | 🆕 New Donor |
| 6 to 15 | ⭐ Regular Donor |
| More than 15 | 🏆 Frequent Donor |

---

## ⚙️ How It Works

1. The user enters four donation details in the web form.
2. The values are scaled using the saved scaler (`scaler.pkl`).
3. The trained model (`blood_donation_model.pkl`) predicts the outcome and probability.
4. The app assigns a donor category and generates a recommendation.
5. The result is displayed on the page and can be downloaded as a PDF.

---

## 🛠️ Tech Stack

- **Language:** Python
- **Backend:** Flask
- **Machine Learning:** scikit-learn, NumPy, Joblib
- **PDF Generation:** ReportLab
- **Frontend:** HTML, CSS, Jinja2

---

## 📁 Project Structure

```text
Blood_Donation_Project/
├── app.py                       # Flask application and routes
├── blood_donation_model.pkl     # Trained ML model
├── scaler.pkl                   # Fitted feature scaler
├── Blood_Donation_Report.pdf    # Sample generated PDF report
├── requirements.txt             # Python dependencies
├── README.md
└── templates/
    ├── index.html               # Home page, prediction form, results
    └── contact.html             # Contact page
```

---

## 🚀 Installation

**1. Clone the repository**

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git
cd YOUR-REPO-NAME
```

**2. Create a virtual environment**

```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS / Linux
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Run the application**

```bash
python app.py
```

**5. Open in your browser**

link in your terminal

---

## 🌐 Routes

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Home page and prediction form |
| `/predict` | POST | Runs the model and shows the result |
| `/download_report` | GET | Downloads the PDF report |
| `/contact` | GET | Contact page |

---

## ⚠️ Limitations

- Report data is stored at application level, so the app is meant for single-user or demo use.
- Predictions are estimates and should support, not replace, human decisions.
- Accuracy depends on the quality and size of the training data.

---

## 🔮 Future Improvements

- Per-user reports using Flask sessions
- Model performance page (accuracy, confusion matrix)
- Prediction history using a database
- Cloud deployment

---

## 👤 Author

**Your Name**
(Afreen Reikhana)