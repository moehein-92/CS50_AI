import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).
    """
    with open("shopping.csv") as f:
        reader = csv.reader(f)
        next(reader)
        e_list = []
        l_list = []
        for line in reader:
            l_list.append(1 if line[17] == "TRUE" else 0)
            c_list = []
            c_list.append(int(line[0]))
            c_list.append(float(line[1]))
            c_list.append(int(line[2]))
            c_list.append(float(line[3]))
            c_list.append(int(line[4]))
            c_list.append(float(line[5]))
            c_list.append(float(line[6]))
            c_list.append(float(line[7]))
            c_list.append(float(line[8]))
            c_list.append(float(line[9]))
            if line[10] == "Jan":
                c_list.append(0)
            elif line[10] == "Feb":
                c_list.append(1)
            elif line[10] == "Mar":
                c_list.append(2)
            elif line[10] == "Apr":
                c_list.append(3)
            elif line[10] == "May":
                c_list.append(4)
            elif line[10] == "June":
                c_list.append(5)
            elif line[10] == "Jul":
                c_list.append(6)
            elif line[10] == "Aug":
                c_list.append(7)
            elif line[10] == "Sep":
                c_list.append(8)
            elif line[10] == "Oct":
                c_list.append(9)
            elif line[10] == "Nov":
                c_list.append(10)
            elif line[10] == "Dec":
                c_list.append(11)
            c_list.append(int(line[11]))
            c_list.append(int(line[12]))
            c_list.append(int(line[13]))
            c_list.append(int(line[14]))
            c_list.append(1 if line[15] == "Returning_Visitor" else 0)
            c_list.append(1 if line[16] == "TRUE" else 0)

            e_list.append(c_list)

    return(e_list, l_list)

def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    return model.fit(evidence, labels)


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return sensitivity and specificity.
    """
    positive_labels = 0
    negative_labels = 0
    prediction_correct = 0
    prediction_incorrect = 0

    for i, j in zip(labels, predictions):
        if i == 1:
            positive_labels += 1
            if j == 1:
                prediction_correct += 1
        elif i == 0:
            negative_labels += 1
            if j == 0:
                prediction_incorrect += 1
    
    sensitivity = round((prediction_correct/positive_labels), 2)
    specificity = round((prediction_incorrect/negative_labels), 2)

    return (sensitivity, specificity)

if __name__ == "__main__":
    main()
