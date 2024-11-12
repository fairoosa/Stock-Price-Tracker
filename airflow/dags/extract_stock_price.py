from __future__ import annotations
import datetime as dt
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python_operator import PythonOperator
from bs4 import BeautifulSoup
import requests
from datetime import datetime
from airflow.hooks.mysql_hook import MySqlHook
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Template
from stock_urls import urls




def extract_stock_price(**kwargs):
    initial = False
    mysql_hook = MySqlHook(mysql_conn_id='unfold_mysql_connection')

    now = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    for stock_url in urls :
        response = requests.get(stock_url)
        soup =BeautifulSoup(response.text, 'html.parser')
        current_price1 = soup.find(id="nsecp").getText()
        current_price = current_price1.replace(',', '')
        div_element = soup.find("div", class_="inid_name")
        h1_element = div_element.find("h1")
        stock = h1_element.text.strip() 

        if initial:
            query = f"INSERT INTO unfold.stock_stock (stock, previous_price, current_price) VALUES ('{stock}',0, {current_price}, '{now}');"
        else:
            query = f"UPDATE unfold.stock_stock SET previous_price = current_price, current_price = {current_price}, updated_at = '{now}' WHERE stock = '{stock}';"
        result = mysql_hook.get_records(query)
        print(query)
    

def send_email(**kwargs):
    mysql_hook = MySqlHook(mysql_conn_id='unfold_mysql_connection')
    query = "SELECT * from unfold.stock_stock where previous_price != current_price ;"
    result = mysql_hook.get_records(query)
    print(result)
    if len(result) > 0:

    # Email configuration
        sender_email = 'fairoosa02112000@gmail.com'
        sender_password = 'klysrlbzaunljglx'
        receiver_email = '20001102fairoosa@gmail.com'
        subject = ' Stock price update '
            
        email_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                table {
                    border-collapse: collapse;
                    width: 100%;
                    font-family: Arial, sans-serif;
                }

                th, td {
                    border: 1px solid #dddddd;
                    text-align: left;
                    padding: 8px;
                }

                th {
                    background-color: #f2f2f2;
                }

                tr:nth-child(even) {
                    background-color: #f2f2f2;
                }
            </style>
        </head>
        <body>
            <h2>Stock Price Update</h2>
            <table>
                <thead>
                    <tr>
                        <th>Stock</th>
                        <th>Previous Price</th>
                        <th>Current Price</th>
                    </tr>
                </thead>
                <tbody>
                    {% for stock in stocks %}
                    <tr>
                        <td>{{ stock[1] }}</td>
                        <td>{{ stock[2] }}</td>
                        <td>{{ stock[3] }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </body>
        </html>
        """


        # Render the template with the data
        template = Template(email_template)
        html_content = template.render(stocks=result)

        # Create a multipart message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject

        # Attach the HTML content to the email
        msg.attach(MIMEText(html_content, 'html'))

        try:
            # Create a secure connection with the SMTP server
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)

            # Send the email
            server.sendmail(sender_email, receiver_email, msg.as_string())

            print('Email sent successfully!')
        except Exception as e:
            print(f'An error occurred while sending the email: {str(e)}')
        finally:
            # Close the SMTP server connection
            server.quit()


with DAG(
    dag_id="extract_stock_price2",
    schedule_interval='@once',
    start_date=dt.datetime(2023, 6, 29),
    catchup=False,
) as dag:
    first_task1 = PythonOperator(task_id="extract_store",
                                python_callable=extract_stock_price)
    second_task = PythonOperator(task_id="send_email",
                                python_callable=send_email)
                                
    first_task1 >> second_task

# '*/15 * * * *'

# def extract_stock_price1(**kwargs):
#     mysql_hook = MySqlHook(mysql_conn_id='unfold_mysql_connection')
#     stock_url = "https://www.moneycontrol.com/india/stockpricequote/trading/adanienterprises/AE13"
#     response = requests.get(stock_url)
#     soup =BeautifulSoup(response.text, 'html.parser')
#     current_price1 = soup.find(id="nsecp").getText()
#     current_price = current_price1.replace(',', '')
#     div_element = soup.find("div", class_="inid_name")
#     h1_element = div_element.find("h1")
#     stock = h1_element.text.strip() 
#     query = f"INSERT INTO unfold.stock_stock (stock, previous_price, current_price) VALUES ('{stock}',0, {current_price});"
#     result = mysql_hook.get_records(query)
#     print(query)

# Define the email template as a string
