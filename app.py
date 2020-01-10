from flask import Flask, request
from flask_cors import CORS, cross_origin

import algorithms

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


def json_parse(data):
    start_inds = data['start']
    end_inds = data['end']
    matrix = data['matrix']
    return matrix, start_inds, end_inds


"""
    Json keys:
     'start' - array of start point indices ([0, 0])
     'end' - array of end point indices ([10, 10])
     'matrix' - 2-d array representation of the field ([[1, 2] [3, 4]])
     
    Possible matrix values:
    1 - ordinary point
    2 - sea point (2x slower)
    4 - swamp point (4x slower)
    [x, y] - pair of portal indices
    -1 - forbidden point (block)
"""


@app.route('/matrix', methods=['GET', 'POST'])
@cross_origin()
def matrix_handler():
    if request.method == 'POST':
        data = request.get_json()
        matrix, start_inds, end_inds = json_parse(data)
        print(matrix)
        res_path = algorithms.Astar(matrix, start_inds, end_inds)
        return {"path": res_path}


if __name__ == '__main__':
    app.run(port=5000)
