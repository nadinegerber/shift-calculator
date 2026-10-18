
<img width="1600" height="512" alt="shift_calculator_banner" src="https://github.com/user-attachments/assets/dd51a954-4f34-45bc-9a44-132a57083b53" />


# 📅 4-On / 4-Off Shift Schedule Web Application

An interactive, mobile-optimized web dashboard built with Streamlit to calculate and display a repeating 4-days-on and 4-days-off work shift schedule. 

Designed specifically for easy viewing on mobile phones and desktop browsers.

[Shift Calculator App](https://chris-benita.streamlit.app/)

<br>

## ✨ Key Features

* **Automated Shift Calculation:** Uses robust modulo arithmetic (`elapsed_days % 8`) to calculate shift cycles from any specified historical anchor date.

* **Vacation Override System:** Allows users to input approved vacation or leave date ranges, automatically overriding regular shift cycles with holiday indicators.

* **Mobile-Optimized Layout:** Formatted specifically to prevent horizontal wrapping on small phone screens, featuring compact emoji badges and clear layout margins.

* **Visual Color Coding:** Instantly distinguishes between work days, off days, and vacation periods using soft custom row background colors.

* **Dynamic Table Sizing:** Automatically calculates table height to display all days of the month cleanly without requiring internal scrollbars.

<br>


<br>

## 🛠️ Tech Stack & Dependencies

* **Python 3.10+**
* **Streamlit** (Web framework)
* **Pandas** (Data manipulation and table styling)

### Required Python Packages (`requirements.txt`)
```text
streamlit
```
<br>
<br>

## 🚀 Running the App Locally

To run this application locally on your machine using your terminal:

### 1.Clone the repository:
```bash
git clone [https://github.com/nadinegerber/shift-calculator.git](https://github.com/nadinegerber/shift-calculator.git)
cd shift-calculator
```

### 2. Install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Launch the Streamlit app:
```bash
streamlit run app.py
```
<br>
<br>


## 🌐 Live Deployment

This application is hosted and deployed live on Streamlit Community Cloud, automatically syncing with the main branch of this GitHub repository.

[View the Live Shift Calculator App](https://chris-benita.streamlit.app/)


