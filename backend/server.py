from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://janakan:janakan@localhost/nautilux'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Intervention(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    libelle = db.Column(db.String(100))
    description = db.Column(db.String(100))
    nomIntervenant = db.Column(db.String(20))
    lieu = db.Column(db.String(20))
    dateIntervention = db.Column(db.String(40))

    def __init__(self, libelle, description, nomIntervenant, lieu, dateIntervention):
        self.libelle = libelle
        self.description = description
        self.nomIntervenant = nomIntervenant
        self.lieu = lieu
        self.dateIntervention = dateIntervention


db.create_all()


class InterventionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'libelle', 'description', 'nomIntervenant', 'lieu', 'dateIntervention')


intervention_schema = InterventionSchema()
interventions_schema = InterventionSchema(many=True)


@app.route('/interventions', methods=['POST'])
def create_intervention():
    libelle = request.json['libelle']
    description = request.json['description']
    nomIntervenant = request.json['nomIntervenant']
    lieu = request.json['lieu']
    dateIntervention = request.json['dateIntervention']

    new_intervention = Intervention(libelle, description, nomIntervenant, lieu, dateIntervention)
    db.session.add(new_intervention)
    db.session.commit()

    return intervention_schema.jsonify(new_intervention)

@app.route('/interventions', methods=['GET'])
def get_interventions():
    all_interventions = Intervention.query.all()
    result = interventions_schema.dump(all_interventions)
    return jsonify(result)

@app.route('/interventions/<id>', methods=['GET'])
def get_intervention(id):
    intervention = Intervention.query.get(id)
    return intervention_schema.jsonify(intervention)

@app.route('/interventions/<id>', methods=['PUT'])
def update_task(id):
    intervention = Intervention.query.get(id)

    libelle = request.json['libelle']
    description = request.json['description']
    nomIntervenant = request.json['nomIntervenant']
    lieu = request.json['lieu']
    dateIntervention = request.json['dateIntervention']

    intervention.libelle = libelle
    intervention.description = description
    intervention.nomIntervenant = nomIntervenant
    intervention.lieu = lieu
    intervention.dateIntervention = dateIntervention

    db.session.commit()
    return intervention_schema.jsonify(intervention)

@app.route('/interventions/<id>', methods=['DELETE'])
def delete_intervention(id):
    intervention = Intervention.query.get(id)
    db.session.delete(intervention)
    db.session.commit()

    return intervention_schema.jsonify(intervention)

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Bienvenue sur mon API'})

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
