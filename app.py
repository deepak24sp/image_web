from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

app = Flask(__name__)

df = pd.read_excel("chunk_9 1.xlsx")
range_index = []
current_index = 0

@app.route("/", methods=["GET", "POST"])
def start():
    global range_index, current_index
    if request.method == "POST":
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
        # 🚀 Immediately save after each input
        df.to_excel("chunk_9 1.xlsx", index=False)
        current_index += 1
        return redirect(url_for("process"))

    return render_template("index.html", image_url=row["IMAGE URL"], row=row.to_dict(), row_number=row_idx)

if __name__ == "__main__":
    app.run(debug=True)
