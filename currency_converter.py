import sys
import os
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QComboBox,
    QPushButton, QVBoxLayout, QMessageBox
)
from PyQt5.QtGui import QIcon

# === YOUR API KEY ===
API_KEY = "68ddbe451f2edabffb807336"
API_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD"

# === Mapping currency to country code for flags ===
currency_to_country = {
    "USD": "US", "EUR": "EU", "GBP": "GB", "JPY": "JP", "CAD": "CA",
    "AUD": "AU", "CHF": "CH", "CNY": "CN", "INR": "IN", "ZAR": "ZA",
    "NGN": "NG", "BRL": "BR", "RUB": "RU", "KRW": "KR", "SGD": "SG",
    "SEK": "SE", "NOK": "NO", "MXN": "MX", "NZD": "NZ", "HKD": "HK"
}

# === Downloads flag icon if not already present ===
def download_flag(currency_code):
    country_code = currency_to_country.get(currency_code)
    if not country_code:
        return None

    flag_url = f"https://flagcdn.com/w40/{country_code.lower()}.png"
    flag_path = os.path.join("flags", f"{currency_code}.png")

    if not os.path.exists("flags"):
        os.makedirs("flags")

    if not os.path.isfile(flag_path):
        try:
            r = requests.get(flag_url)
            if r.status_code == 200:
                with open(flag_path, "wb") as f:
                    f.write(r.content)
        except Exception as e:
            print(f"Failed to download flag for {currency_code}: {e}")

    return flag_path if os.path.exists(flag_path) else None


# === Main App Class ===
class CurrencyConverter(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Currency Converter")
        self.setGeometry(100, 100, 300, 200)

        self.amount_input = QLineEdit(self)
        self.amount_input.setPlaceholderText("Enter amount")

        self.from_currency = QComboBox(self)
        self.to_currency = QComboBox(self)

        self.result_label = QLabel("Converted amount: ", self)

        self.convert_button = QPushButton("Convert", self)
        self.convert_button.clicked.connect(self.convert_currency)

        layout = QVBoxLayout()
        layout.addWidget(self.amount_input)
        layout.addWidget(QLabel("From:"))
        layout.addWidget(self.from_currency)
        layout.addWidget(QLabel("To:"))
        layout.addWidget(self.to_currency)
        layout.addWidget(self.convert_button)
        layout.addWidget(self.result_label)

        self.setLayout(layout)

        self.load_currencies()

    def load_currencies(self):
        try:
            response = requests.get(API_URL)
            data = response.json()
            if data["result"] == "success":
                currencies = list(data["conversion_rates"].keys())
                for code in currencies:
                    flag_path = download_flag(code)
                    icon = QIcon(flag_path) if flag_path else QIcon()
                    self.from_currency.addItem(icon, code)
                    self.to_currency.addItem(icon, code)
            else:
                self.show_error("Failed to fetch currencies.")
        except Exception as e:
            self.show_error(str(e))

    def convert_currency(self):
        amount = self.amount_input.text()
        try:
            amount = float(amount)
        except ValueError:
            self.show_error("Invalid amount")
            return

        from_cur = self.from_currency.currentText()
        to_cur = self.to_currency.currentText()

        try:
            url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{from_cur}"
            response = requests.get(url)
            data = response.json()
            if data["result"] == "success":
                rate = data["conversion_rates"].get(to_cur)
                if rate:
                    converted = amount * rate
                    self.result_label.setText(f"Converted amount: {converted:.2f} {to_cur}")
                else:
                    self.show_error(f"Rate for {to_cur} not found.")
            else:
                self.show_error("Conversion failed.")
        except Exception as e:
            self.show_error(str(e))

    def show_error(self, message):
        QMessageBox.critical(self, "Error", message)


# === Run the App ===
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CurrencyConverter()
    window.show()
    sys.exit(app.exec_())
