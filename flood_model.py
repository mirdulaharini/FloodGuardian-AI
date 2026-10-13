from sklearn.ensemble import RandomForestClassifier

# Demonstration training data only.
# Replace this with verified historical flood data
# before using predictions for real decisions.

X = [
    [10, 0, 0],
    [25, 0, 1],
    [40, 1, 0],
    [60, 1, 1],
    [80, 2, 1],
    [100, 2, 2],
    [150, 3, 2],
    [200, 3, 2],
    [30, 0, 0],
    [120, 1, 2],
    [70, 2, 0],
    [180, 3, 1],
]

# Features: rainfall in mm, water level score, drainage score
# Labels: 0 = Low, 1 = Moderate, 2 = High
y = [
    0, 0, 0, 1, 1, 2,
    2, 2, 0, 1, 1, 2
]

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)


def predict_flood_risk(rainfall, water_level_score, drainage_score):
    features = [[rainfall, water_level_score, drainage_score]]
    prediction = int(model.predict(features)[0])

    labels = {
        0: "LOW",
        1: "MODERATE",
        2: "HIGH",
    }

    return labels[prediction]