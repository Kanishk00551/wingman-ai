import { useEffect, useRef } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, SafeAreaView } from 'react-native';
import { Video, ResizeMode } from 'expo-av';
import { LinearGradient } from 'expo-linear-gradient';

export default function SplashScreen({ navigation }) {
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
        colors={['transparent', 'rgba(0,0,0,0.4)', '#000000']}
        style={StyleSheet.absoluteFill}
        locations={[0, 0.5, 1]}
      />

      <SafeAreaView style={styles.content}>
        <View style={styles.textBlock}>
          <Text style={styles.title}>Wingman</Text>
          <Text style={styles.tagline}>your move.</Text>
        </View>

        <View style={styles.buttonBlock}>
          <TouchableOpacity
            style={styles.primaryButton}
            onPress={() => navigation.navigate('Auth')}
          >
            <Text style={styles.primaryButtonText}>Create Account</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={styles.secondaryButton}
            onPress={() => navigation.navigate('Auth')}
          >
            <Text style={styles.secondaryButtonText}>Sign In</Text>
          </TouchableOpacity>
        </View>
      </SafeAreaView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#000000' },
  content: { flex: 1, justifyContent: 'space-between', paddingHorizontal: 24, paddingBottom: 24 },
  textBlock: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  title: { fontSize: 42, fontWeight: '700', color: '#F0EFF4', letterSpacing: -0.5 },
  tagline: { fontSize: 16, color: 'rgba(240,239,244,0.5)', marginTop: 8 },
  buttonBlock: { gap: 12 },
  primaryButton: {
    backgroundColor: 'rgba(255,255,255,0.08)',
    borderWidth: 1,
    borderColor: 'rgba(240,239,244,0.15)',
    borderRadius: 14,
    paddingVertical: 16,
    alignItems: 'center',
  },
  primaryButtonText: { color: '#F0EFF4', fontSize: 16, fontWeight: '600' },
  secondaryButton: { paddingVertical: 14, alignItems: 'center' },
  secondaryButtonText: { color: 'rgba(240,239,244,0.7)', fontSize: 15, fontWeight: '500' },
});