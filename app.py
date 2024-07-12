from flask import Flask, request, jsonify
from pyXSteam.XSteam import XSteam

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Enthalpy Calculation API!"

@app.route('/enthalpy', methods=['POST'])
def calculate_enthalpy():
    try:
        data = request.get_json()
        pressure = float(data['pressure'])
        temperature = float(data['temperature'])

        steamTable = XSteam(XSteam.UNIT_SYSTEM_MKS)

        enthalpy_in_KJKg = steamTable.h_pt(pressure, temperature)
        enthalpy_in_KcalKg = enthalpy_in_KJKg / 4.184

        # Format enthalpy values to 2 decimal places
        enthalpy_in_KJKg = round(enthalpy_in_KJKg, 2)
        enthalpy_in_KcalKg = round(enthalpy_in_KcalKg, 2)

        result = {
            "enthalpy_KJ_Kg": enthalpy_in_KJKg,
            "enthalpy_kcal_Kg": enthalpy_in_KcalKg
        }

        return jsonify(result), 200

    except KeyError as e:
        return jsonify({"error": f"Missing key in JSON data: {str(e)}"}), 400

    except ValueError as e:
        return jsonify({"error": f"Invalid value provided: {str(e)}"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
