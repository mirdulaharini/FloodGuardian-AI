from flood_model import predict_flood_risk

risk = predict_flood_risk(100, 2, 1)

print("Flood Guardian AI - Model Test")
print("Rainfall: 100 mm")
print("Water level score: 2")
print("Drainage score: 1")
print("Predicted risk:", risk)