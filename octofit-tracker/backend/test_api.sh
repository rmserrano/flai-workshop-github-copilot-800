#!/bin/bash

# Test API endpoints for OctoFit Tracker
# This script tests all REST API endpoints

# Get codespace URL
if [ -z "$CODESPACE_NAME" ]; then
    BASE_URL="http://localhost:8000"
    echo "Testing on localhost..."
else
    BASE_URL="https://$CODESPACE_NAME-8000.app.github.dev"
    echo "Testing on Codespaces: $BASE_URL"
fi

echo ""
echo "=== Testing OctoFit Tracker API Endpoints ==="
echo ""

# Test API Root
echo "1. Testing API Root:"
curl -s "$BASE_URL/api/" | python3 -m json.tool
echo ""

# Test Users endpoint
echo "2. Testing Users endpoint:"
curl -s "$BASE_URL/api/users/" | python3 -m json.tool
echo ""

# Test Teams endpoint
echo "3. Testing Teams endpoint:"
curl -s "$BASE_URL/api/teams/" | python3 -m json.tool
echo ""

# Test Activities endpoint
echo "4. Testing Activities endpoint:"
curl -s "$BASE_URL/api/activities/" | python3 -m json.tool
echo ""

# Test Leaderboard endpoint
echo "5. Testing Leaderboard endpoint:"
curl -s "$BASE_URL/api/leaderboard/" | python3 -m json.tool
echo ""

# Test Workouts endpoint
echo "6. Testing Workouts endpoint:"
curl -s "$BASE_URL/api/workouts/" | python3 -m json.tool
echo ""

echo "=== API Testing Complete ==="
