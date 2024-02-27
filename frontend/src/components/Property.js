import React from 'react'
import { Grid, Card, CardContent, CardMedia, CardActionArea } from '@mui/material';
// Remove the unused import statement for useHistory
import {  useNavigate } from 'react-router-dom';

// const properties = [
//     {
//         id: 1,
//         title: 'Apartment',
//         description: 'a modern apartment building',
//         image: '...',
//         price: '$1,500/month',
//         location: 'Beijing/China'
//     },
//     {
//       id: 2,
//       title: 'Apartment',
//       description: 'a modern apartment building',
//       image: '...',
//       price: '$2,500/month',
//       location: 'Shanghai/China'
//   }
// ];
const PropertyList = () => {
  const navigate = useNavigate();

  const handleCardClick = (propertyId) => {
    navigate(`/properties/${propertyId}`);
  };
  const [properties, setProperties] = React.useState([]);

  React.useEffect(() => {
    fetch('http://127.0.0.1:5000/api/home')
      .then((response) => response.json())
      .then((data) => setProperties(data));
      
  }, []);

  return (
    <div>
      <h1>Properties</h1>
    <Grid container spacing={2}>
      {properties.length > 0 ? (properties.map((property) => (
        <Grid item key={property.id}>
          <Card>
            <CardMedia 
              component='img'
              image={property.image}
              alt={property.title}
            />
            <CardContent>
              <CardActionArea onClick={() => handleCardClick(property.id)}>
                <h2>{property.title}</h2>
                <p>{property.price}</p>
                <p>{property.location}</p>
              </CardActionArea>
            </CardContent>

            
          </Card>
        </Grid>
      ))) : (
        <p>No properties found</p>
      )}
    </Grid>
    </div>
  )
}

export default PropertyList