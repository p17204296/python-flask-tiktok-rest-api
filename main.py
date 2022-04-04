from flask import Flask, abort, jsonify
from flask_restful import Api, Resource, reqparse, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy, Model

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class videoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)
    # def __repr__(self) -> str:
    #     return super().__repr__()
    def __repr__(self):
        return f"Video(name = {name}, views={views}, likes={likes})"

# -------- Hello World Example ------
# names = {"Ayo": {"age":23, "gender": "Male"},
#          "Liz": {"age":20, "gender": "Female"}
#          }
# class HelloWorld(Resource):
#     def get(self,name):
#         return names[name]

#     def post(self):
#         return {"data": "Posted!"}


# api.add_resource(HelloWorld,"/helloworld/<string:name>")


#------------Request Parser ---------

#---- Dictionary that will store all the values passed in
video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of Video")
video_put_args.add_argument("views", type=int, help="Views of Video")
video_put_args.add_argument("likes", type=int, help="Likes of Video")

#UPDATE ARGS
video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="Name of Video")
video_update_args.add_argument("views", type=int, help="Views of Video")
video_update_args.add_argument("likes", type=int, help="Likes of Video")




# ------ USED BEFRE IMPLEMENTATION OF SQLALCHEMEY DATABASE --------
# videos = {{"name": "Welcome to my YT Channel", "views": 344, "likes": 33}}
# videos = {} 

# @app.errorhandler(404)
# def resource_not_found(e):
#     return jsonify(error=str(e)), 404


# def abortNotExist(video_id):
#     if video_id not in videos:
#         abort(404, "Video ID is invalid")

# def abortIfExist(video_id):
#     if video_id in videos:
#         abort(404, "Video already exists")

# class Video(Resource):
#     def get(self, video_id):
#         abortNotExist(video_id) #Abort if the video doesn't exist
#         return videos[video_id]

#     def put(self, video_id):
#         abortIfExist(video_id)       
#         args = video_put_args.parse_args()
#         videos[video_id] = args
#         return videos[video_id], 201

#     def delete(self, video_id):
#         abortNotExist(video_id)
#         del videos[video_id]
#         return f"video ID {video_id} deleted", 204 


#----New SQLALCHEMEY DATABASE Implementation --------

resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer
}

class Video(Resource):
    #----- GET Method ------
    @marshal_with(resource_fields) #serialises the object
    def get(self, video_id):
        result = videoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, "Video ID is invalid")
        return result

    #----- PUT Method ------
    @marshal_with(resource_fields) #serialises the object
    def put(self, video_id):
        args = video_put_args.parse_args()
        result = videoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409, "Video Id already exist...")

        video = videoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
        db.session.add(video)
        db.session.commit()
        return video, 201

    #----- Patch (The UPDATE) Method ------
    @marshal_with(resource_fields) #serialises the object
    def patch(self, video_id):
        args = video_put_args.parse_args()
        result = videoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, "Video ID is invalid")
        
        if args['name']:
            result.name = args['name']
        if args['views']:
            result.views = args['views']
        if args['likes']:
            result.likes = args['likes']

        db.session.commit()
        return result


api.add_resource(Video, f"/video/<int:video_id>")


if __name__ == "__main__":
    app.run(debug=True)
