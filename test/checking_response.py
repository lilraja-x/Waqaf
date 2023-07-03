def checking_response(response, data):
    '''
        Function that checks: 
            -correctness of message on response status code.

        args:
            - response
            - data
        
        used in:
            - test_account.py
            - test_commenting.py
            - test_following.py
            - test_unfollowing.py
            - test_liking.py
            - test_unliking.py
            - test_posting.py
            - test_view_and_edit_profile.py
    '''
    if response.status_code in (200, 201):
        assert "Account Created" or "User Found" or "Message Edited!" or "Message Deleted!" or "Message Sent!" or "Account deleted successfully!" or "Logged In!" or "Comment added successfully" or  "Comment deleted successfully" or "Comment updated successfully" or "Successfully Followed" or "Successfully unfollowed" or "Post liked successfully" or "Post unliked successfully" or "Post Added!" or "Post Deleted!" or "Post Updated!" or "Profile Updated Successfully!" or "Data fetched!" or "Password reset token has been sent to your email." in data['Message']
    elif response.status_code == 500:
        assert "Token Invalid" in data['Message']
    elif response.status_code == 400:
        assert "Failed to Create Account" or "Message Not Not Deleted!" or "Message Not Edited!" or "Message Not Sent!" or "Failed to delete account!" or "Failed to login!" or "Failed to delete comment!" or "Failed to add comment!" or "Failed to update comment!" or "Failed to follow" or "Failed to unfollow" or "Post liked already" or "Post not liked already" or "Unable to add post" or "No post ID provided" or "Unable to delete post" or "Account Not Found" or "Unable to edit post" or "Failed to edit profile!" or "Failed to view profile!" in data['Message']
    elif response.status_code == 401:
        assert "Missing Keys" or "No user found with this username" or "You are not authorized to delete this message" or "Invalid message ID" or "To whom are you sending this message?" or "At least tell whom to follow." or "Atleast add some text to send message" or "Please provide a username to unfollow." or "Atleast add content or image!" or "Password missing!" or "Value Error!" or "Username missing!" in data['Message']
    elif response.status_code == 404:
        assert "User not found" or "Message does not exists" or "Post not found" or "Comment not found" in data['Message']