from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime, timedelta
import networkx as nx
from transformers import pipeline
import os

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mysql+pymysql://root:password@localhost/socialdb')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

sentiment_analyzer = pipeline("sentiment-analysis")

class User(db.Model):
    __tablename__ = 'User '
    UserID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100))
    Email = db.Column(db.String(100), unique=True)
    Age = db.Column(db.Integer)
    Gender = db.Column(db.String(10))
    Location = db.Column(db.String(100))

class Post(db.Model):
    __tablename__ = 'Post'
    PostID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('User .UserID'))
    Content = db.Column(db.Text)
    Timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    SentimentScore = db.Column(db.Float)

class Follow(db.Model):
    __tablename__ = 'Follow'
    FollowerID = db.Column(db.Integer, db.ForeignKey('User .UserID'), primary_key=True)
    FollowingID = db.Column(db.Integer, db.ForeignKey('User .UserID'), primary_key=True)
    Timestamp = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        users = User.query.all()
        return jsonify([{
            'User ID': u.UserID,
            'Name': u.Name,
            'Email': u.Email,
            'Age': u.Age,
            'Gender': u.Gender,
            'Location': u.Location
        } for u in users])
    else:
        data = request.json
        user = User(
            Name=data['Name'],
            Email=data['Email'],
            Age=data.get('Age'),
            Gender=data.get('Gender'),
            Location=data.get('Location')
        )
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'User  created', 'User ID': user.UserID}), 201

@app.route('/posts', methods=['GET', 'POST'])
def posts():
    if request.method == 'GET':
        posts = Post.query.all()
        return jsonify([{
            'PostID': p.PostID,
            'User ID': p.UserID,
            'Content': p.Content,
            'Timestamp': p.Timestamp.isoformat(),
            'SentimentScore': p.SentimentScore
        } for p in posts])
    else:
        data = request.json
        content = data['Content']
        sentiment = sentiment_analyzer(content)[0]
        score = sentiment['score'] if sentiment['label'] == 'POSITIVE' else -sentiment['score']
        post = Post(
            UserID=data['User ID'],
            Content=content,
            SentimentScore=score,
            Timestamp=datetime.utcnow()
        )
        db.session.add(post)
        db.session.commit()
        return jsonify({'message': 'Post created', 'PostID': post.PostID}), 201

@app.route('/communities/detect', methods=['GET'])
def detect_communities():
    follows = Follow.query.all()
    G = nx.Graph()
    for f in follows:
        G.add_edge(f.FollowerID, f.FollowingID)
    communities = list(nx.algorithms.community.greedy_modularity_communities(G))
    result = []
    for i, community in enumerate(communities):
        result.append({
            'CommunityID': i,
            'Members': list(community)
        })
    return jsonify(result)

@app.route('/influence/analyze', methods=['GET'])
def influence_analysis():
    follows = Follow.query.all()
    G = nx.DiGraph()
    for f in follows:
        G.add_edge(f.FollowerID, f.FollowingID)
    pagerank = nx.pagerank(G)
    return jsonify(pagerank)

@app.route('/links/predict', methods=['GET'])
def link_prediction():
    follows = Follow.query.all()
    G = nx.Graph()
    for f in follows:
        G.add_edge(f.FollowerID, f.FollowingID)
    preds = []
    preds_gen = nx.jaccard_coefficient(G)
    for u, v, p in preds_gen:
        preds.append({'User 1ID': u, 'User 2ID': v, 'PredictionScore': p})
    preds = sorted(preds, key=lambda x: x['PredictionScore'], reverse=True)[:10]
    return jsonify(preds)

@app.route('/anomalies/detect', methods=['GET'])
def anomaly_detection():
    one_hour_ago = datetime.utcnow() - timedelta(hours=1)
    posts = Post.query.filter(Post.Timestamp >= one_hour_ago).all()
    user_post_counts = {}
    for p in posts:
        user_post_counts[p.UserID] = user_post_counts.get(p.UserID, 0) + 1
    suspicious = []
    threshold = 5
    for user_id, count in user_post_counts.items():
        if count > threshold:
            suspicious.append({
                'User ID': user_id,
                'ActivityType': 'High Post Frequency',
                'Score': count,
                'DetectedOn': datetime.utcnow().isoformat()
            })
    return jsonify(suspicious)

if __name__ == '__main__':
    app.run(debug=True)