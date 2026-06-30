import { View, Text, StyleSheet, TouchableOpacity, ImageBackground, SafeAreaView } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';

export default function HomeScreen({ navigation }) {
  return (
    <View style={styles.container}>
      <SafeAreaView style={styles.safeArea}>
        <View style={styles.topRow}>
          <Text style={styles.wordmark}>Wingman</Text>
          <TouchableOpacity>
            <Text style={styles.settingsIcon}>⚙</Text>
          </TouchableOpacity>
        </View>

        <Text style={styles.greeting}>Hey Arjun,</Text>
        <Text style={styles.date}>TODAY, 12 MAY</Text>

        <View style={styles.cardStack}>
          <TouchableOpacity activeOpacity={0.85} onPress={() => navigation.navigate('Home')}>
            <ImageBackground
              source={require('../assets/profile-audit.jpg')}
              style={[styles.card, styles.activeCard]}
              imageStyle={styles.cardImage}
            >
              <LinearGradient
                colors={['rgba(26,15,10,0.3)', 'rgba(26,15,10,0.85)']}
                style={StyleSheet.absoluteFill}
              />
              <View style={styles.cardContent}>
                <Text style={styles.cardTitle}>Profile Audit</Text>
                <Text style={styles.cardSubtitle}>Find out exactly what's killing your matches.</Text>
              </View>
              <Text style={styles.cardArrow}>→</Text>
            </ImageBackground>
          </TouchableOpacity>

          <TouchableOpacity activeOpacity={0.85} onPress={() => navigation.navigate('OpenerUpload')}>
            <ImageBackground
              source={require('../assets/opener-generator.jpg')}
              style={styles.card}
              imageStyle={styles.cardImage}
            >
              <LinearGradient
                colors={['rgba(26,15,10,0.3)', 'rgba(26,15,10,0.85)']}
                style={StyleSheet.absoluteFill}
              />
              <View style={styles.cardContent}>
                <Text style={styles.cardTitle}>Opener Generator</Text>
                <Text style={styles.cardSubtitle}>Upload their photo.{'\n'}Get 3 openers that actually work.</Text>
              </View>
              <Text style={styles.cardArrowSecondary}>→</Text>
            </ImageBackground>
          </TouchableOpacity>

          <View style={styles.lockedCardWrapper}>
            <ImageBackground
              source={require('../assets/chat-assistant.jpg')}
              style={styles.card}
              imageStyle={styles.cardImage}
            >
              <LinearGradient
                colors={['rgba(13,8,7,0.5)', 'rgba(13,8,7,0.92)']}
                style={StyleSheet.absoluteFill}
              />
              <View style={styles.cardContent}>
                <Text style={styles.cardTitleLocked}>Chat Assistant</Text>
                <Text style={styles.cardSubtitleLocked}>Coming soon.</Text>
              </View>
              <View style={styles.soonPill}>
                <Text style={styles.soonText}>Soon</Text>
              </View>
            </ImageBackground>
          </View>
        </View>
      </SafeAreaView>

      <View style={styles.bottomNav}>
        <View style={styles.navItem}>
          <Text style={styles.navIconActive}>⌂</Text>
          <View style={styles.activeDot} />
        </View>
        <View style={styles.navItem}>
          <Text style={styles.navIcon}>💬</Text>
        </View>
        <View style={styles.navItem}>
          <Text style={styles.navIcon}>☺</Text>
        </View>
      </View>
    </View>
  );
}

const GOLD = '#D4A574';
const CREAM = '#F0EFF4';

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#0d0807' },
  safeArea: { flex: 1, paddingHorizontal: 20 },

  topRow: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginTop: 8 },
  wordmark: { fontFamily: 'DMSerifDisplay_400Regular', fontSize: 22, color: GOLD },
  settingsIcon: { fontSize: 20, color: 'rgba(212,165,116,0.5)' },

  greeting: { fontFamily: 'DMSerifDisplay_400Regular_Italic', fontSize: 40, color: CREAM, marginTop: 24 },
  date: { fontSize: 12, color: GOLD, letterSpacing: 2, marginTop: 6, fontWeight: '600' },

  cardStack: { marginTop: 28, gap: 16, paddingBottom: 16 },

  card: { height: 190, borderRadius: 16, overflow: 'hidden', justifyContent: 'flex-end', borderWidth: 1, borderColor: 'rgba(212,165,116,0.15)' },
  activeCard: { borderLeftWidth: 3, borderLeftColor: GOLD },
  cardImage: { borderRadius: 16 },

  cardContent: { padding: 18 },
  cardTitle: { fontFamily: 'DMSerifDisplay_400Regular_Italic', fontSize: 26, color: CREAM },
  cardSubtitle: { fontSize: 13, color: 'rgba(240,239,244,0.6)', marginTop: 6, lineHeight: 18 },

  cardTitleLocked: { fontFamily: 'DMSerifDisplay_400Regular_Italic', fontSize: 24, color: 'rgba(240,239,244,0.4)' },
  cardSubtitleLocked: { fontSize: 13, color: 'rgba(240,239,244,0.25)', marginTop: 6 },

  cardArrow: { position: 'absolute', bottom: 18, right: 18, fontSize: 18, color: GOLD },
  cardArrowSecondary: { position: 'absolute', bottom: 18, right: 18, fontSize: 18, color: 'rgba(212,165,116,0.6)' },

  lockedCardWrapper: { opacity: 0.85 },
  soonPill: { position: 'absolute', bottom: 18, right: 18 },
  soonText: { fontSize: 12, color: GOLD, fontWeight: '600' },

  bottomNav: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    paddingVertical: 14,
    borderTopWidth: 1,
    borderTopColor: 'rgba(212,165,116,0.1)',
    backgroundColor: '#0d0807',
  },
  navItem: { alignItems: 'center', gap: 4 },
  navIcon: { fontSize: 20, color: 'rgba(240,239,244,0.3)' },
  navIconActive: { fontSize: 20, color: GOLD },
  activeDot: { width: 4, height: 4, borderRadius: 2, backgroundColor: GOLD },
});