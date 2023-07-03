from models import User, Post, Follow, Like, Comment


def test_new_user():
    user = User(
        'osamahunyawwr',
        'osama@gmail.com',
        's2ser',
        'Osama Butt',
        "I'm a devil of my world 😈",
        'https://wallpapers.com/images/high/dark-profile-pictures-1200-x-1714-3nrfdoj70fmbivxq.webp'
    )

    assert user.username == 'osamahunyawwr'
    assert user.email == 'osama@gmail.com'
    assert user.password == 's2ser'
    assert user.name == 'Osama Butt'
    assert user.bio == "I'm a devil of my world 😈"
    assert user.profile_image_url == 'https://wallpapers.com/images/high/dark-profile-pictures-1200-x-1714-3nrfdoj70fmbivxq.webp'


def test_new_post():
    post = Post(
        '1',
        'Racka Backa... Bombasitc!',
        'https://wallpapers.com/images/high/dark-profile-pictures-1680-x-1050-8ybcdnlc2d35dwt7.webp'
    )

    assert post.user_id == '1'
    assert post.content == 'Racka Backa... Bombasitc!'
    assert post.image_url == 'https://wallpapers.com/images/high/dark-profile-pictures-1680-x-1050-8ybcdnlc2d35dwt7.webp'


def test_new_follow():
    follow = Follow('2', '7')

    assert follow.followed_id == '7'
    assert follow.follower_id == '2'


def test_new_likes():
    like = Like(3, 5, 1)

    assert like.user_id == 3
    assert like.post_id == 5
    assert like.post_liked_of_id == 1


def test_new_comment():
    comment = Comment(1, 1, 'This is my comment', 2)

    assert comment.user_id == 1
    assert comment.post_id == 1
    assert comment.content == 'This is my comment'
    assert comment.post_commented_of_id == 2
