import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';

export default function HomeScreen({ navigation }) {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Wingman AI 🪶</Text>
      <Text style={styles.sub}>Your AI dating coach</Text>

      <TouchableOpacity style={styles.button} onPress={() => navigation.navigate('Results')}>
        <Text style={styles.buttonText}>Get Openers →</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#0f0f0f', alignItems: 'center', justifyContent: 'center' },
  title: { fontSize: 36, fontWeight: 'bold', color: '#fff' },
  sub: { fontSize: 16, color: '#888', marginTop: 8, marginBottom: 40 },
  button: { backgroundColor: '#7c3aed', paddingHorizontal: 32, paddingVertical: 14, borderRadius: 12 },
  buttonText: { color: '#fff', fontSize: 16, fontWeight: '600' },
});