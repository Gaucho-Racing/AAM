import requests
from loguru import logger
from pydantic import BaseModel, ValidationError

from aam.config.config import Config
from aam.model.user import User


class SentinelTokenResponse(BaseModel):
    """Response from the Sentinel API when exchanging a code for a token."""

    access_token: str | None = None
    refresh_token: str | None = None
    id_token: str | None = None
    token_type: str | None = None
    expires_in: int | None = None
    scope: str | None = None


class SentinelErrorResponse(BaseModel):
    """Error response from the Sentinel API."""

    message: str


class SentinelError(Exception):
    """Exception raised for Sentinel API errors."""

    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message
        super().__init__(f"Sentinel error: [{code}] {message}")


class Sentinel:
    """Service for interacting with the Sentinel API with Pydantic models."""

    @staticmethod
    def ping() -> bool:
        """
        Ping the Sentinel API to check if it is online.

        Returns:
            bool: True if the API is online, False otherwise
        """
        try:
            response = requests.get(f"{Config.SENTINEL_URL}/ping")
            logger.info(f"Successfully pinged sentinel: {response.status_code}")
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Failed to ping sentinel: {e}")
            return False

    @staticmethod
    def _handle_api_error(response: requests.Response) -> None:
        """
        Handle API error responses using Pydantic parsing.

        Args:
            response: The HTTP response object

        Raises:
            SentinelError: If the response indicates an error
        """
        if response.status_code != 200:
            logger.info(f"Response body: {response.text}")
            try:
                error_data = SentinelErrorResponse.model_validate(response.json())
                raise SentinelError(response.status_code, error_data.message)
            except (ValidationError, ValueError):
                # Fallback if error response doesn't match expected format
                raise SentinelError(response.status_code, "Unknown error")

    @staticmethod
    def exchange_code_for_token(code: str) -> SentinelTokenResponse:
        """
        Exchange an authorization code for an access token using Pydantic parsing.

        Args:
            code: The authorization code from OAuth grant

        Returns:
            SentinelTokenResponse: Token response object

        Raises:
            SentinelError: If the API request fails
        """
        try:
            response = requests.post(
                f"{Config.SENTINEL_URL}/oauth/token",
                data={
                    "grant_type": "authorization_code",
                    "client_id": Config.SENTINEL_CLIENT_ID,
                    "client_secret": Config.SENTINEL_CLIENT_SECRET,
                    "code": code,
                    "redirect_uri": Config.SENTINEL_REDIRECT_URI,
                },
            )

            Sentinel._handle_api_error(response)

            # Use Pydantic to automatically parse and validate the JSON response
            return SentinelTokenResponse.model_validate(response.json())

        except requests.RequestException as e:
            logger.error(f"Failed to exchange code for token: {e}")
            raise SentinelError(500, f"Request failed: {str(e)}")
        except ValidationError as e:
            logger.error(f"Failed to parse token response: {e}")
            raise SentinelError(500, "Invalid response format")

    @staticmethod
    def refresh_credentials(refresh_token: str) -> SentinelTokenResponse:
        """
        Refresh access credentials using a refresh token with Pydantic parsing.

        Args:
            refresh_token: The refresh token

        Returns:
            SentinelTokenResponse: New token response

        Raises:
            SentinelError: If the API request fails
        """
        try:
            response = requests.post(
                f"{Config.SENTINEL_URL}/oauth/token",
                data={
                    "grant_type": "refresh_token",
                    "refresh_token": refresh_token,
                    "client_id": Config.SENTINEL_CLIENT_ID,
                    "client_secret": Config.SENTINEL_CLIENT_SECRET,
                    "redirect_uri": Config.SENTINEL_REDIRECT_URI,
                },
            )

            Sentinel._handle_api_error(response)

            # Use Pydantic to automatically parse and validate the JSON response
            return SentinelTokenResponse.model_validate(response.json())

        except requests.RequestException as e:
            logger.error(f"Failed to refresh credentials: {e}")
            raise SentinelError(500, f"Request failed: {str(e)}")
        except ValidationError as e:
            logger.error(f"Failed to parse token response: {e}")
            raise SentinelError(500, "Invalid response format")

    @staticmethod
    def get_all_users() -> list[User]:
        """
        Get all users from the Sentinel API using Pydantic parsing.

        Returns:
            List[User]: List of all users

        Raises:
            SentinelError: If the API request fails
        """
        try:
            headers = {"Authorization": f"Bearer {Config.SENTINEL_TOKEN}"}
            response = requests.get(f"{Config.SENTINEL_URL}/users", headers=headers)

            Sentinel._handle_api_error(response)

            # Use Pydantic to automatically parse and validate the JSON response
            users_data = response.json()
            users = [User.model_validate(user_data) for user_data in users_data]

            return users

        except requests.RequestException as e:
            logger.error(f"Failed to get users from sentinel: {e}")
            raise SentinelError(500, f"Request failed: {str(e)}")
        except ValidationError as e:
            logger.error(f"Failed to parse users response: {e}")
            raise SentinelError(500, "Invalid response format")

    @staticmethod
    def get_user(user_id: str) -> User:
        """
        Get a specific user from the Sentinel API by ID using Pydantic parsing.

        Args:
            user_id: The ID of the user to retrieve

        Returns:
            User: The user object

        Raises:
            SentinelError: If the API request fails
        """
        try:
            headers = {"Authorization": f"Bearer {Config.SENTINEL_TOKEN}"}
            response = requests.get(
                f"{Config.SENTINEL_URL}/users/{user_id}", headers=headers
            )

            Sentinel._handle_api_error(response)

            # Use Pydantic to automatically parse and validate the JSON response
            return User.model_validate(response.json())

        except requests.RequestException as e:
            logger.error(f"Failed to get user from sentinel: {e}")
            raise SentinelError(500, f"Request failed: {str(e)}")
        except ValidationError as e:
            logger.error(f"Failed to parse user response: {e}")
            raise SentinelError(500, "Invalid response format")

    @staticmethod
    def get_current_user(access_token: str) -> User:
        """
        Get the current user from the Sentinel API based on access token using Pydantic parsing.

        Args:
            access_token: The user's access token

        Returns:
            User: The current user object

        Raises:
            SentinelError: If the API request fails
        """
        try:
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get(f"{Config.SENTINEL_URL}/users/@me", headers=headers)

            Sentinel._handle_api_error(response)

            # Use Pydantic to automatically parse and validate the JSON response
            return User.model_validate(response.json())

        except requests.RequestException as e:
            logger.error(f"Failed to get current user from sentinel: {e}")
            raise SentinelError(500, f"Request failed: {str(e)}")
        except ValidationError as e:
            logger.error(f"Failed to parse user response: {e}")
            raise SentinelError(500, "Invalid response format")
