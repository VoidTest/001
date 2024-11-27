from flask import Flask, render_template, request, redirect
from data import pievienot_lietotaju, iegut_lietotajus, pievienot_zinu, iegut_zinas, iegut_statistiku

app = Flask(__name__)

@app.route("/")
def index():
    return redirect("/registre")

@app.route("/registre", methods=["GET", "POST"])
def registre():
    error = None
    if request.method == "POST":
        vards = request.form.get("vards", "").capitalize()
        uzvards = request.form.get("uzvards", "").capitalize()
        lietotajvards = request.form.get("lietotajvards", "").lower()

        if not vards or not uzvards or not lietotajvards:
            error = "Visi lauki ir jāaizpilda!"
        else:
            result = pievienot_lietotaju(vards, uzvards, lietotajvards)
            if result == "Šāds lietotājvārds jau eksistē.":
                error = result
            else:
                return redirect("/registre")
    lietotaji = iegut_lietotajus()
    return render_template("registre.html", lietotaji=lietotaji, error=error)

@app.route("/zinas", methods=["GET", "POST"])
def zinas():
    error = None
    lietotaji = iegut_lietotajus()
    if request.method == "POST":
        lietotaja_id = request.form.get("lietotajs")
        zina = request.form.get("zina", "")
        if not lietotaja_id or not zina.strip():
            error = "Visi lauki ir jāaizpilda!"
        else:
            result = pievienot_zinu(lietotaja_id, zina)
            if result != "Ziņa pievienota veiksmīgi.":
                error = result
            else:
                return redirect("/zinas")
    zinas = iegut_zinas()
    return render_template("zinas.html", lietotaji=lietotaji, zinas=zinas, error=error)

@app.route("/statistika")
def statistika():
    statistika = iegut_statistiku()
    return render_template("statistika.html", statistika=statistika)

if __name__ == "__main__":
    app.run(debug=True)
