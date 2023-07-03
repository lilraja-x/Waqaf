from app import create_app
import json
from pytest_check import check
from checking_response import checking_response


def test_posting_route():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/post/add (POST)', 'post/delete (DELETE)', 'post/edit (PUT/PATCH)' page is requested 
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
        #Case 1 ==> To Add post
        with check:
            response = test_client.patch('/post/add', headers= headers, data=json.dumps(dict(content="This is a post", image="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT9exX-jIAqoN91jcrXpiIsHkLcovEJNk-aX_NQNPIJ4w&")))

            checking_response(response, response.data)
        
        #Case 2 ==> To Edit post
        with check:
            response = test_client.patch('/post/edit', headers= headers, data=json.dumps(dict(post_id=1, content="This is edited post", image="")))

            data = json.loads(response.data)
            checking_response(response, data)


        #Case 3 ==> To delete post
        with check:
            response = test_client.patch('/post/delete', headers= headers, data=json.dumps(dict(post_id=1)))

            checking_response(response, response.data)

        #Case 4 ==> with wrong headers
        with check:
            headers = {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json',
                'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4ODM2MTA3NiwianRpIjoiYjgwNTFlZjUtZTRlOS00Yjg2LTlmMmUtNGE4MDVjZWQyZWQ1IiwidHlwZSI6InJlZnJlc2giLCJzdWIiOjIsIm5iZiI6MTY4ODM2MTA3NiwiZXhwIjoxNjkwOTUzMDc2fQ.05Y2oWu-v1scZ1EKzHeiRYy5MB0UC-ZD_v_lUqV1Yr8s'
            }
            response = test_client.patch('/post/add', headers= headers, data=json.dumps(dict(content="This is a post", image="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT9exX-jIAqoN91jcrXpiIsHkLcovEJNk-aX_NQNPIJ4w&")))

            checking_response(response, response.data)