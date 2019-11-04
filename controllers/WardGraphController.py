from flask import Flask
import model.GraphModel as graphModel


app = Flask(__name__)

@app.route("/ward-graph/summoner/<string:summoner_name>")
def get_latest_ward_data_by_summoner_name(summoner_name):
    return graphModel.build_graph_using_summoner_name(summoner_name)

if __name__ == "__main__":
    app.run()