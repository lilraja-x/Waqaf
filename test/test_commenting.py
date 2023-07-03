from app import create_app
import json
from pytest_check import check
from checking_response import checking_response


def test_comment_route():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/comment/add (POST)', 'comment/delete (DELETE)', 'comment/edit (PUT/PATCH)' page is requested 
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
        #Case 1 ==> To Add comment
        with check:
            response = test_client.patch('/comment/add', headers= headers, data=json.dumps(dict(user_id=1, post_id=1, content="This is a comment")))

            checking_response(response, response.data)
        
        #Case 2 ==> To Edit comment
        with check:
            response = test_client.patch('/comment/edit', headers= headers, data=json.dumps(dict(user_id=1, post_id=1, content="This is a comment")))

            data = json.loads(response.data)
            checking_response(response, data)


        #Case 3 ==> To delete comment
        with check:
            response = test_client.patch('/comment/delete', headers= headers, data=json.dumps(dict(user_id=1, post_id=1, content="This is a comment")))

            checking_response(response, response.data)

        #Case 4 ==> with wrong headers
        with check:
            headers = {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json',
                'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4ODM2MTA3NiwianRpIjoiYjgwNTFlZjUtZTRlOS00Yjg2LTlmMmUtNGE4MDVjZWQyZWQ1IiwidHlwZSI6InJlZnJlc2giLCJzdWIiOjIsIm5iZiI6MTY4ODM2MTA3NiwiZXhwIjoxNjkwOTUzMDc2fQ.05Y2oWu-v1scZ1EKzHeiRYy5MB0UC-ZD_v_lUqV1Yr8s'
            }
            response = test_client.patch('/comment/add', headers= headers, data=json.dumps(dict(user_id=8, post_id=2, content="This is a comment")))

            checking_response(response, response.data)