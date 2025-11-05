from flask import Flask, render_template, request, jsonify
from collections import Counter

app = Flask(__name__)

votos = Counter({"A": 0, "B": 0, "C": 0, "D": 0})
total_votos = 0

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/votar", methods=["POST"])
def votar():
    global total_votos
    data = request.get_json()
    opcion = data.get("opcion")

    if opcion not in votos:
        return jsonify({"error": "Opción inválida"}), 400

    votos[opcion] += 1
    total_votos += 1

    return jsonify({"mensaje": "Voto registrado con éxito"})

@app.route("/resultados")
def resultados():
    if total_votos == 0:
        porcentajes = {k: 0 for k in votos}
    else:
        porcentajes = {k: round((v / total_votos) * 100, 1) for k, v in votos.items()}
    return jsonify({"total": total_votos, "porcentajes": porcentajes})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
