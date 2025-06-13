import { Button, View, StyleSheet } from 'react-native';
import { googleClientId, googleCallbackUri } from '../config';

export default function HomeScreen() {
  const googleSignInUrl = `https://accounts.google.com/o/oauth2/v2/auth?redirect_uri=${googleCallbackUri}&prompt=consent&response_type=code&client_id=${googleClientId}&scope=openid%20email%20profile&access_type=offline`;

  const handleSignIn = () => {
    window.location.href = googleSignInUrl;
  };

  return (
    <View style={styles.container}>
      <Button title="Sign in with Google" onPress={handleSignIn} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', alignItems: 'center' },
});
