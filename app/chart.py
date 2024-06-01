import sys

from PyQt5.QtChart import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

x_data = [("Serie 1", 20), ("Serie 1", 50), ("Serie 1", 30)]


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.centralwidget = QWidget(self)
        self.setWindowTitle("PyQt")
        self.chart = QChart()
        self.chart_view = QChartView(self.chart)

        layout = QVBoxLayout()
        layout.addWidget(self.chart_view)
        self.centralwidget.setLayout(layout)

        series = QPieSeries()

        for label, value in x_data:
            series.append(label, value)
        self.chart.addSeries(series)

        self.customize_chart()
        self.show()

    def customize_chart(self):
        self.chart.setTitle("Pie")

        for data in self.chart.series()[0].slices():
            data.setLabel(data.label())
            data.setColor(QColor("lightblue"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
