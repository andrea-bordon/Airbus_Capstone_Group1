# Airbus Fuel Leak Detection - Capstone Project Group 1

## 🚀 Project Overview
This project aims to improve the automatic detection of aircraft fuel leaks using data analytics and machine learning. The current detection methods rely on visual inspections post-landing, which is inefficient and can lead to increased Aircraft on Ground (AOG) time. Our objective is to develop a predictive model that enhances leak detection, allowing for proactive maintenance and reducing fleet downtime.

## 📌 Problem Statement
Fuel leaks in aircraft are detected manually through post-flight visual inspections. However, this method has significant drawbacks:
- **Inaccuracy**: Automated detection by the aircraft is unreliable due to fuel volume measurement errors.
- **Causes**: Common causes of fuel leaks include tank sealant degradation and structural damage.
- **Consequences**: Fuel leaks lead to AOG situations, disrupting fleet operations and increasing maintenance costs.

## 🎯 Project Goals
1. **Develop a predictive model** to detect fuel leaks not identified by standard inspections.
2. **Analyze sensor data** to identify key variables contributing to fuel leaks.
3. **Improve operational efficiency** by reducing unscheduled maintenance and increasing fleet availability.
4. **Provide insights** through exploratory data analysis (EDA) to understand fuel leak patterns.

## 📊 Dataset
We utilize time-series sensor data collected from **8 different aircraft**, covering approximately **500 flights**. The dataset consists of cleaned and preprocessed sensor readings.

### ✈️ Key Features in the Dataset
- **Aircraft & Flight Data**: Flight number, phase, altitude, UTC time.
- **Fuel & Engine System Data**:
  - Fuel used per engine (FUEL_USED_1, FUEL_USED_2, etc.)
  - Fuel on board (FOB)
  - Fuel quantity per collector cell and surge tank
  - Pump status (On/Off, normal/abnormal, immersed/not immersed)
  - Leak detection and fuel transfer mode

## 🔍 Methodology
1. **Exploratory Data Analysis (EDA)**: Identify patterns, anomalies, and critical trends in fuel leak occurrences.
2. **Feature Engineering**: Transform raw sensor data into useful features for leak detection.
3. **Predictive Modeling**:
   - Train machine learning models to classify fuel leak events.
   - Compare different algorithms to identify the best-performing model.
4. **Evaluation & Validation**: Assess model performance using precision, recall, and F1-score.
5. **Deployment & Recommendations**: Suggest actionable insights for fleet operators.

## 🛠️ Tools & Technologies
- **Python** (Pandas, NumPy, Scikit-learn, TensorFlow/PyTorch)
- **Jupyter Notebooks** for data analysis
- **Matplotlib & Seaborn** for data visualization
- **Time-series forecasting techniques**

## 📌 Expected Outcomes
- A **predictive model** capable of identifying fuel leaks before they become critical issues.
- Improved **aircraft availability** and reduced unscheduled maintenance costs.
- **Data-driven insights** to optimize maintenance operations and fleet management.

## 📜 Contributors
This project is developed as part of a **Master's Capstone Project** in collaboration with Airbus.

## 👥 Participants
[Matteo Becchis](https://github.com/mbecchis)

[Andrea Bordon](https://github.com/andrea-bordon)

[Gabriel Chapman](https://github.com/Gechz)

[Santiago Ramírez Planter](https://github.com/santiagoplanter)

[Siriyakorn Suepiantham](https://github.com/gssuepian)

## 📂 Repository Structure
```
├── data/                 # Raw and preprocessed datasets
├── notebooks/            # Jupyter notebooks for EDA and modeling
├── documents/            # Source documents for understading of case
├── models/               # Saved machine learning models
├── reports/              # Documentation and analysis reports
├── README.md             # Project overview
```

## 📧 Contact
For any inquiries or collaborations, feel free to reach out!

---
_This project contributes to advancing predictive maintenance in the aviation industry._ ✈️

