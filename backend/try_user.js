#!/usr/bin/node
const fs = require('fs');
const request = require('request');

// Base URL for the API
const baseURL = 'http://localhost:5000/api';

// User data for POST and PUT requests
const userData = {
  full_name: 'John Doe',
  email: 'johndoe@example.com',
  phone_number: '1234567890',
  password: 'password',
  verification_status: 1,
  profile_picture: null,
  bio: 'This is John Doe',
  user_role: 1
};

// User data for POST and PUT requests
const updated_user = {
  full_name: 'John mukerson Doe',
  email: 'johndoe@example.com',
  phone_number: '1234567890',
  password: 'password',
  verification_status: 1,
  profile_picture: null,
  bio: 'This is John Doe',
  user_role: 1
};

// User ID for GET, PUT and DELETE requests
const userId = '4f307c09-00cd-4c86-87c4-b98910ae60ee';
const deleted_user_userId = '4f9b348c-a7d2-4bd9-8a3b-2cdd8f068bdf';

// GET all users
request(`${baseURL}/users`, function (error, response, body) {
  if (!error) {
    fs.writeFileSync('all_users.json', body);
  }
});

// GET a user by ID
request(`${baseURL}/users/${userId}`, function (error, response, body) {
  if (!error) {
    fs.writeFileSync('user.json', body);
  }
});

// POST a new user
request.post({
  url: `${baseURL}/users`,
  json: userData
}, function (error, response, body) {
  if (!error) {
    fs.writeFileSync('new_user.json', JSON.stringify(body));
  }
});

// PUT (update) a user
request.put({
  url: `${baseURL}/users/${userId}`,
  json: updated_user
}, function (error, response, body) {
  if (!error) {
    fs.writeFileSync('updated_user.json', JSON.stringify(body));
  }
});

// DELETE a user
request.delete(`${baseURL}/users/${deleted_user_userId}`, function (error, response, body) {
  if (!error) {
    fs.writeFileSync('deleted_user.json', body);
  }
});
