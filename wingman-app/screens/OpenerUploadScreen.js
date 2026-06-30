import { useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, ImageBackground, SafeAreaView, ScrollView, Image } from 'react-native';
import * as ImagePicker from 'expo-image-picker';

const GOLD = '#D4A574';
const CREAM = '#F0EFF4';

export default function OpenerUploadScreen({ navigation }) {
  const [mainPhoto, setMainPhoto] = useState(null);
  const [extraPhotos, setExtraPhotos] = useState([]);

  const pickMainPhoto = async () => {
    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: true,
      aspect: [4, 3],
      quality: 0.8,
    });
    if (!result.canceled) {
      setMainPhoto(result.assets[0].uri);
    }
  };

  const pickExtraPhoto = async () => {
    if (extraPhotos.length >= 7) return;
    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      quality: 0.8,
    });
    if (!result.canceled) {
      setExtraPhotos([...extraPhotos, result.assets[0].uri]);
    }
  };

  const canGenerate = mainPhoto !== null;

  const handleGenerate = () => {
    if (!canGenerate) return;
    navigation.navigate('OpenerLoading', { mainPhoto, extraPhotos });
  };

  return (
    <View style={styles.container}>
      <SafeAreaView style={styles.safeArea}>
        <View style={styles.topRow}>
          <TouchableOpacity onPress={() => navigation.goBack()}>
            <Text style={styles.backIcon}>←</Text>
          </TouchableOpacity>
          <Text style={styles.headerTitle}>Opener Generator</Text>
          <TouchableOpacity>
            <Text style={styles.settingsIcon}>⚙</Text>
          </TouchableOpacity>
        </View>

        <View style={styles.progressRow}>
          <View style={styles.progressLabels}>
            <Text style={styles.progressLabelActive}>Upload</Text>
            <Text style={styles.progressLabelInactive}>Generate</Text>
          </View>
          <View style={styles.progressTrack}>
            <View style={styles.progressDotActive} />
            <View style={styles.progressLine} />
            <View style={styles.progressDotInactive} />
          </View>
        </View>

        <ScrollView showsVerticalScrollIndicator={false}>
          <Text style={styles.headline}>
            Show me who they are,{'\n'}
            <Text style={styles.headlineItalic}>I'll write the perfect opener.</Text>
          </Text>
          <Text style={styles.subtext}>Add their photos and I'll craft openers that get real replies.</Text>

          <TouchableOpacity style={styles.mainUploadBox} onPress={pickMainPhoto} activeOpacity={0.8}>
            {mainPhoto ? (
              <Image source={{ uri: mainPhoto }} style={styles.mainPhotoPreview} />
            ) : (
              <>
                <Text style={styles.plusIcon}>+</Text>
                <Text style={styles.uploadTitle}>Add their best photo</Text>
                <Text style={styles.uploadSubtitle}>This photo is required.</Text>
              </>
            )}
          </TouchableOpacity>

          <View style={styles.moreContextRow}>
            <Text style={styles.moreContextLabel}>More context</Text>
            <Text style={styles.optionalLabel}> (Optional)</Text>
          </View>
          <Text style={styles.moreContextSubtext}>
            The more photos you add, the better Wingman understands their vibe.
          </Text>

          <View style={styles.thumbGrid}>
            {[...Array(7)].map((_, i) => (
              <TouchableOpacity
                key={i}
                style={[styles.thumbSlot, extraPhotos[i] && styles.thumbSlotFilled]}
                onPress={pickExtraPhoto}
                activeOpacity={0.8}
              >
                {extraPhotos[i] ? (
                  <Image source={{ uri: extraPhotos[i] }} style={styles.thumbImage} />
                ) : (
                  <Text style={styles.thumbPlus}>+</Text>
                )}
              </TouchableOpacity>
            ))}
          </View>

          <TouchableOpacity style={styles.addAnotherRow} onPress={pickExtraPhoto}>
            <Text style={styles.addAnotherIcon}>⊕</Text>
            <Text style={styles.addAnotherText}>Add another photo</Text>
          </TouchableOpacity>

          <View style={{ height: 100 }} />
        </ScrollView>
      </SafeAreaView>

      <View style={styles.bottomBar}>
        <TouchableOpacity
          style={[styles.generateButton, !canGenerate && styles.generateButtonDisabled]}
          onPress={handleGenerate}
          disabled={!canGenerate}
        >
          <Text style={[styles.generateButtonText, !canGenerate && styles.generateButtonTextDisabled]}>
            Generate Openers ✦
          </Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#0d0807' },
  safeArea: { flex: 1, paddingHorizontal: 20 },

  topRow: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginTop: 8, marginBottom: 20 },
  backIcon: { fontSize: 22, color: CREAM },
  headerTitle: { fontFamily: 'DMSerifDisplay_400Regular', fontSize: 18, color: CREAM },
  settingsIcon: { fontSize: 18, color: 'rgba(212,165,116,0.5)' },

  progressRow: { marginBottom: 28 },
  progressLabels: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: 8 },
  progressLabelActive: { fontSize: 13, color: GOLD, fontWeight: '600' },
  progressLabelInactive: { fontSize: 13, color: 'rgba(240,239,244,0.4)' },
  progressTrack: { flexDirection: 'row', alignItems: 'center' },
  progressDotActive: { width: 10, height: 10, borderRadius: 5, backgroundColor: GOLD },
  progressLine: { flex: 1, height: 1, backgroundColor: 'rgba(212,165,116,0.3)', marginHorizontal: 4 },
  progressDotInactive: { width: 10, height: 10, borderRadius: 5, borderWidth: 1.5, borderColor: 'rgba(240,239,244,0.3)' },

  headline: { fontFamily: 'DMSerifDisplay_400Regular', fontSize: 28, color: CREAM, lineHeight: 36 },
  headlineItalic: { fontFamily: 'DMSerifDisplay_400Regular_Italic' },
  subtext: { fontSize: 14, color: 'rgba(240,239,244,0.5)', marginTop: 12, lineHeight: 20 },

  mainUploadBox: {
    height: 280,
    borderRadius: 16,
    borderWidth: 1,
    borderColor: 'rgba(212,165,116,0.3)',
    borderStyle: 'dashed',
    backgroundColor: 'rgba(212,165,116,0.04)',
    alignItems: 'center',
    justifyContent: 'center',
    marginTop: 28,
    overflow: 'hidden',
  },
  mainPhotoPreview: { width: '100%', height: '100%' },
  plusIcon: { fontSize: 32, color: GOLD, marginBottom: 12 },
  uploadTitle: { fontFamily: 'DMSerifDisplay_400Regular', fontSize: 20, color: CREAM },
  uploadSubtitle: { fontSize: 13, color: 'rgba(240,239,244,0.4)', marginTop: 6 },

  moreContextRow: { flexDirection: 'row', marginTop: 32 },
  moreContextLabel: { fontFamily: 'DMSerifDisplay_400Regular', fontSize: 16, color: GOLD },
  optionalLabel: { fontSize: 14, color: 'rgba(240,239,244,0.4)' },
  moreContextSubtext: { fontSize: 13, color: 'rgba(240,239,244,0.45)', marginTop: 6, lineHeight: 18 },

  thumbGrid: { flexDirection: 'row', flexWrap: 'wrap', gap: 10, marginTop: 16 },
  thumbSlot: {
    width: 80,
    height: 80,
    borderRadius: 10,
    borderWidth: 1,
    borderColor: 'rgba(212,165,116,0.2)',
    borderStyle: 'dashed',
    backgroundColor: 'rgba(212,165,116,0.03)',
    alignItems: 'center',
    justifyContent: 'center',
    overflow: 'hidden',
  },
  thumbSlotFilled: { borderStyle: 'solid' },
  thumbImage: { width: '100%', height: '100%' },
  thumbPlus: { fontSize: 18, color: 'rgba(240,239,244,0.3)' },

  addAnotherRow: { flexDirection: 'row', alignItems: 'center', marginTop: 16, gap: 8 },
  addAnotherIcon: { fontSize: 16, color: GOLD },
  addAnotherText: { fontSize: 14, color: GOLD, fontWeight: '500' },

  bottomBar: { paddingHorizontal: 20, paddingBottom: 20, paddingTop: 12, backgroundColor: '#0d0807' },
  generateButton: { backgroundColor: GOLD, borderRadius: 14, paddingVertical: 16, alignItems: 'center' },
  generateButtonDisabled: { backgroundColor: 'rgba(212,165,116,0.15)' },
  generateButtonText: { fontFamily: 'DMSerifDisplay_400Regular', fontSize: 17, color: '#1a0f0a' },
  generateButtonTextDisabled: { color: 'rgba(240,239,244,0.3)' },
});