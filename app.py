from flask import Flask, request
from flask_cors import CORS, cross_origin

import algorithms
import time

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


def json_parse(data):
    start_inds = data['start']
    end_inds = data['end']
    matrix = data['matrix']
    return matrix, tuple(start_inds), tuple(end_inds)


"""
    Json keys:
     'start' - array of start point indices ([0, 0])
     'end' - array of end point indices ([10, 10])
     'matrix' - 2-d array representation of the field ([[1, 2] [3, 4]])
     
    Possible matrix values:
    1 - ordinary point
    2 - swamp point (2x slower)
    4 - sea point (4x slower)
    [y, x] - pair of portal indices
    -1 - forbidden point (block)
"""

@app.route('/matrix', methods=['GET', 'POST'])
@cross_origin()
def matrix_handler():
    if request.method == 'POST':
        data = request.get_json()
        alg_str, metric_str = request.args.get('alg'), request.args.get('metric')
        matrix, start_inds, end_inds = json_parse(data)

        if alg_str == 'dijkstra':
            alg = algorithms.Dijkstra
        elif alg_str == 'astar':
            alg = algorithms.astar
        elif alg_str == 'bf':
            alg = algorithms.best_first

        if metric_str == 'manhattan':
            metric = algorithms.manhattan_dist
        elif metric_str == 'euclid':
            metric = algorithms.euclidean_dist

        start = time.time()
        (res_paths, length) = alg(matrix, start_inds, end_inds, metric)
        end = time.time()

        final_path = []
        for row in res_paths:
            path = [(x, y) for y, x in row]
            final_path.append(path)
        print(final_path)
        res_time = int((end - start) * 1000)
        return {"paths": final_path, "length": length, "time": res_time}


if __name__ == '__main__':
    app.run(port=5000)
