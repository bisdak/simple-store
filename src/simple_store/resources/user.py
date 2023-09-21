from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from simple_store import BlacklistedToken
from simple_store.models.user import User as UserModel, UserModelSchema
from simple_store.schema import UserSchema
from flask_jwt_extended import (
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)

blp = Blueprint("Users", "users", description="Operations on users")


@blp.route("/register", endpoint="register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        """Register a new user and return access_token."""
        if UserModel.find_by_email(user_data.get("email", "")):
            abort(409, message="Email address is already registered.")

        user = UserModel(
            email=user_data["email"],
            password=user_data["password"],
        )
        user.save_to_db()
        access_token = user.create_access_token()
        return {
            "message": "User created successfully.",
            "access_token": access_token,
        }, 201


@blp.route("/login", endpoint="login")
class LoginUser(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        """Authenticate an existing user and return an access token."""
        user = UserModel.find_by_email(user_data["email"])

        if user and user.check_password(user_data["password"]):
            access_token = user.create_access_token()
            refresh_token = create_refresh_token(user.public_id)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200

        abort(401, "email or password does not match")


@blp.route("/user", endpoint="user")
class GetUser(MethodView):
    @jwt_required()
    def get(self):
        """Validate access token and return user info."""
        public_id = get_jwt_identity()
        user = UserModel.find_by_public_id(public_id)
        user_schema = UserModelSchema()
        return user_schema.dump(user), 200


@blp.route("/logout", endpoint="logout")
class LogoutUser(MethodView):
    @jwt_required()
    def post(self):
        """Add token to blacklist, deauthenticating the current user."""
        token = request.headers["Authorization"].split(" ")[1]
        expires_at = get_jwt()["exp"]
        blacklisted_token = BlacklistedToken(token, expires_at)
        BlacklistedToken.delete_expired_token()
        blacklisted_token.save_to_db()
        return {"message": "Successfully logged out."}, 200
