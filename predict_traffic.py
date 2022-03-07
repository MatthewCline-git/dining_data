import csv
import graphviz
from sklearn import tree

silliman_features = [[0 for i in range(4)] for j in range(28)]
silliman_monthly = 0
silliman_daily = [0 for i in range(28)]

with open('door_data.csv','r') as file:
  for row in csv.reader(file, delimiter=' '):
    x = row[0].split(",")
    # building codes for silliman dining hall
    if x[4] == "62" and x[5] == "1":
      for i, j in enumerate(x):
        x[i] = int(j)
      # from 11:30 - 1:30
      if x[3] >= 690 and x[3] <= 810:
        if x[3] <= 705:
          silliman_features[x[2]][0] += 1
          silliman_features[x[2]][3] = x[1]
        if x[3] <= 720: 
          silliman_features[x[2]][1] += 1
          silliman_features[x[2]][3] = x[1]
        silliman_daily[x[2]] += 1

silliman_total = sum(silliman_daily)
silliman_mean = silliman_total / 28
silliman_labels = [None] * 28

for i, j in enumerate(silliman_daily):
  if j >= (silliman_mean * 1.05):
    silliman_labels[i] = "high"
  elif j <= (silliman_mean * .95):
    silliman_labels[i] = "low"
  else:
    silliman_labels[i] = "normal"

class_names = ["high", "low", "normal"]
feature_names = ["Before 11:45am", "Before 12:00pm", "Before 12:15pm", "Day of the Week"]

silliman_clf = tree.DecisionTreeClassifier(random_state = 1)
silliman_clf = silliman_clf.fit(silliman_features, silliman_labels)
silliman_dot_data = tree.export_graphviz(silliman_clf, class_names=class_names, feature_names=feature_names, filled=True)
silliman_graph = graphviz.Source(silliman_dot_data)
silliman_graph.render("Silliman_Decision_Tree")
print(silliman_clf.predict([[90, 171, 230, 0]]))