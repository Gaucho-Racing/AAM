import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { checkCredentials } from "@/lib/auth";
import Footer from "@/components/Footer";
import { AuthLoading } from "@/components/AuthLoading";
import { useUser } from "@/lib/store";
import Header from "@/components/Header";
import { Client, initClient } from "@/models/client";
import { BACKEND_URL } from "@/consts/config";
import axios from "axios";
import { notify } from "@/lib/notify";
import { getAxiosErrorMessage } from "@/lib/axios-error-handler";
import { OutlineButton } from "@/components/ui/outline-button";
import { Plus } from "lucide-react";
import { NoProfilesCard } from "@/components/NoProfilesCard";
import { NoExpiredProfilesCard } from "@/components/NoExpiredProfilesCard";
import { ProfileCard } from "@/components/ProfileCard";

function App() {
  const navigate = useNavigate();
  const currentUser = useUser();

  React.useEffect(() => {
    checkAuth().then(() => {});
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

  return (
    <>
      {currentUser.id == "" ? (
        <AuthLoading />
      ) : (
        <div className="flex h-screen flex-col justify-between">
          <Header />
          <div className="flex flex-grow flex-col justify-start p-4 lg:p-32 lg:pt-16">
            <div className="flex flex-row items-center justify-between"></div>
          </div>
          <Footer />
        </div>
      )}
    </>
  );
}

export default App;
