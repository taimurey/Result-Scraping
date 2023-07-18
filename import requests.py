import requests
from bs4 import BeautifulSoup
import pandas as pd

base_url = 'https://result1.fbise.edu.pk/STATIC_PAGES_SSC_23A/'

# List to store all the results
all_data = []

for roll_no in range(9806581, 9806617):  # adjust the range as needed
    url = base_url + str(roll_no) + '.html'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    candidate_name = soup.find(
        "td", text="Candidate's Name").find_next_sibling("td").text
    result = soup.find("td", text="Result").find_next_sibling("td").text
    remarks = soup.find("td", text="Remarks").find_next_sibling("td").text

    table = soup.find_all('table')[1]
    rows = table.find_all('tr')[1:]

    subjects_marks = []
    for row in rows:
        cols = row.find_all('td')
        subject = cols[1].text
        mark = cols[2].text
        subjects_marks.append((subject, mark))

    # Create a DataFrame from the subjects and marks
    df = pd.DataFrame(subjects_marks, columns=['Subject', 'Mark'])

    # Add the roll number, candidate name, result and remarks as new columns in the DataFrame
    df['Roll No'] = roll_no
    df['Candidate Name'] = candidate_name
    df['Result'] = result
    df['Remarks'] = remarks

    # Transpose the DataFrame
    df = df.set_index('Subject').T

    # Append the data to the list
    all_data.append(df)

# Concatenate all the dataframes
all_data = pd.concat(all_data)

# Reset the index of the overall DataFrame
all_data.reset_index(drop=True, inplace=True)

# Write the DataFrame to an Excel file
all_data.to_excel('output.xlsx', index=False)
