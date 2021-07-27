from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from flask_marshmallow import Marshmallow

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = ''
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False

db = SQLAlchemy(app)
api = Api(app)
ma = Marshmallow(app)

class Reaction(db.Model):

    __tablename__ = "reaction"

    id = db.Column(db.Integer, primary_key = True)
    ReactionID = db.Column(db.String)
    Description = db.Column(db.String)
    Formula = db.Column(db.String)
    Reversible = db.Column(db.Integer)
    ConfidenceScore = db.Column(db.Integer)
    Notes = db.Column(db.String)
    References = db.Column(db.String)
    ECNumber = db.Column(db.String)
    KEGGID = db.Column(db.String)
    LastModified = db.Column(db.String)
    Subsystem = db.Column(db.String)

    def __init__(self, ReactionID, Description, Formula, Reversible, ConfidenceScore, Notes, References, ECNumber, KEGGID, LastModified, Subsystem):
        self.ReactionID = ReactionID
        self.Description = Description
        self.Formula = Formula
        self.Reversible = Reversible
        self.ConfidenceScore = ConfidenceScore
        self.Notes = Notes
        self.References = References
        self.ECNumber = ECNumber
        self.KEGGID = KEGGID
        self.LastModified = LastModified
        self.Subsystem = Subsystem

class ReactionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Reaction

reaction_schema = ReactionSchema()
reactions_schema = ReactionSchema(many=True)

class GetDBReaction(Resource):
    def get(self):
        all_reactions = db.session.query(Reaction).all()
        result = reactions_schema.dump(all_reactions)
        return jsonify(result)

class PostDBReaction(Resource):
    def post(self):
        received = request.get_json(force=True)

        ReactionID = received['ReactionID']
        Description = received['Description']
        Formula = received['Formula']
        Reversible = received['Reversible']
        ConfidenceScore = received['ConfidenceScore']
        Notes = received['Notes']
        References = received['References']
        ECNumber = received['ECNumber']
        KEGGID = received['KEGGID']
        LastModified = received['LastModified']
        Subsystem = received['Subsystem']

        new_reaction = Reaction(ReactionID, Description, Formula, Reversible, ConfidenceScore, Notes, References, ECNumber, KEGGID, LastModified, Subsystem)

        try:
            db.session.add(new_reaction)
            db.session.commit()

            return {"message": "posted"}
        except:
            return {"message": "There was a problem posting to the database"}

class Metabolite(db.Model):

    __tablename__ = "metabolite"

    id = db.Column(db.Integer, primary_key = True)
    x0 = db.Column(db.String)
    x1 = db.Column(db.String)
    x2 = db.Column(db.String)
    x3 = db.Column(db.String)
    x4 = db.Column(db.Integer)
    x5 = db.Column(db.String)
    x6 = db.Column(db.String)
    x7 = db.Column(db.String)
    x8 = db.Column(db.String)
    x9 = db.Column(db.String)
    x10 = db.Column(db.String)
    x11 = db.Column(db.String)

    def __init__(self, x0, x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11):
        self.x0 = x0
        self.x1 = x1
        self.x2 = x2
        self.x3 = x3
        self.x4 = x4
        self.x5 = x5
        self.x6 = x6
        self.x7 = x7
        self.x8 = x8
        self.x9 = x9
        self.x10 = x10
        self.x11 = x11
    
class MetaboliteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Metabolite

metabolites_schema = MetaboliteSchema(many=True)

class GetDBMetabolite(Resource):
    def get(self):
        all_metabolites = Metabolite.query.all()
        result = metabolites_schema.dump(all_metabolites)
        return jsonify(result)

class PostDBMetabolite(Resource):
    def post(self):
        received = request.get_json(force=True)

        x0 = received['x0']
        x1 = received['x1']
        x2 = received['x2']
        x3 = received['x3']
        x4 = received['x4']
        x5 = received['x5']
        x6 = received['x6']
        x7 = received['x7']
        x8 = received['x8']
        x9 = received['x9']
        x10 = received['x10']
        x11 = received['x11']

        new_metabolite = Metabolite(x0, x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11)
        try:
            db.session.add(new_metabolite)
            db.session.commit()

            return {"message": "posted"}
        except:
            return {"message": "There was a problem posting to the database"}

api.add_resource(GetDBReaction, '/reaction')
api.add_resource(PostDBReaction, '/add_reaction')
api.add_resource(GetDBMetabolite, '/metabolite')
api.add_resource(PostDBMetabolite, '/add_metabolite')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)