import React from "react";
import {
  View,
  Text,
  Button,
  StyleSheet
} from "react-native";

export default function HomeScreen({
  navigation,
}: any) {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>
        Personal Memory Search
      </Text>

      <Button
        title="Go To Results"
        onPress={() =>
          navigation.navigate(
            "SearchResults"
          )
        }
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
  },

  title: {
    fontSize: 24,
    fontWeight: "bold",
    marginBottom: 20,
  },
});