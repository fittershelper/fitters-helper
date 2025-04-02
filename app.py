from flask import Flask, render_template, request, jsonify
from fractions import Fraction

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = {"offset": "", "takeout": ""}

    # Dropdown values
    nums = [str(i) for i in range(1, 11)]
    fracs = ['1/16', '1/8', '3/16', '1/4', '5/16', '3/8', '7/16',
             '1/2', '9/16', '5/8', '11/16', '3/4', '13/16', '7/8', '15/16']

    # Pre-fill dropdowns for default page load
    selected = {
        "a_num": "", "a_frac": "",
        "b_num": "", "b_frac": "",
        "c_num": "", "c_frac": ""
    }

    return render_template("index.html", nums=nums, fracs=fracs, result=result, selected=selected)


@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()

        a_num = float(data.get("a_num", 0) or 0)
        a_frac = float(Fraction(data.get("a_frac", 0) or 0))
        b_num = float(data.get("b_num", 0) or 0)
        b_frac = float(Fraction(data.get("b_frac", 0) or 0))
        c_num = float(data.get("c_num", 0) or 0)
        c_frac = float(Fraction(data.get("c_frac", 0) or 0))

        total = a_num + a_frac + b_num + b_frac + c_num + c_frac
        offset_float = round((total * 0.707) / 0.0625) * 0.0625
        takeout_float = round((offset_float + b_num + b_frac) / 0.0625) * 0.0625

        def to_mixed(value):
            whole = int(value)
            frac = Fraction(value - whole).limit_denominator(16)
            return f"{whole} {frac.numerator}/{frac.denominator}" if frac.numerator else f"{whole}"

        return jsonify({
            "offset": to_mixed(offset_float),
            "takeout": to_mixed(takeout_float)
        })

    except Exception:
        return jsonify({"offset": "Error", "takeout": "Check inputs"})


if __name__ == '__main__':
    app.run(debug=True)
