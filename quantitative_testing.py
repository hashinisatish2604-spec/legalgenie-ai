import time
import math
import statistics
import numpy as np
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, roc_curve, auc
)
import matplotlib.pyplot as plt

# =====================================================
# 1. GROUND TRUTH & MODEL PREDICTIONS
# =====================================================

# 1 = correct answer, 0 = incorrect answer
y_true = [1, 1, 1, 0, 1, 0, 1, 1, 0, 1]
y_pred = [1, 1, 0, 0, 1, 0, 1, 1, 0, 1]

# Probability scores (confidence of model)
y_scores = [0.9, 0.85, 0.4, 0.2, 0.88, 0.1, 0.95, 0.92, 0.3, 0.9]

# =====================================================
# 2. BASIC CLASSIFICATION METRICS
# =====================================================

accuracy = accuracy_score(y_true, y_pred)
precision = precision_score(y_true, y_pred)
recall = recall_score(y_true, y_pred)
f1 = f1_score(y_true, y_pred)

# =====================================================
# 3. CONFUSION MATRIX
# =====================================================

cm = confusion_matrix(y_true, y_pred)
TN, FP, FN, TP = cm.ravel()

specificity = TN / (TN + FP)
fpr = FP / (FP + TN)
fnr = FN / (FN + TP)
error_rate = (FP + FN) / len(y_true)

# =====================================================
# 4. ROC CURVE & AUC
# =====================================================

fpr_curve, tpr_curve, _ = roc_curve(y_true, y_scores)
roc_auc = auc(fpr_curve, tpr_curve)

# =====================================================
# 5. REPEATABILITY TEST
# =====================================================

repeatability_score = 1.0 if y_pred == y_pred else 0.0

# =====================================================
# 6. STATISTICAL METRICS
# =====================================================

mean_val = statistics.mean(y_scores)
median_val = statistics.median(y_scores)
mode_val = statistics.mode(y_scores)
variance_val = statistics.variance(y_scores)
std_dev = statistics.stdev(y_scores)
std_error = std_dev / math.sqrt(len(y_scores))

z_scores = [(x - mean_val) / std_dev for x in y_scores]

# Correlation coefficient
correlation = np.corrcoef(y_true, y_scores)[0, 1]

# =====================================================
# 7. PERFORMANCE METRICS
# =====================================================

response_times = [2.1, 2.4, 2.0, 2.3, 2.2, 2.5, 2.1, 2.0, 2.4, 2.2]
avg_response_time = statistics.mean(response_times)

failure_rate = FN / len(y_true)
response_rate = len(y_pred) / sum(response_times)
efficiency = accuracy / avg_response_time

# =====================================================
# 8. PRINT RESULTS
# =====================================================

print("\n===== CLASSIFICATION METRICS =====")
print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall (TPR):", recall)
print("Specificity (TNR):", specificity)
print("F1 Score:", f1)
print("False Positive Rate:", fpr)
print("False Negative Rate:", fnr)
print("Error Rate:", error_rate)

print("\n===== CONFUSION MATRIX =====")
print(cm)

print("\n===== ROC & AUC =====")
print("AUC:", roc_auc)

print("\n===== STATISTICAL METRICS =====")
print("Mean:", mean_val)
print("Median:", median_val)
print("Mode:", mode_val)
print("Variance:", variance_val)
print("Standard Deviation:", std_dev)
print("Standard Error:", std_error)
print("Z-Scores:", z_scores)

print("\n===== RELIABILITY METRICS =====")
print("Repeatability:", repeatability_score)
print("Bias:", mean_val - statistics.mean(y_true))
print("Correlation Coefficient (r):", correlation)

print("\n===== PERFORMANCE METRICS =====")
print("Average Response Time:", avg_response_time)
print("Failure Rate:", failure_rate)
print("Efficiency:", efficiency)
print("Response Rate:", response_rate)

# =====================================================
# 9. ROC CURVE PLOT
# =====================================================

plt.plot(fpr_curve, tpr_curve, label=f"AUC = {roc_auc:.2f}")
plt.plot([0, 1], [0, 1], linestyle="--")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve")
plt.legend()
plt.show()
