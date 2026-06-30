import { useRef } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, SafeAreaView } from 'react-native';
import { Video, ResizeMode } from 'expo-av';
import { LinearGradient } from 'expo-linear-gradient';

export default function AuthScreen({ navigation }) {
  const video = useRef(null);

  return (
    <View style={styles.container}>
      <Video
        ref={video}
        source={require('../assets/splash video.mp4')}
        style={StyleSheet.absoluteFill}
        resizeMode={ResizeMode.COVER}
        shouldPlay
        isLooping
        isMuted
      />

      <LinearGradient
        colors={['rgba(0,0,0,0.3)', 'rgba(0,0,0,0.5)', '#000000']}
        style={StyleSheet.absoluteFill}
        locations={[0, 0.4, 0.85]}
      />

      <SafeAreaView style={styles.content}>
        <View style={styles.toast}>
          <View style={styles.toastTop}>
            <Text style={styles.toastApp}>Wingman</Text>
            <Text style={styles.toastTime}>now</Text>
          </View>
          <Text style={styles.toastTitle}>🎉 You got 23 new matches</Text>
          <Text style={styles.toastBody}>Your conversations are working. Keep it up.</Text>
        </View>

        <View style={styles.textBlock}>
          <Text style={styles.title}>Wingman</Text>
          <Text style={styles.tagline}>your move.</Text>

          <Text style={styles.headline}>Dating is a skill.{'\n'}Great relationships aren't luck.</Text>
          <Text style={styles.subtext}>Your AI dating coach for real-world results.</Text>
        </View>

        <View style={styles.buttonBlock}>
          <TouchableOpacity style={styles.googleButton} onPress={() => navigation.navigate('Home')}>
            <Text style={styles.googleIcon}>G</Text>
            <Text style={styles.googleButtonText}>Continue with Google</Text>
          </TouchableOpacity>

          <TouchableOpacity style={styles.emailButton} onPress={() => navigation.navigate('Signup')}>
            <Text style={styles.emailIcon}>✉</Text>
            <Text style={styles.emailButtonText}>Continue with Email</Text>
          </TouchableOpacity>

          <View style={styles.dividerRow}>
            <View style={styles.dividerLine} />
            <Text style={styles.dividerText}>or</Text>
            <View style={styles.dividerLine} />
          </View>

          <TouchableOpacity onPress={() => navigation.navigate('Login')}>
            <Text style={styles.signInText}>
              Already have an account? <Text style={styles.signInLink}>Sign in</Text>
            </Text>
          </TouchableOpacity>
        </View>
      </SafeAreaView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#000000' },
  content: { flex: 1, justifyContent: 'space-between', paddingHorizontal: 24, paddingTop: 16, paddingBottom: 24 },

  toast: {
    backgroundColor: 'rgba(255,255,255,0.08)',
    borderWidth: 1,
    borderColor: 'rgba(255,255,255,0.1)',
    borderRadius: 16,
    padding: 16,
  },
  toastTop: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: 6 },
  toastApp: { color: 'rgba(240,239,244,0.6)', fontSize: 13, fontWeight: '600' },
  toastTime: { color: 'rgba(240,239,244,0.4)', fontSize: 13 },
  toastTitle: { color: '#F0EFF4', fontSize: 16, fontWeight: '700', marginBottom: 4 },
  toastBody: { color: 'rgba(240,239,244,0.6)', fontSize: 14, lineHeight: 19 },

  textBlock: { alignItems: 'center', flex: 1, justifyContent: 'center' },
  title: { fontSize: 40, fontWeight: '700', color: '#F0EFF4', letterSpacing: -0.5 },
  tagline: { fontSize: 15, color: 'rgba(240,239,244,0.4)', marginTop: 4, marginBottom: 28 },
  headline: { fontSize: 22, fontWeight: '600', color: '#F0EFF4', textAlign: 'center', lineHeight: 30, fontStyle: 'italic' },
  subtext: { fontSize: 14, color: 'rgba(240,239,244,0.5)', textAlign: 'center', marginTop: 12 },

  buttonBlock: { gap: 10 },
  googleButton: {
    flexDirection: 'row',
    backgroundColor: '#FFFFFF',
    borderRadius: 14,
    paddingVertical: 15,
    alignItems: 'center',
    justifyContent: 'center',
    gap: 10,
  },
  googleIcon: { fontSize: 16, fontWeight: '700', color: '#4285F4' },
  googleButtonText: { color: '#000000', fontSize: 15, fontWeight: '600' },

  emailButton: {
    flexDirection: 'row',
    backgroundColor: 'rgba(255,255,255,0.06)',
    borderWidth: 1,
    borderColor: 'rgba(255,255,255,0.15)',
    borderRadius: 14,
    paddingVertical: 15,
    alignItems: 'center',
    justifyContent: 'center',
    gap: 10,
  },
  emailIcon: { fontSize: 15, color: '#F0EFF4' },
  emailButtonText: { color: '#F0EFF4', fontSize: 15, fontWeight: '600' },

  dividerRow: { flexDirection: 'row', alignItems: 'center', marginVertical: 6 },
  dividerLine: { flex: 1, height: 1, backgroundColor: 'rgba(255,255,255,0.12)' },
  dividerText: { color: 'rgba(240,239,244,0.4)', fontSize: 13, marginHorizontal: 12 },

  signInText: { color: 'rgba(240,239,244,0.5)', fontSize: 14, textAlign: 'center' },
  signInLink: { color: '#D4A574', fontWeight: '600' },
});