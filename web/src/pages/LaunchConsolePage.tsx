import React from "react";
import axios from "axios";
import {
  BACKEND_URL,
  SENTINEL_CLIENT_ID,
  SENTINEL_OAUTH_BASE_URL,
} from "@/consts/config";
import { Card } from "@/components/ui/card";
import { Loader2, Copy, Check } from "lucide-react";
import { getAxiosErrorMessage } from "@/lib/axios-error-handler";
import { useNavigate, useSearchParams } from "react-router-dom";
import { checkCredentials, logout, saveAccessToken } from "@/lib/auth";
import { notify } from "@/lib/notify";
import { OutlineButton } from "@/components/ui/outline-button";

function LaunchConsolePage() {
  const navigate = useNavigate();
  const [queryParameters] = useSearchParams();

  const [sentinelMsg, setSentinelMsg] = React.useState("");
  const [loginLoading, setLoginLoading] = React.useState(true);
  const [error, setError] = React.useState("");
  const [iamCredentials, setIamCredentials] = React.useState({
    access_key_id: "",
    secret_access_key: "",
    session_token: "",
    expiration: "",
    assumed_role_arn: "",
    login_url: "",
  });
  const [copiedField, setCopiedField] = React.useState("");

  React.useEffect(() => {
    ping();
    checkAuth().then(() => {
      getCredentials();
    });
  }, []);

  const checkAuth = async () => {
    const currentRoute = window.location.pathname + window.location.search;
    const status = await checkCredentials();
    if (status != 0) {
      if (currentRoute == "/") {
        navigate(`/auth/login`);
      } else {
        navigate(`/auth/login?route=${encodeURIComponent(currentRoute)}`);
      }
    }
  };

  const ping = async () => {
    try {
      const response = await axios.get(`${BACKEND_URL}/ping`);
      setSentinelMsg(response.data.message);
    } catch (error: any) {
      notify.error(getAxiosErrorMessage(error));
    }
  };

  const getCredentials = async () => {
    setLoginLoading(true);
    setError("");
    const idToken = localStorage.getItem("sentinel_id_token");
    if (!idToken) {
      logout();
      navigate(`/auth/login`);
      return;
    }
    try {
      const response = await axios.post(
        `${BACKEND_URL}/iam/login`,
        {},
        {
          headers: {
            Authorization: `Bearer ${idToken}`,
          },
        },
      );
      if (response.status == 200) {
        setLoginLoading(false);
        setIamCredentials(response.data);
        window.location.href = response.data.login_url;
      } else {
        setError(response.data);
        setLoginLoading(false);
      }
    } catch (error: any) {
      setError(getAxiosErrorMessage(error));
      setLoginLoading(false);
    }
  };

  const copyToClipboard = async (text: string, fieldName: string) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopiedField(fieldName);
      setTimeout(() => setCopiedField(""), 2000);
      notify.success(`${fieldName} copied to clipboard!`);
    } catch (err) {
      notify.error("Failed to copy to clipboard");
    }
  };

  const LoadingCard = () => {
    return (
      <Card className="border-none p-4 md:w-[500px] md:p-8">
        <div className="flex flex-col items-center justify-center">
          <img
            src="/logo/mechanic-logo.png"
            alt="Gaucho Racing"
            className="mx-auto h-20 md:h-24"
          />
          <Loader2 className="mt-8 h-16 w-16 animate-spin" />
        </div>
      </Card>
    );
  };

  const InvalidCodeCard = () => {
    return (
      <Card className="p-4 md:w-[500px] md:p-8">
        <div className="items-center">
          <img
            src="/logo/mechanic-logo.png"
            alt="Gaucho Racing"
            className="mx-auto h-20 md:h-24"
          />
          <h1 className="mt-6 text-2xl font-semibold tracking-tight">
            AWS Federation Error
          </h1>
          <p className="mt-4">
            Something went wrong when trying to initialize your IAM session.
          </p>
          <p className="mt-4">{error}</p>
          <OutlineButton
            className="mt-4 w-full"
            onClick={() => {
              logout();
              navigate(
                `/auth/login?route=${encodeURIComponent(window.location.pathname + window.location.search)}`,
              );
            }}
          >
            Sentinel Sign On
          </OutlineButton>
        </div>
      </Card>
    );
  };

  const CredentialField = ({
    label,
    value,
    fieldKey,
  }: {
    label: string;
    value: string;
    fieldKey: string;
  }) => (
    <div className="mt-4 space-y-2">
      <label className="text-sm font-medium text-neutral-300">{label}</label>
      <div className="flex items-center space-x-2">
        <div className="flex-1 rounded-md border border-neutral-700 bg-neutral-800 p-3">
          <code className="break-all text-sm text-neutral-100">{value}</code>
        </div>
        <button
          onClick={() => copyToClipboard(value, label)}
          className="rounded-md border border-neutral-700 p-2 transition-colors hover:bg-neutral-800"
          title={`Copy ${label}`}
        >
          {copiedField === label ? (
            <Check className="h-4 w-4 text-green-400" />
          ) : (
            <Copy className="h-4 w-4 text-neutral-400" />
          )}
        </button>
      </div>
    </div>
  );

  const IamCard = () => {
    const formatExpiration = (exp: string) => {
      return new Date(exp).toLocaleString();
    };

    return (
      <Card className="p-4 md:w-[700px] md:p-8">
        <div className="items-center">
          <img
            src="/logo/mechanic-logo.png"
            alt="Gaucho Racing"
            className="mx-auto h-20 md:h-24"
          />
          <h1 className="mt-6 text-2xl font-semibold tracking-tight">
            AWS IAM Session Credentials
          </h1>
          <p className="mt-4">
            Your session is now ready. You will be automactially redirected to
            the AWS console.
          </p>

          <div className="mt-6 space-y-1">
            <CredentialField
              label="Access Key ID"
              value={iamCredentials.access_key_id || ""}
              fieldKey="access_key_id"
            />
            <CredentialField
              label="Secret Access Key"
              value={iamCredentials.secret_access_key || ""}
              fieldKey="secret_access_key"
            />
            <CredentialField
              label="Session Token"
              value={iamCredentials.session_token || ""}
              fieldKey="session_token"
            />

            <div className="mt-4 grid grid-cols-1 gap-4 md:grid-cols-2">
              <div className="space-y-2">
                <label className="text-sm font-medium text-neutral-300">
                  Expiration
                </label>
                <div className="rounded-md border border-neutral-700 bg-neutral-800 p-3">
                  <code className="text-sm text-neutral-100">
                    {iamCredentials.expiration
                      ? formatExpiration(iamCredentials.expiration)
                      : ""}
                  </code>
                </div>
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium text-neutral-300">
                  Role ARN
                </label>
                <div className="rounded-md border border-neutral-700 bg-neutral-800 p-3">
                  <code className="break-all text-sm text-neutral-100">
                    {iamCredentials.assumed_role_arn || ""}
                  </code>
                </div>
              </div>
            </div>
          </div>

          <OutlineButton
            className="mt-6 w-full"
            onClick={() => {
              window.location.href = iamCredentials.login_url;
            }}
          >
            Launch Console
          </OutlineButton>
        </div>
      </Card>
    );
  };

  return (
    <>
      <div className="flex h-screen flex-col items-center justify-between">
        <div className="w-full"></div>
        <div className="w-full items-center justify-center p-4 md:flex md:p-32">
          {loginLoading ? (
            <LoadingCard />
          ) : error == "" ? (
            <IamCard />
          ) : (
            <InvalidCodeCard />
          )}
        </div>
        <div className="flex w-full justify-end p-4 text-gray-500">
          <p>{sentinelMsg}</p>
        </div>
      </div>
    </>
  );
}

export default LaunchConsolePage;
