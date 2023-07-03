from app import create_app
import json
from pytest_check import check
from checking_response import checking_response

def test_view_route():
    '''
    GIVEN a Flask application configured for testing
    WHEN the '/profile/view' page is requested (GET)
    THEN check that the response is valid
    '''

    # Set the Testing configuration prior to creating the Flask application
    flask_app = create_app({"TESTING": True})

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as test_client:
        #Case 1 ==> To View with correct headers
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4ODM2MTA3NiwianRpIjoiYjgwNTFlZjUtZTRlOS00Yjg2LTlmMmUtNGE4MDVjZWQyZWQ1IiwidHlwZSI6InJlZnJlc2giLCJzdWIiOjIsIm5iZiI6MTY4ODM2MTA3NiwiZXhwIjoxNjkwOTUzMDc2fQ.05Y2oWu-v1scZ1EKzHeiRYy5MB0UC-ZD_v_lUqV1Yr8'
        }
        with check:
            response = test_client.patch('/profile/view', headers= headers)
            checking_response(response, response.data)

        #Case 2 ==> To View with incorrect headers
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer eyJhbGciOiJIUzI11NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4ODM2MTA3NiwianRpIjoiYjgwNTFlZjUtZTRlOS00Yjg2LTlmMmUtNGE4MDVjZWQyZWQ1IiwidHlwZSI6InJlZnJlc2giLCJzdWIiOjIsIm5iZiI6MTY4ODM2MTA3NiwiZXhwIjoxNjkwOTUzMDc2fQ.05Y2oWu-v1scZ1EKzHeiRYy5MB0UC-ZD_v_lUqV1Yr8'
        }
        with check:
            response = test_client.patch('/profile/view', headers= headers)
            checking_response(response, response.data)


def test_edit_profile_route():
    '''
    GIVEN a Flask application configured for testing
    WHEN the '/profile/edit' page is requested (PUT, PATCH)
    THEN check that the response is valid
    '''

    # Set the Testing configuration prior to creating the Flask application
    flask_app = create_app({"TESTING": True})
    headers = {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4ODM2MTA3NiwianRpIjoiYjgwNTFlZjUtZTRlOS00Yjg2LTlmMmUtNGE4MDVjZWQyZWQ1IiwidHlwZSI6InJlZnJlc2giLCJzdWIiOjIsIm5iZiI6MTY4ODM2MTA3NiwiZXhwIjoxNjkwOTUzMDc2fQ.05Y2oWu-v1scZ1EKzHeiRYy5MB0UC-ZD_v_lUqV1Yr8'
        }
    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as test_client:
        #Case 1 ==> To Edit Profile's alll detail
        with check:
            response = test_client.patch('/profile/edit', headers= headers, data=json.dumps(dict(username='fillyx', name='fillape', email='fill@gmail.com', bio='Unstoppable', profile_image_url='https://www.metoffice.gov.uk/binaries/content/gallery/metofficegovuk/hero-images/advice/maps-satellite-images/satellite-image-of-globe.jpg')))

            checking_response(response, response.data)

        #Case 2 ==> To Edit Profile's some detail
        with check:
            response = test_client.patch('/profile/edit', headers= headers, data=json.dumps(dict(username='fillyx', profile_image_url='https://www.metoffice.gov.uk/binaries/content/gallery/metofficegovuk/hero-images/advice/maps-satellite-images/satellite-image-of-globe.jpg')))

            checking_response(response, response.data)

        #Case 3 ==> To Edit but wrong headers
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer eyJhbGciOiJIUzI11NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4ODM2MTA3NiwianRpIjoiYjgwNTFlZjUtZTRlOS00Yjg2LTlmMmUtNGE4MDVjZWQyZWQ1IiwidHlwZSI6InJlZnJlc2giLCJzdWIiOjIsIm5iZiI6MTY4ODM2MTA3NiwiZXhwIjoxNjkwOTUzMDc2fQ.05Y2oWu-v1scZ1EKzHeiRYy5MB0UC-ZD_v_lUqV1Yr8'
        }
        with check:
            response = test_client.patch('/profile/edit', headers= headers, data=json.dumps(dict(username='fillyx')))
            checking_response(response, response.data)

        #Case 4 ==> Empty data
        with check:
            response = test_client.patch('/profile/edit', headers=headers)
            checking_response(response, response.data)