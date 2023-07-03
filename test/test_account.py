from app import create_app
import json
from pytest_check import check
from checking_response import checking_response

def test_signup_route():
    '''
    GIVEN a Flask application configured for testing
    WHEN the '/signup' page is requested (POST)
    THEN check that the response is valid
    '''
    # Set the Testing configuration prior to creating the Flask application
    flask_app = create_app({"TESTING": True})

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as test_client:
        
        #case 1 ==> with correct inputs (complete)
        with check:
            response = test_client.post('/signup', 
                                        data=json.dumps(dict(username='uzairayyy__', email='uzair@gmail.com', password='123rew', name='Uzair', bio='You are slave to your subconcious thoughts!', profile_image_url='https://wallpapercave.com/wp/wp8953915.jpg')),
                                        content_type='application/json')
            data = json.loads(response.data)
            checking_response(response, data)

        #case 2.1 ==> with correct inputs (incomplete)
        with check:
            response = test_client.post('/signup', 
                                        data=json.dumps(dict(username='ayeshahaha', email='ayesha@gmail.com', password='asshhh', name='Ayesha', profile_image_url='https://wallpapercave.com/uwp/uwp3794478.jpeg')),
                                        content_type='application/json')
            data = json.loads(response.data)
            checking_response(response, data)

        #case 2.2 ==> with correct inputs (incomplete)
        with check:
            response = test_client.post('/signup', 
                                        data=json.dumps(dict(username='_butt_jee', email='butt@gmail.com', password='revbutver', name='Butt Jee', bio='BUTTT TIGER 1')),
                                        content_type='application/json')
            data = json.loads(response.data)
            checking_response(response, data)

        #case 3 ==> with incomplete inputs
        with check:
            response = test_client.post('/signup', 
                                        data=json.dumps(dict(email='uzair@gmail.com', password='123rew', name='Uzair', profile_image_url='https://wallpapercave.com/wp/wp8953915.jpg')),
                                        content_type='application/json')
            data = json.loads(response.data)
            checking_response(response, data)

def test_login_route():
    '''
    GIVEN a Flask application configured for testing
    WHEN the '/login' page is requested (POST)
    THEN check that the response is valid
    '''
    # Set the Testing configuration prior to creating the Flask application
    flask_app = create_app({"TESTING": True})

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as test_client:
        
        #case 1 ==> with correct inputs (complete)
        with check:
            response = test_client.post('/login', 
                                        data=json.dumps(dict(username='uzairayyy__', password='123rew')),
                                        content_type='application/json')
            data = json.loads(response.data)
            checking_response(response, data)

        #case 2.1 ==> with wrong inputs (password)
        with check:
            response = test_client.post('/login', 
                                        data=json.dumps(dict(username='uzairayyy__', password='123rew321123')),
                                        content_type='application/json')
            data = json.loads(response.data)
            checking_response(response, data)

        #case 2.2 ==> with wrong inputs (username)
        with check:
            response = test_client.post('/login', 
                                        data=json.dumps(dict(username='uzairayyy__123', password='123rew')),
                                        content_type='application/json')
            data = json.loads(response.data)
            checking_response(response, data)

        #case 3.1 ==> with incomplete inputs(password)
        with check:
            response = test_client.post('/login', 
                                        data=json.dumps(dict(username='uzairayyy__')),
                                        content_type='application/json')
            data = json.loads(response.data)
            checking_response(response, data)

        #case 3.2 ==> with incomplete inputs(username)
        with check:
            response = test_client.post('/login', 
                                        data=json.dumps(dict(password='123rew')),
                                        content_type='application/json')
            data = json.loads(response.data)
            checking_response(response, data)

        #case 3.3 ==> with incomplete inputs(both)
        with check:
            response = test_client.post('/login', 
                                        data=json.dumps(dict()),
                                        content_type='application/json')
            data = json.loads(response.data)
            checking_response(response, data)

        #case 4 ==> with forgotten_password
        with check:
            response = test_client.post('/login', data=json.dumps(dict(username='uzair', passsword='', forgotten_password='True')))
            data = json.loads(response.data)
            checking_response(response, data)

# def test_update_route(reset_token):
#     '''
#     GIVEN a Flask application configured for testing
#     WHEN the '/update' page is requested (POST)
#     THEN check that the response is valid
#     '''
#     # Set the Testing configuration prior to creating the Flask application
#     flask_app = create_app({"TESTING": True})

#     # Create a test client using the Flask application configured for testing
#     with flask_app.test_client() as test_client:
        
#         #case 1 ==> with correct inputs (complete)
#         with check:
#             response = test_client.post('/update', data=json.dumps(dict(reset_token=reset_token, username='uzair', new_password='1234567'),content_type='application/json'))
#             data = json.loads(response.data)
#             checking_response(response, data)


def test_delete_route():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/delete' page is requested (DELETE)
    THEN check that the response is valid
    """
    # Set the Testing configuration prior to creating the Flask application
    flask_app = create_app({"TESTING": True})

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as test_client:
        #case 1 ==> with incorrect inputs
        with check:
            headers = {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json',
                'Authorization': ''
            }
            response = test_client.delete('/delete', headers= headers)

            data = json.loads(response.data)
            checking_response(response, data)

        #case 2  ==> with correct inputs
        with check:
            headers = {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json',
                'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4Nzc4NTExMSwianRpIjoiZjc5ZjdhOTEtYjIyMS00OTBjLWJkNjctN2Y5ZDYxNTE4MDgzIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6NSwibmJmIjoxNjg3Nzg1MTExLCJleHAiOjE2ODc3ODYwMTF9.vUjjyJzGkUU91LVrnLKSs5blkoWnXWFnuzcOXLBI-g8'
            }
            response = test_client.delete('/delete', headers= headers)

            data = json.loads(response.data)
            checking_response(response, data)
