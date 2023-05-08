# Technical Assignment for Software Developer CS
# Name : Abhijeet Mahto

from flask import Flask, render_template
import pandas as pd
import datetime
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__,template_folder=r'C:\Users\ababh\Desktop\templates')

@app.route('/')
def index():
    # Load data into a Pandas DataFrame
    URL = "https://rc-vault-fap-live-1.azurewebsites.net/api/gettimeentries?code=vO17RnE8vuzXzPJo5eaLLjXjmRW07law99QTD90zat9FfOQJKKUcgQ=="
    df = pd.read_json(URL)
	
	# Question 1 : Visualize JSON data via HTML table

    df['start_time'] = df['StarTimeUtc'].apply(lambda x: datetime.datetime.fromisoformat(x))
    df['end_time'] = df['EndTimeUtc'].apply(lambda x: datetime.datetime.fromisoformat(x))
    df['time_of_work'] = abs(df['end_time'] - df['start_time'])
    df['work_hours'] = (df['time_of_work']) / pd.Timedelta(hours=1)
    df_new=df[['EmployeeName','time_of_work', 'work_hours']]

    df_total=df_new.groupby(df["EmployeeName"])["work_hours"].sum()
    df_total=df_total.reset_index(name="work_hours")
    #df_total['highlighted']=df_total['work_hours']>100


			
    def color_row(df):
        if df['work_hours']< 100:
            return ['background-color: yellow']*len(df)
        else:
            return ['']*len(df)
    df_styled=df_total.style.apply(color_row,axis=1)
    # Create a pie chart of the total work hours by employee
    hours_by_employee = df_total.groupby('EmployeeName')['work_hours'].sum()

    df_table=df_styled.to_html(classes='table',index=False)

	
	# Question 2 : Visualize JSON data in a PIE Chart 

    plt.pie(hours_by_employee.values, labels=hours_by_employee.index,autopct='%1.1f%%')
    plt.title('Total Work Hours by Employee')
	

    # Save the pie chart as a PNG image
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    chart_data = base64.b64encode(buffer.read()).decode('utf-8')


    # Render the template with the DataFrame and chart attached as variables
    return render_template('my_template.html', chart_data=chart_data,table=df_table)


if __name__ == '__main__':
    app.run(debug=True)
