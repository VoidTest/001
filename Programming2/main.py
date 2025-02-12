from flask import Flask, request, render_template, jsonify
import requests, random

# Initialize Flask and explicitly set the template folder
app = Flask(__name__, template_folder='templates')

# Global variable that tracks whether the blue state is active (True = blue; False = not blue)
global_blue_state = False

def update_blue_state(new_state=None):
    global global_blue_state
    if new_state is not None:
        global_blue_state = bool(new_state)
    return global_blue_state

@app.route("/", methods=["POST", "GET"])
def index():
    # Get a random joke and categories from the Chuck Norris API
    response = requests.get("https://api.chucknorris.io/jokes/random")
    joke_data = response.json()
    response = requests.get("https://api.chucknorris.io/jokes/categories")
    categories = response.json()
    
    if request.method == "POST":
        search = request.form.get("search", "").strip()
        if search:
            try:
                response = requests.get(f"https://api.chucknorris.io/jokes/search?query={search}")
                search_data = response.json()
                total = search_data.get("total", 0)
                if total > 0:
                    random_index = random.randint(0, total - 1)
                    joke_text = search_data["result"][random_index]["value"]
                else:
                    joke_text = "No jokes found for your search."
                return render_template("index.html", joks=joke_text, kategorijas=categories)
            except Exception:
                return render_template("index.html", joks="Invalid search", kategorijas=categories)
        else:
            category = request.form.get("kat")
            if category:
                response = requests.get(f"https://api.chucknorris.io/jokes/random?category={category}")
                joke_data = response.json()
                return render_template("index.html", joks=joke_data["value"], bilde=joke_data["icon_url"], kategorijas=categories)
    
    return render_template("index.html", joks=joke_data["value"], bilde=joke_data["icon_url"], kategorijas=categories)

@app.route("/uni")
def uni():
    # Retrieve Latvian universities from the external API
    response = requests.get("http://universities.hipolabs.com/search?country=latvia")
    uni_data = response.json()
    uni_list = []
    for uni in uni_data:
        uni_list.append({
            "nosaukums": uni["name"],
            "majaslapas": uni["web_pages"]
        })
    return render_template("universitates.html", uni=uni_list)

@app.route("/jschats")
def chats():
    # Render the chat interface template
    return render_template("chats.html")

@app.route("/jschats/suutiit", methods=["POST"])
def send_chat():
    data = request.json
    message = data.get("saturs", "")
    name = data.get("vards", "")
    
    if message == "\\clear":
        with open("chataZinas.txt", "w") as f:
            f.write("")
        return "Cleared"
    elif message == "\\blue":
        update_blue_state(True)
        return jsonify({"blue": update_blue_state()})
    
    with open("chataZinas.txt", "a") as f:
        f.write(f"{name}----{message}\n")
    return jsonify("OK")

@app.route("/jschats/lasiit")
def read_chat():
    try:
        with open("chataZinas.txt", "r") as f:
            messages = f.readlines()
    except FileNotFoundError:
        messages = []
    return jsonify(messages)

@app.route("/jschats/blue")
def blue_route():
    isblue = request.args.get("isblue")
    if isblue is not None:
        # Interpret "true" (case-insensitive) as True; any other value as False.
        new_state = True if isblue.lower() == "true" else False
        update_blue_state(new_state)
    return jsonify({"blue": update_blue_state()})

if __name__ == '__main__':
    app.run(port=5000)
