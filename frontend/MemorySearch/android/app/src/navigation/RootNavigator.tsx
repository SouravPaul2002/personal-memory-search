import React from "react";

import {
  NavigationContainer,
} from "@react-navigation/native";

import {
  createNativeStackNavigator,
} from "@react-navigation/native-stack";

import HomeScreen from "../screens/HomeScreen";
import SearchResultsScreen from "../screens/SearchResultsScreen";

const Stack =
  createNativeStackNavigator();

export default function RootNavigator() {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen
          name="Home"
          component={HomeScreen}
        />

        <Stack.Screen
          name="SearchResults"
          component={
            SearchResultsScreen
          }
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}