import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import {
  View,
  Text,
  TextInput,
  Button,
  StyleSheet,
  TouchableOpacity,
  Alert
} from 'react-native';

function Home() {
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  const GOOGLELOGIN_API = import.meta.env.VITE_GOOGLELOGIN;
  const USERME_API = import.meta.env.VITE_USERME;
  const BLACKLIST_API = import.meta.env.VITE_BLACKLIST;
  const REFRESHTOKEN_API = import.meta.env.VITE_REFRESHTOKEN;

  useEffect(() => {
    const tokenString = localStorage.getItem("auth_token");
    let token = null;
    try {
      token = JSON.parse(tokenString);
    } catch (e) {
      token = tokenString;
    }
    const REFRESH_INTERVAL = 1000 * 60 * 4; // 4 minutes
    const hashParams = new URLSearchParams(window.location.hash.substring(1));
    const accessToken = hashParams.get("access_token");

    if (accessToken) {
      handleGoogleLogin(accessToken);
    } else if (token) {
      fetchUserProfile(token);
    } else {
      navigate("/login");
    }

    const intervalId = setInterval(() => {
      const tokenString = localStorage.getItem("auth_token");
      let token = null;
      try {
        token = JSON.parse(tokenString);
      } catch (e) {
        token = tokenString;
      }
      if (token?.refresh) {
        updateToken(token);
      }
    }, REFRESH_INTERVAL);

    return () => clearInterval(intervalId);
  }, []);

  const fetchUserProfile = async (token) => {
    try {
      const response = await fetch(USERME_API, {
        headers: {
          Authorization: `Bearer ${token?.access}`,
        },
      });
      const data = await response.json();
      setUser(data);
    } catch {
      navigate("/login");
    }
  };

  const handleGoogleLogin = async (accessToken) => {
    try {
      const response = await fetch(GOOGLELOGIN_API, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ access_token: accessToken }),
      });

      const data = await response.json();

      if (data.refresh) {
        localStorage.setItem("auth_token", JSON.stringify(data));
        window.history.replaceState(null, "", "/");
        fetchUserProfile(data)
        navigate("/");
      } else {
        navigate("/login");
      }
    } catch {
      navigate("/login");
    }
  };

  const blacklisttoken = async (token) => {
    try {
      await fetch(BLACKLIST_API, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ refresh: token?.refresh }),
      });
    } catch (err) {
      console.error("Error blacklisting token:", err);
    }
  };

  const logout = () => {
    const tokenString = localStorage.getItem("auth_token");
    let token = null;
    try {
        token = JSON.parse(tokenString);
    } catch (e) {
        token = tokenString;
    }
    localStorage.removeItem("auth_token");
    blacklisttoken(token);
    navigate("/login");
  };

  const updateToken = async (token) => {
    try {
      const response = await fetch(REFRESHTOKEN_API, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ refresh: token?.refresh }),
      });

      const data = await response.json();
      if (response.status === 200) {
        const updatedToken = { ...token, access: data.access };
        localStorage.setItem("auth_token", JSON.stringify(updatedToken));
      } else {
        logout();
      }
    } catch {
      logout();
    }
  };

  if (!user) return <p>Loading...</p>;

  return (
    <View style={styles.container}>
      <View style={styles.details}>
        <View style={styles.row}>
          <Text style={styles.label}>Name: </Text>
          <Text style={styles.value}>{user.username}</Text>
        </View>
        <View style={styles.row}>
          <Text style={styles.label}>Email: </Text>
          <Text style={styles.value}>{user.email}</Text>
        </View>
        <View style={styles.button}>
          <Button title="Sign out" onPress={logout} />
        </View>
      </View>
    </View>
  );
}
export default Home;
