import sys
import json
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QComboBox, QTabWidget, QFormLayout, QListWidget, QListWidgetItem, QMessageBox

class Settings:
    def __init__(self, printer_price=None, electricity_price=None, materials=None):
        self.printer_price = printer_price
        self.electricity_price = electricity_price
        self.materials = materials if materials else []

    def to_dict(self):
        return {
            "printer_price": self.printer_price,
            "electricity_price": self.electricity_price,
            "materials": [{"name": m.name, "price_per_kg": m.price_per_kg} for m in self.materials]
        }

    @classmethod
    def from_dict(cls, data):
        materials = [Material(m['name'], m['price_per_kg']) for m in data.get('materials', [])]
        return cls(
            printer_price=data.get("printer_price"),
            electricity_price=data.get("electricity_price"),
            materials=materials
        )

class Material:
    def __init__(self, name, price_per_kg):
        self.name = name
        self.price_per_kg = price_per_kg

    def __str__(self):
        return f'{self.name} - {self.price_per_kg:.2f} BGN/kg'

class PrintCostCalculator(QWidget):
    def __init__(self, settings):
        super().__init__()

        self.settings = settings
        self.initUI()

    def initUI(self):
        self.setWindowTitle('3D Print Cost Calculator')

        self.tabs = QTabWidget()

        self.main_tab = QWidget()
        self.create_main_tab()

        self.settings_tab = QWidget()
        self.create_settings_tab()

        self.tabs.addTab(self.main_tab, "Main")
        self.tabs.addTab(self.settings_tab, "Settings")

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)

        self.setLayout(main_layout)

    def create_main_tab(self):
        self.material_label = QLabel('Select Material:', self.main_tab)
        self.material_combo = QComboBox(self.main_tab)
        self.update_material_combo()

        self.weight_label = QLabel('Weight (grams):', self.main_tab)
        self.weight_input = QLineEdit(self.main_tab)

        self.time_label = QLabel('Print Time (hours):', self.main_tab)
        self.time_input = QLineEdit(self.main_tab)

        self.margin_label = QLabel('Profit Margin (%):', self.main_tab)
        self.margin_input = QLineEdit(self.main_tab)

        self.additional_cost_label = QLabel('Additional Cost (BGN):', self.main_tab)
        self.additional_cost_input = QLineEdit(self.main_tab)
        self.additional_cost_input.setPlaceholderText('Optional')

        self.calculate_button = QPushButton('Calculate Cost', self.main_tab)
        self.calculate_button.clicked.connect(self.calculate_cost)

        self.result_label = QLabel('Total Cost:', self.main_tab)

        vbox = QVBoxLayout()
        vbox.addWidget(self.material_label)
        vbox.addWidget(self.material_combo)
        vbox.addWidget(self.weight_label)
        vbox.addWidget(self.weight_input)
        vbox.addWidget(self.time_label)
        vbox.addWidget(self.time_input)
        vbox.addWidget(self.margin_label)
        vbox.addWidget(self.margin_input)
        vbox.addWidget(self.additional_cost_label)
        vbox.addWidget(self.additional_cost_input)
        vbox.addWidget(self.calculate_button)
        vbox.addWidget(self.result_label)

        self.main_tab.setLayout(vbox)

    def create_settings_tab(self):
        self.printer_price_label = QLabel('Printer Price (BGN):', self.settings_tab)
        self.printer_price_input = QLineEdit(self.settings_tab)
        if self.settings.printer_price:
            self.printer_price_input.setText(str(self.settings.printer_price))

        self.electricity_price_label = QLabel('Electricity Price (BGN per kWh):', self.settings_tab)
        self.electricity_price_input = QLineEdit(self.settings_tab)
        if self.settings.electricity_price:
            self.electricity_price_input.setText(str(self.settings.electricity_price))

        self.material_name_label = QLabel('Material Name:', self.settings_tab)
        self.material_name_input = QLineEdit(self.settings_tab)

        self.material_price_label = QLabel('Material Price per kg (BGN):', self.settings_tab)
        self.material_price_input = QLineEdit(self.settings_tab)

        self.add_material_button = QPushButton('Add Material', self.settings_tab)
        self.add_material_button.clicked.connect(self.add_material)

        self.edit_material_button = QPushButton('Edit Material', self.settings_tab)
        self.edit_material_button.clicked.connect(self.edit_material)

        self.delete_material_button = QPushButton('Delete Material', self.settings_tab)
        self.delete_material_button.clicked.connect(self.delete_material)

        self.save_settings_button = QPushButton('Save Settings', self.settings_tab)
        self.save_settings_button.clicked.connect(self.save_settings)

        self.materials_list_widget = QListWidget(self.settings_tab)
        self.update_material_list()

        form_layout = QFormLayout()
        form_layout.addRow(self.printer_price_label, self.printer_price_input)
        form_layout.addRow(self.electricity_price_label, self.electricity_price_input)
        form_layout.addRow(self.material_name_label, self.material_name_input)
        form_layout.addRow(self.material_price_label, self.material_price_input)
        form_layout.addRow(self.add_material_button)
        form_layout.addRow(self.edit_material_button)
        form_layout.addRow(self.delete_material_button)
        form_layout.addRow(QLabel("Added Materials:"))
        form_layout.addRow(self.materials_list_widget)
        form_layout.addRow(self.save_settings_button)

        self.settings_tab.setLayout(form_layout)

    def update_material_combo(self):
        """ Обновяване на QComboBox с наличните материали """
        self.material_combo.clear()
        for material in self.settings.materials:
            self.material_combo.addItem(material.name)

    def update_material_list(self):
        """ Обновяване на QListWidget с наличните материали """
        self.materials_list_widget.clear()
        for material in self.settings.materials:
            item = QListWidgetItem(str(material))
            self.materials_list_widget.addItem(item)

    def add_material(self):
        name = self.material_name_input.text().strip()
        if not name or not self.material_price_input.text():
            self.result_label.setText('Please provide valid material name and price.')
            return

        try:
            price = float(self.material_price_input.text())
        except ValueError:
            self.result_label.setText('Invalid price format.')
            return

        new_material = Material(name, price)
        self.settings.materials.append(new_material)

        self.update_material_combo()
        self.update_material_list()

        self.material_name_input.clear()
        self.material_price_input.clear()

        self.save_settings()

    def edit_material(self):
        current_row = self.materials_list_widget.currentRow()
        if current_row == -1:
            QMessageBox.warning(self, "Warning", "Please select a material to edit.")
            return

        name = self.material_name_input.text().strip()
        if not name or not self.material_price_input.text():
            self.result_label.setText('Please provide valid material name and price.')
            return

        try:
            price = float(self.material_price_input.text())
        except ValueError:
            self.result_label.setText('Invalid price format.')
            return

        self.settings.materials[current_row].name = name
        self.settings.materials[current_row].price_per_kg = price

        self.update_material_combo()
        self.update_material_list()

        self.material_name_input.clear()
        self.material_price_input.clear()

        self.save_settings()

    def delete_material(self):
        current_row = self.materials_list_widget.currentRow()
        if current_row == -1:
            QMessageBox.warning(self, "Warning", "Please select a material to delete.")
            return

        del self.settings.materials[current_row]

        self.update_material_combo()
        self.update_material_list()

        self.save_settings()

    def save_settings(self):
        self.settings.printer_price = float(self.printer_price_input.text()) if self.printer_price_input.text() else None
        self.settings.electricity_price = float(self.electricity_price_input.text()) if self.electricity_price_input.text() else None

        with open('settings.json', 'w') as f:
            json.dump(self.settings.to_dict(), f)

    def calculate_cost(self):
        if not self.settings.materials:
            self.result_label.setText('No materials available. Please add materials in settings.')
            return

        material_index = self.material_combo.currentIndex()

        if material_index < 0 or material_index >= len(self.settings.materials):
            self.result_label.setText('Selected material is not valid.')
            return

        selected_material = self.settings.materials[material_index]

        if self.settings.printer_price is None:
            self.result_label.setText('Printer price is not set. Please set it in the settings tab.')
            return

        weight = float(self.weight_input.text()) / 1000 
        time = float(self.time_input.text())
        margin = float(self.margin_input.text()) / 100

        printer_hours = 20 * 8 * 12 * 2  
        printer_depreciation = (self.settings.printer_price / printer_hours) * 1.15

        material_cost = weight * (selected_material.price_per_kg * 1.15)

        electricity_cost = time * self.settings.electricity_price

        production_cost = material_cost + electricity_cost + (printer_depreciation * time)

        final_price = production_cost * (1 + margin)

        if self.additional_cost_input.text():
            try:
                additional_cost = float(self.additional_cost_input.text())
                final_price += additional_cost
            except ValueError:
                self.result_label.setText('Invalid additional cost format.')
                return

        self.result_label.setText(f'Total Cost: {final_price:.2f} BGN')

def load_settings():
    try:
        with open('settings.json', 'r') as f:
            data = json.load(f)
            return Settings.from_dict(data)
    except FileNotFoundError:
        return Settings()

def main():
    app = QApplication(sys.argv)

    settings = load_settings()

    calc = PrintCostCalculator(settings)
    calc.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
