from app import create_app
import json
from pytest_check import check
from checking_response import checking_response


def test_following_route():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/follow (POST)' page is requested 
    THEN check that the response is valid
    """
    # Set the Testing configuration prior to creating the Flask application
    flask_app = create_app({"TESTING": True})
    headers = {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4ODM2MTA3NiwianRpIjoiYjgwNTFlZjUtZTRlOS00Yjg2LTlmMmUtNGE4MDVjZWQyZWQ1IiwidHlwZSI6InJlZnJlc2giLCJzdWIiOjIsIm5iZiI6MTY4ODM2MTA3NiwiZXhwIjoxNjkwOTUzMDc2fQ.05Y2oWu-v1scZ1EKzHeiRYy5MB0UC-ZD_v_lUqV1Yr8'
        }
    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as test_client:
        #Case 1 ==> To follow a user
        with check:
            response = test_client.patch('/follow', headers= headers, data=json.dumps(dict(username='uzair')))

            checking_response(response, response.data)
        
        #Case 2 ==> To follow with wrong username
        with check:
            response = test_client.patch('/follow', headers= headers, data=json.dumps(dict(username='qasim')))

            checking_response(response, response.data)

        #Case3 ==> null request
        with check:
            response = test_client.patch('/follow', headers= headers, data=json.dumps(dict(username='')))

            checking_response(response, response.data)

        #Case 4 ==> with wrong headers
        with check:
            headers = {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json',
                'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4ODM2MTA3NiwianRpIjoiYjgwNTFlZjUtZTRlOS00Yjg2LTlmMmUtNGE4MDVjZWQyZWQ1IiwidHlwZSI6InJlZnJlc2giLCJzdWIiOjIsIm5iZiI6MTY4ODM2MTA3NiwiZXhwIjoxNjkwOTUzMDc2fQ.05Y2oWu-v1scZ1EKzHeiRYy5MB0UC-ZD_v_lUqV1Yr8s'
            }
            response = test_client.patch('/follow', headers= headers, data=json.dumps(dict(username='uzair')))

            checking_response(response, response.data)