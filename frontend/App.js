import React, { useState } from 'react';
import { View, Text, Button, Image, ActivityIndicator, Alert, Platform } from 'react-native';
import * as ImagePicker from 'expo-image-picker';

export default function App() {
  const [imageUri, setImageUri] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [detections, setDetections] = useState([]);

  const pickImage = async () => {
    console.log("📷 Launching image picker...");
  
    const { status } = await ImagePicker.requestMediaLibraryPermissionsAsync();
    if (status !== 'granted') {
      Alert.alert('Permission required', 'We need permission to access your photos.');
      return;
    }
  
    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaType.IMAGE,
      allowsEditing: true,
      quality: 1,
    });
  
    console.log("🔍 Image picker result:", result);
  
    if (!result.canceled && result.assets && result.assets.length > 0) {
      setImageUri(result.assets[0].uri);
      console.log("✅ Image set:", result.assets[0].uri);
    } else {
      console.log("❌ No image selected");
    }
  };
  
  

  const uploadImage = async () => {
    if (!imageUri) return;

    setIsLoading(true);
    const formData = new FormData();

    const filename = imageUri.split('/').pop();
    const match = /\.(\w+)$/.exec(filename ?? '');
    const ext = match ? match[1].toLowerCase() : 'jpg';
    const mimeType =
      ext === 'jpg' || ext === 'jpeg'
        ? 'image/jpeg'
        : ext === 'png'
        ? 'image/png'
        : 'application/octet-stream';

    formData.append('file', {
      uri: Platform.OS === 'android' ? imageUri : imageUri.replace('file://', ''),
      name: filename,
      type: mimeType,
    });

    try {
      console.log('📡 Uploading to backend...');

      // ❗ Replace with your actual live ngrok URL here every time you restart ngrok
      const response = await fetch('https://2773-124-217-126-229.ngrok-free.app', {
        method: 'POST',
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        body: formData,
      });

      console.log('🔄 Status code:', response.status);
      const data = await response.json();
      console.log('✅ Response from server:', data);

      if (!response.ok) {
        throw new Error(data?.detail || 'Detection failed');
      }

      setDetections(data.detections);
    } catch (error) {
      console.error('❌ Upload error:', error);
      Alert.alert('Detection Error', error.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center', padding: 20 }}>
      <Button title="Pick an Image" onPress={pickImage} />
      {imageUri && (
        <>
          <Image source={{ uri: imageUri }} style={{ width: 300, height: 300, marginVertical: 10 }} />
          <Button title="Detect Mealybug" onPress={uploadImage} />
        </>
      )}

      {isLoading && <ActivityIndicator size="large" color="#00ff00" style={{ marginTop: 20 }} />}

      {detections.length > 0 && (
        <View style={{ marginTop: 20 }}>
          <Text>Detections:</Text>
          {detections.map((det, index) => (
            <Text key={index}>
              🐛 {det.class} - {Math.round(det.confidence * 100)}% confidence
            </Text>
          ))}
        </View>
      )}
    </View>
  );
}
