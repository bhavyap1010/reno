import { useRouter, useLocalSearchParams } from 'expo-router';
import { useEffect } from 'react';

export default function GoogleCallback() {
  const { code } = useLocalSearchParams();
  const router = useRouter();

  useEffect(() => {
    if (!code) return;

    (async () => {
      try {
        const res = await fetch('http://localhost:8000/api/v1/auth/google/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ code }),
        });
        const result = await res.json();
        console.log(result);

        router.replace('/');
      } catch (e) {
        console.error(e);
      }
    })();
  }, [code]);

  return null;
}
