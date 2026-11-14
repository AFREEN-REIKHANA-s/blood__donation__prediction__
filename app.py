from flask import Flask, render_template, request, send_file
import joblib
import numpy as np
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# -----------------------------------
# Create Flask App
# -----------------------------------
app = Flask(__name__)

# -----------------------------------
# Load Model and Scaler
# -----------------------------------
model = joblib.load("blood_donation_model.pkl")
scaler = joblib.load("scaler.pkl")


# -----------------------------------
# Home Page
# -----------------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------------
# About Page
# -----------------------------------
@app.route("/about")
def about():
    return render_template("about.html")


# -----------------------------------
# Contact Page
# -----------------------------------
@app.route("/contact")
def contact():
    return render_template("contact.html")


# -----------------------------------
# Prediction
# -----------------------------------
@app.route("/predict", methods=["POST"])
def predict():

    try:
        # Get input values
        months_last = float(request.form["months_last"])
        donations = float(request.form["donations"])
        volume = float(request.form["volume"])
        months_first = float(request.form["months_first"])

        # Convert input into NumPy array
        data = np.array([
            [months_last, donations, volume, months_first]
        ])

        # Scale input data
        data_scaled = scaler.transform(data)

        # Make prediction
        prediction = model.predict(data_scaled)

        # Get prediction probability
        probability = model.predict_proba(data_scaled)

        # Calculate confidence
        confidence = round(np.max(probability) * 100, 2)

        # -----------------------------------
        # Donor Category
        # -----------------------------------
        if donations <= 5:
            category = "🆕 New Donor"

        elif donations <= 15:
            category = "⭐ Regular Donor"

        else:
            category = "🏆 Frequent Donor"

        # -----------------------------------
        # Prediction Result
        # -----------------------------------
        if prediction[0] == 1:

            result = "✅ The person is likely to donate blood."

            recommendation = (
                "This donor has a high probability of donating blood. "
                "Consider sending a donation reminder or scheduling an appointment."
            )

        else:

            result = "❌ The person is not likely to donate blood."

            recommendation = (
                "This donor has a lower probability of donating blood. "
                "Consider awareness campaigns or follow-up communication "
                "to encourage future donations."
            )

        # -----------------------------------
        # Store Data for PDF Report
        # -----------------------------------
        app.config["REPORT_DATA"] = {
            "prediction": result,
            "confidence": confidence,
            "category": category,
            "recommendation": recommendation,
            "months_last": months_last,
            "donations": donations,
            "volume": volume,
            "months_first": months_first
        }

        # -----------------------------------
        # Return Result to Home Page
        # -----------------------------------
        return render_template(
            "index.html",
            prediction=result,
            confidence=confidence,
            category=category,
            recommendation=recommendation
        )

    except Exception as e:

        return render_template(
            "index.html",
            error=f"Error: {str(e)}"
        )


# -----------------------------------
# Download PDF Report
# -----------------------------------
@app.route("/download_report")
def download_report():

    data = app.config.get("REPORT_DATA")

    # Check if prediction was made
    if not data:
        return "Please make a prediction first."

    filename = "Blood_Donation_Report.pdf"

    # Create PDF
    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    story = []

    # -----------------------------------
    # PDF Title
    # -----------------------------------
    story.append(
        Paragraph(
            "Blood Donation Prediction Report",
            styles["Title"]
        )
    )

    story.append(Spacer(1, 20))

    # -----------------------------------
    # Prediction Details
    # -----------------------------------
    story.append(
        Paragraph(
            f"<b>Prediction:</b> {data['prediction']}",
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 10))

    story.append(
        Paragraph(
            f"<b>Confidence:</b> {data['confidence']}%",
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 10))

    story.append(
        Paragraph(
            f"<b>Donor Category:</b> {data['category']}",
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 20))

    # -----------------------------------
    # Recommendation
    # -----------------------------------
    story.append(
        Paragraph(
            "<b>Recommendation</b>",
            styles["Heading2"]
        )
    )

    story.append(Spacer(1, 10))

    story.append(
        Paragraph(
            data["recommendation"],
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 20))

    # -----------------------------------
    # Input Details
    # -----------------------------------
    story.append(
        Paragraph(
            "<b>Input Details</b>",
            styles["Heading2"]
        )
    )

    story.append(Spacer(1, 10))

    story.append(
        Paragraph(
            f"Months Since Last Donation: {data['months_last']}",
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 8))

    story.append(
        Paragraph(
            f"Number of Donations: {data['donations']}",
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 8))

    story.append(
        Paragraph(
            f"Total Volume Donated: {data['volume']} cc",
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 8))

    story.append(
        Paragraph(
            f"Months Since First Donation: {data['months_first']}",
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            "Generated by Blood Donation Prediction System",
            styles["Italic"]
        )
    )

    # Build PDF
    doc.build(story)

    return send_file(
        filename,
        as_attachment=True
    )


# -----------------------------------
# Run Flask Application
# -----------------------------------
if __name__ == "__main__":
    app.run(debug=True)