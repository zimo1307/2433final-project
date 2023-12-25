from flask import Flask, render_template, request, redirect, url_for
from access_database import print_table_info, operating_mydatabase
from config import get_config_dict
from price_caculator import calculating_price, get_data_input

# Load configuration
config_path = "C:\\zqhome\\NYU Course\\DBS\\FinalProject\\code\\config.yaml"
config = get_config_dict(config_path)
all_tables = print_table_info(config, print_type='show_tables')

def retrive_table_data(request):
   result=request.form
   table_name = result['table_name']
   col_names = print_table_info(config, print_type='show_col', table_name=table_name)
   data = print_table_info(config, table_name=table_name)
   return result,table_name, col_names,data

app = Flask(__name__)

@app.route('/')
def index():
   # Redirect to the main page
   return redirect(url_for('main_page'))

@app.route('/main_page')
def main_page():
   # Display the main page with table names
   return render_template("main_page.html", table_names=all_tables)

@app.route('/questionnaire', methods=['GET'])
def questionnaire():
   return render_template("questionnaire.html")

@app.route('/questionnaire/1', methods=['POST'])
def calculate_insurance_price():
   customer_input = request.form
   price = calculating_price(get_data_input(customer_input))[0]
   return render_template("result.html", result=customer_input, price=price)

@app.route('/table_info', methods=['POST'])
def show_table_info():
   # Show information for a specific table
   result, table_name, col_names, data=retrive_table_data(request=request)
   return render_template("table_info.html", table_name=table_name, col_names=col_names, data=data)

@app.route('/operation', methods=['POST', 'GET'])
def perform_operation():
   # Perform specific operations on tables
   if request.method == 'GET':
      return redirect(url_for('main_page'))
   else:
      result, table_name, col_names, data=retrive_table_data(request=request)
      operation_name = result['operation']
      return render_template(f"{operation_name}.html", table_name=table_name, col_names=col_names, data=data, operation_name=operation_name)

@app.route('/success', methods=['POST'])
def execute_operation():
   result, table_name, col_names, data=retrive_table_data(request=request)
   query = operating_mydatabase(config, col_names=col_names, input_value=result, data=data, operation=result["operation_name"])
   return render_template("operate_succ.html", result=result, query=query)

@app.route('/success/1', methods=['GET'])
def operation_success():
   # Redirect to the main page after successful operation
   return redirect(url_for('main_page'))

if __name__ == '__main__':
   app.run(debug=True)
