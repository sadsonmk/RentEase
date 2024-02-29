#!/usr/bin/node
const fs = require('fs');
const request = require('request');

// Base URL for the API
const baseURL = 'http://localhost:5000/api';

// Property data for POST and PUT requests
const propertyData = {
  user_id: '24b8b743-910f-49d3-952f-c9c5623d0a6e', // Replace with actual user ID
  title: 'Beautiful Beach House',
  description: 'This is a beautiful beach house with 3 bedrooms and 2 bathrooms.',
  location: '123 Beach Ave, Miami, FL 33139',
  address: '123 Beach Ave, Miami, FL 33139',
  type: 'House',
  picture: 'path-to-your-image.jpg', // Replace with actual path to image
  price: 500.02,
  availability: true,
  miscellaneous: 'No pets allowed'
};
// Property data for POST and PUT requests
const updatedProperty = {
  // your updated property data here
};

// Property ID for GET, PUT and DELETE requests
const propertyId = 'your-property-id-here';
const deletedPropertyId = 'your-deleted-property-id-here';

// GET all properties
request(`${baseURL}/properties`, function (error, response, body) {
  if (!error) {
    fs.writeFileSync('all_properties.json', body);
  }
});

// GET a property by ID
// request(`${baseURL}/properties/${propertyId}`, function (error, response, body) {
//   if (!error) {
//     fs.writeFileSync('property.json', body);
//   }
// });

// POST a new property
request.post({
  url: `${baseURL}/properties`,
  json: propertyData
}, function (error, response, body) {
  if (!error) {
    fs.writeFileSync('new_property.json', JSON.stringify(body));
  }
});

// PUT (update) a property
// request.put({
//   url: `${baseURL}/properties/${propertyId}`,
//   json: updatedProperty
// }, function (error, response, body) {
//   if (!error) {
//     fs.writeFileSync('updated_property.json', JSON.stringify(body));
//   }
// });

// DELETE a property
// request.delete(`${baseURL}/properties/${deletedPropertyId}`, function (error, response, body) {
//   if (!error) {
//     fs.writeFileSync('deleted_property.json', body);
//   }
// });