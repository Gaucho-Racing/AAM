import json
import urllib.parse

import boto3
import requests

ADMIN_ROLE_ARN = "arn:aws:iam::211125506628:role/SentinelAdmin"
MEMBER_ROLE_ARN = "arn:aws:iam::211125506628:role/SentinelMember"


class IAMService:
    @staticmethod
    def assume_role(
        id_token: str,
        role_arn: str,
        *,
        region="us-west-2",
        session_name="aam-session",
        duration_seconds=3600,
    ):
        sts = boto3.client("sts", region_name=region)
        resp = sts.assume_role_with_web_identity(
            RoleArn=role_arn,
            RoleSessionName=session_name,
            WebIdentityToken=id_token,
            DurationSeconds=duration_seconds,
        )
        c = resp["Credentials"]
        return {
            "access_key_id": c["AccessKeyId"],
            "secret_access_key": c["SecretAccessKey"],
            "session_token": c["SessionToken"],
            "expiration": c["Expiration"].isoformat(),
            "assumed_role_arn": resp["AssumedRoleUser"]["Arn"],
            "subject_from_web_identity_token": resp.get("SubjectFromWebIdentityToken"),
        }

    @staticmethod
    def build_console_login_url(
        creds: dict, destination="https://us-west-2.console.aws.amazon.com"
    ):
        session = {
            "sessionId": creds["access_key_id"],
            "sessionKey": creds["secret_access_key"],
            "sessionToken": creds["session_token"],
        }
        r = requests.get(
            "https://signin.aws.amazon.com/federation",
            params={
                "Action": "getSigninToken",
                "SessionType": "json",
                "Session": json.dumps(session),
            },
            timeout=30,
        )
        r.raise_for_status()
        token = r.json()["SigninToken"]
        dest = urllib.parse.quote(destination, safe="")
        return f"https://signin.aws.amazon.com/federation?Action=login&Issuer=GauchoRacing&Destination={dest}&SigninToken={token}"
