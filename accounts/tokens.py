from django.core.signing import TimestampSigner


def generate_user_token(user_id):
    user_specific_signer = TimestampSigner(salt=f"user_{user_id}")
    payload = {'user_id': user_id}
    token = user_specific_signer.sign_object(payload)
    return token


def verify_user_token(user_id, token, max_age=None):
    user_specific_signer = TimestampSigner(salt=f"user_{user_id}")
    payload = user_specific_signer.unsign_object(token, max_age=max_age)
    return payload
