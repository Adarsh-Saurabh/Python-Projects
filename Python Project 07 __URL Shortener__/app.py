from flask import Flask, redirect, request, render_template
import hashlib
import csv

app = Flask(__name__)

# Define the name of the CSV file to store the URLs and their shortened versions
csv_filename = "url.csv"

# Define a function to generate a shortened URL using a hash function
def generate_short_url(url):
    # Use the MD5 hash function to generate a hash value for the URL
    hash_object = hashlib.md5(url.encode())
    hash_value = hash_object.hexdigest()[:6]
    # Store the original URL and the shortened URL in the CSV file
    with open(csv_filename, mode="a", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        print(hash_value, url)
        csv_writer.writerow([hash_value, url])
    return hash_value

# Define a function to redirect to the original URL from the shortened URL
def redirect_to_url(short_url):
    with open(csv_filename, mode="r") as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            if row[0] == short_url:
                return row[1]
    return "URL not found"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        original_url = request.form["url"]
        custom_url = request.form["custom_url"]
        if custom_url == "":
            custom_url = "ContloUrlShortener"
        short_url = generate_short_url(original_url)
        # print(short_url)
        return render_template("result.html", short_url=f"https://www.{custom_url}.com/{short_url}", original_url=original_url, click_url=short_url)
        # return render_template("result.html", short_url=short_url, original_url=original_url)

    else:
        return render_template("index.html")

@app.route("/<short_url>")

def redirect_to_url(short_url):
    with open(csv_filename, mode="r") as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            if row[0] == short_url:
                return redirect(row[1])
    return "URL not found"

# Add a new route to update a long URL
@app.route("/update", methods=["POST"])
def update_url():
    original_url = request.form["original_url"]
    new_url = request.form["new_url"]
    with open(csv_filename, mode="r") as csv_file:
        csv_reader = csv.reader(csv_file)
        rows = []
        for row in csv_reader:
            if row[1] == original_url:
                row[1] = new_url
            rows.append(row)
    with open(csv_filename, mode="w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(rows)
    return redirect("/")

# Add a new route to delete a short URL
@app.route("/delete/<short_url>", methods=["POST"])
def delete_url(short_url):
    # Read the CSV file and find the row to delete
    with open(csv_filename, mode="r") as csv_file:
        csv_reader = csv.reader(csv_file)
        rows = []
        row_deleted = False
        for row in csv_reader:
            if row[0] != short_url:
                rows.append(row)
            else:
                row_deleted = True

    # Write the remaining rows to the CSV file
    with open(csv_filename, mode="w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(rows)

    # Return a response based on whether the row was deleted or not
    if row_deleted:
        return "Short URL deleted successfully"
    else:
        return "Short URL not found"



if __name__ == "__main__":
    app.run(debug=True)
