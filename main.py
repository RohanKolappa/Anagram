from flask import Flask, render_template, request
import mysql.connector
import os

#figure out how to do error checking --> maybe try-catch block?

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/AddStrings", methods=["POST"])
def enterStrings():
    string1 = request.form["First String"].lower()
    string2 = request.form["Second String"].lower()


    db = mysql.connector.connect(user='root', password='Lablix12',
                                 host='127.0.0.1',
                                 database='anagram')
    cur = db.cursor(buffered=True)

    if string1 == string2:
        cur.execute(f"""SELECT * 
                           FROM anagram.strings 
                           WHERE (string_one = '{string1}' AND string_two = '{string2}')""")
    else:
        cur.execute(f"""SELECT * 
                    FROM anagram.strings 
                    WHERE (string_one = '{string1}' OR string_two = '{string1}')
                    AND (string_one = '{string2}' OR string_two = '{string2}')""")
    row = cur.fetchone()
    if row == None:
        flag = anagramLogic(string1, string2)
        return flag
    else:
        return row[2]

def anagramLogic(string1, string2):
    flag = False

    if sorted(string1) == sorted(string2):
        flag = True

    db = mysql.connector.connect(user='root', password='Lablix12',
                                  host='127.0.0.1',
                                  database='anagram')

    cur = db.cursor(buffered=True)


    str_flag = str(flag)

    #SQL code
    cur.execute("SELECT * FROM anagram.strings")
    cur.execute(f"""INSERT INTO strings (string_one, string_two, is_anagram_flag) VALUES ('{string1}', '{string2}', '{str_flag}')""")
    db.commit()

    db.close()
    return str_flag


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    app.run(debug=True, host='0.0.0.0', port=port) #runs the web server; debug command provides info on what is going on whenever something occurs

#pseudocode
#this python script will use flask to build an interface for the user to enter in the two strings
#once the two strings are entered and the submit button is clicked, the anagramLogic function will be run