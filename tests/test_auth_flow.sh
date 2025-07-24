#!/bin/bash

# Test Authentication Flow for AI Career Discovery Assistant
# This script tests the complete authentication flow

echo "=== Testing Authentication Flow ==="
echo

# Base URL
API_BASE="http://localhost:8000/api/v1"

# Test data
TEST_EMAIL="test$(date +%s)@example.com"
TEST_PASSWORD="testpassword123"
TEST_NAME="Test User"

echo "1. Testing User Registration"
echo "   POST $API_BASE/auth/register"
REGISTER_RESPONSE=$(curl -s -X POST "$API_BASE/auth/register" \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": \"$TEST_EMAIL\",
    \"password\": \"$TEST_PASSWORD\",
    \"full_name\": \"$TEST_NAME\"
  }")

echo "   Response: $REGISTER_RESPONSE"
echo

echo "2. Testing User Login"
echo "   POST $API_BASE/auth/login"
LOGIN_RESPONSE=$(curl -s -X POST "$API_BASE/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=$TEST_EMAIL&password=$TEST_PASSWORD")

TOKEN=$(echo $LOGIN_RESPONSE | jq -r '.access_token')
echo "   Token: ${TOKEN:0:20}..."
echo

echo "3. Testing Protected Endpoint"
echo "   GET $API_BASE/users/me"
ME_RESPONSE=$(curl -s -X GET "$API_BASE/users/me" \
  -H "Authorization: Bearer $TOKEN")

echo "   Response: $ME_RESPONSE"
echo

echo "4. Testing Invalid Token"
echo "   GET $API_BASE/users/me (with invalid token)"
INVALID_RESPONSE=$(curl -s -X GET "$API_BASE/users/me" \
  -H "Authorization: Bearer invalid_token_here")

echo "   Response: $INVALID_RESPONSE"
echo

echo "=== Authentication Flow Test Complete ==="