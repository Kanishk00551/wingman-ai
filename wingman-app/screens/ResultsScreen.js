import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';

export default function ResultsScreen({ navigation }) {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Results ✨</Text>
      <Text style={styles.sub}>Your openers will appear here</Text>

      <TouchableOpacity style={styles.button} onPress={() => navigation.goBack()}>
        <Text style={styles.buttonText}>← Go Back</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#0f0f0f', alignItems: 'center', justifyContent: 'center' },
  title: { fontSize: 32, fontWeight: 'bold', color: '#fff' },
  sub: { fontSize: 15, color: '#888', marginTop: 8, marginBottom: 40 },
  button: { backgroundColor: '#333', paddingHorizontal: 32, paddingVertical: 14, borderRadius: 12 },
  buttonText: { color: '#fff', fontSize: 16, fontWeight: '600' },
});