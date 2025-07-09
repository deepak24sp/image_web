from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd

app = Flask(__name__)
app.secret_key = "supersecretkey"  # needed for session

df = pd.read_excel("chunk_9 1.xlsx")
range_index = []
current_index = 0
empty_index = 0
empty_rows = []

@app.route("/", methods=["GET", "POST"])
def start():
    global range_index, current_index, empty_index, empty_rows
    if request.method == "POST":
        if "from_row" in request.form:
            from_row = max(int(request.form["from_row"]) - 2, 0)
            to_row = max(int(request.form["to_row"]) - 2, 0)
            range_index = list(range(from_row, to_row + 1))
            current_index = 0
            return redirect(url_for("process"))
    return render_template("start.html")

@app.route("/process", methods=["GET", "POST"])
def process():
    global range_index, current_index, df

    if current_index >= len(range_index):
        return render_template("done.html")

    row_idx = range_index[current_index]
    row = df.iloc[row_idx]

    if request.method == "POST":
        comment = request.form["comment"]
        df.at[row_idx, "REASON"] = comment
        df.to_excel("chunk_9 1.xlsx", index=False)
        current_index += 1
        return redirect(url_for("process"))

    return render_template("index.html", image_url=row["IMAGE URL"], row=row.to_dict(), row_number=row_idx + 2)

@app.route("/process_empty", methods=["POST"])
def process_empty():
    global empty_rows, empty_index
    empty_rows = [i for i, row in df.iterrows() if pd.isna(row["REASON"]) or str(row["REASON"]).strip() == ""]
    empty_index = 0
    return redirect(url_for("process_empty_step"))

@app.route("/process_empty_step", methods=["GET", "POST"])
def process_empty_step():
    global empty_rows, empty_index, df

    if empty_index >= len(empty_rows):
        return render_template("done.html")

    row_idx = empty_rows[empty_index]
    row = df.iloc[row_idx]

    if request.method == "POST":
        comment = request.form["comment"]
        df.at[row_idx, "REASON"] = comment
        df.to_excel("chunk_9 1.xlsx", index=False)
        empty_index += 1
        return redirect(url_for("process_empty_step"))

    return render_template("index.html", image_url=row["IMAGE URL"], row=row.to_dict(), row_number=row_idx + 2)

if __name__ == "__main__":
    app.run(debug=True)
