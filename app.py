from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import datetime

app = Flask(__name__)

# Global in-memory task list
columns = ['Description', 'Deadline', 'Completed']
df = pd.DataFrame(columns=columns)

@app.route('/')
def index():
    global df
    if not df.empty:
        # Ensure 'Deadline' is datetime
        df['Deadline'] = pd.to_datetime(df['Deadline'], errors='coerce')
        df_sorted = df.sort_values('Deadline')
        df_display = df_sorted.copy()
        df_display['Deadline'] = df_display['Deadline'].dt.strftime('%d-%m-%Y')
    else:
        df_display = df.copy()

    return render_template('index.html', tasks=df_display.to_dict(orient='records'))

@app.route('/add', methods=['POST'])
def add_task():
    global df
    description = request.form.get('description')
    deadline = request.form.get('deadline')

    try:
        deadline_date = datetime.datetime.strptime(deadline, "%Y-%m-%d")
        new_task = pd.DataFrame({
            'Description': [description],
            'Deadline': [deadline_date],
            'Completed': [False]
        })
        df = pd.concat([df, new_task], ignore_index=True)
    except ValueError:
        pass  # Invalid date input, silently ignore or handle as needed

    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>')
def mark_complete(task_id):
    global df
    if 0 <= task_id < len(df):
        df.at[task_id, 'Completed'] = True
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
