import sys
import csv
import re
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use the 'Agg' backend for better performance
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QInputDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QFileDialog, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class SpearmanCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.x = []
        self.y = []
        self.correlation = None

    def initUI(self):
        self.setWindowTitle("Spearman's Rank Correlation Calculator")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Input fields
        input_layout = QHBoxLayout()
        self.x_input = QLineEdit()
        self.y_input = QLineEdit()
        input_layout.addWidget(QLabel("X Values:"))
        input_layout.addWidget(self.x_input)
        input_layout.addWidget(QLabel("Y Values:"))
        input_layout.addWidget(self.y_input)
        main_layout.addLayout(input_layout)

        # Buttons
        button_layout = QHBoxLayout()
        calculate_button = QPushButton("Calculate")
        calculate_button.clicked.connect(self.calculate)
        import_button = QPushButton("Import CSV")
        import_button.clicked.connect(self.import_csv)
        export_graph_button = QPushButton("Export Graph as PNG")
        export_graph_button.clicked.connect(self.export_graph)
        export_results_button = QPushButton("Export Results as CSV")
        export_results_button.clicked.connect(self.export_results)
        button_layout.addWidget(calculate_button)
        button_layout.addWidget(import_button)
        button_layout.addWidget(export_graph_button)
        button_layout.addWidget(export_results_button)
        main_layout.addLayout(button_layout)

        # Results display
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        main_layout.addWidget(self.result_text)

        # Graph
        self.figure = plt.figure(figsize=(5, 4))
        self.canvas = FigureCanvas(self.figure)
        main_layout.addWidget(self.canvas)

    def parse_numbers(self, input_string):
        # Use regex to find all numbers (including decimals and scientific notation)
        numbers = re.findall(r'-?\d*\.?\d+(?:[eE][-+]?\d+)?', input_string)
        return [float(num) for num in numbers]

    def calculate(self):
        self.x = self.parse_numbers(self.x_input.text())
        self.y = self.parse_numbers(self.y_input.text())
        self.process_data(self.x, self.y)

    def import_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv)")
        if file_path:
            try:
                with open(file_path, 'r') as csv_file:
                    csv_reader = csv.reader(csv_file)
                    self.x = []
                    self.y = []
                    for row in csv_reader:
                        if len(row) >= 2:
                            try:
                                self.x.append(float(row[0]))
                                self.y.append(float(row[1]))
                            except ValueError:
                                continue  # Skip rows with non-numeric data
                
                if len(self.x) == 0 or len(self.y) == 0:
                    self.display_message("Error: No valid numeric data found in the CSV file.")
                else:
                    self.x_input.setText(' '.join(map(str, self.x)))
                    self.y_input.setText(' '.join(map(str, self.y)))
                    self.process_data(self.x, self.y)
            except Exception as e:
                self.display_message(f"Error reading CSV file: {str(e)}")
        else:
            self.display_message("No file selected.")

    def process_data(self, x, y):
        def assign_ranks(data):
            sorted_data = sorted(data)
            ranks = []
            for value in data:
                rank = sorted_data.index(value) + 1
                ranks.append(rank)
            return ranks

        if len(x) != len(y):
            self.display_message("Error: The number of X values must be equal to the number of Y values.")
            return

        x_ranks = assign_ranks(x)
        y_ranks = assign_ranks(y)

        totalsquares = sum((x_ranks[i] - y_ranks[i])**2 for i in range(len(x_ranks)))
        n = len(x)
        self.correlation = 1 - ((6 * totalsquares) / (n * (n**2 - 1)))

        correlation_type = "Positive" if self.correlation > 0 else "Negative" if self.correlation < 0 else "No"
        strength = "Weak" if abs(self.correlation) < 0.3 else "Moderate" if abs(self.correlation) < 0.7 else "Strong"

        result_message = f"Spearman's Rank Correlation Coefficient: {self.correlation:.4f}\n"
        result_message += f"Type: {correlation_type} correlation\n"
        result_message += f"Strength: {strength}"

        self.display_message(result_message)
        self.plot_graph(x, y, self.correlation)

    def display_message(self, message):
        self.result_text.setPlainText(message)

    def plot_graph(self, x, y, correlation):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.scatter(x, y)
        ax.set_xlabel('X Values')
        ax.set_ylabel('Y Values')
        ax.set_title(f"Scatter Plot (Correlation: {correlation:.4f})")
        self.canvas.draw()

    def export_graph(self):
        if self.correlation is None:
            QMessageBox.warning(self, "No Data", "Please calculate the correlation before exporting the graph.")
            return

        # Prompt user for the title, x-label, and y-label
        title, ok_title = QInputDialog.getText(self, 'Graph Title', 'Enter the title for the graph:', text=f"Scatter Plot (Correlation: {self.correlation:.4f})")
        if not ok_title:
            return  # User canceled the input dialog

        x_label, ok_x_label = QInputDialog.getText(self, 'X-Axis Label', 'Enter the label for the X-axis:', text='X Values')
        if not ok_x_label:
            return  # User canceled the input dialog

        y_label, ok_y_label = QInputDialog.getText(self, 'Y-Axis Label', 'Enter the label for the Y-axis:', text='Y Values')
        if not ok_y_label:
            return  # User canceled the input dialog

        # Ask if the user wants to add a trend line
        trend_line = QMessageBox.question(self, 'Trend Line', 'Do you want to include a trend line in the graph?', 
                                          QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        file_path, _ = QFileDialog.getSaveFileName(self, "Save Graph", "", "PNG Files (*.png)")
        if file_path:
            dpi = 300  # Set DPI to 300 for high quality graph
            fig = plt.figure(figsize=(12, 9), dpi=dpi)
            ax = fig.add_subplot(111)
            ax.scatter(self.x, self.y)
            ax.set_xlabel(x_label, fontsize=14)
            ax.set_ylabel(y_label, fontsize=14)
            ax.set_title(title, fontsize=16)
            ax.tick_params(axis='both', which='major', labelsize=12)
            
            if trend_line == QMessageBox.Yes:
                # Add a trend line using a least squares fit (linear regression)
                z = np.polyfit(self.x, self.y, 1)
                p = np.poly1d(z)
                ax.plot(self.x, p(self.x), "r-", alpha=0.75, label=f'Trend Line: y={z[0]:.2f}x+{z[1]:.2f}')
                
                # Add R-squared value to the plot for better understanding of the fit quality
                y_fit = p(self.x)
                ss_res = np.sum((self.y - y_fit) ** 2)
                ss_tot = np.sum((self.y - np.mean(self.y)) ** 2)
                r_squared = 1 - (ss_res / ss_tot)
                ax.text(0.05, 0.95, f'$R^2 = {r_squared:.3f}$', transform=ax.transAxes, fontsize=14,
                        verticalalignment='top', bbox=dict(boxstyle='round,pad=0.5', edgecolor='black', facecolor='white'))

                # Add a legend
                ax.legend(loc='best', fontsize=12)
            
            # Add grid lines
            ax.grid(True, linestyle='--', alpha=0.7)
            
            # Adjust layout and save
            plt.tight_layout()
            fig.savefig(file_path, dpi=dpi, bbox_inches='tight')
            plt.close(fig)
            QMessageBox.information(self, "Export Successful", f"Graph saved to {file_path}")

    def export_results(self):
        if self.correlation is None:
            QMessageBox.warning(self, "No Data", "Please calculate the correlation before exporting the results.")
            return
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Results as CSV", "", "CSV Files (*.csv)")
        if file_path:
            with open(file_path, 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(['X', 'Y'])
                for x, y in zip(self.x, self.y):
                    csv_writer.writerow([x, y])
                csv_writer.writerow([])
                csv_writer.writerow(['Spearman\'s Rank Correlation Coefficient', self.correlation])
            QMessageBox.information(self, "Export Successful", f"Results saved to {file_path}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = SpearmanCalculator()
    calc.show()
    sys.exit(app.exec_())
