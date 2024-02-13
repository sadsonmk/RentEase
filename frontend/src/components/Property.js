import React from 'react'
import { Grid, Card, CardContent, CardMedia, CardActionArea } from '@mui/material';
import { Navigate } from 'react-router-dom';

const properties = [
    {
        id: 1,
        title: 'Apartment',
        description: 'a modern apartment building',
        image: '...',
        price: '$1,500/month',
        location: 'Beijing/China'
    }
];
const PropertyList = () => {
  return (
    <Grid container spacing={2}>
      {properties.map((property) => (
        <Grid item key={property.id}>
          <Card>
            <CardMedia 
              component='img'
              image={property.image}
              alt={property.title}
            />
            <CardContent>
              <CardActionArea onClick={() => Navigate(`/properties/${property.id}`)}>
                <h2>{property.title}</h2>
                <p>{property.price}</p>
                <p>{property.location}</p>
              </CardActionArea>
            </CardContent>

            
          </Card>
        </Grid>
      ))}
    </Grid>
  )
}

export default PropertyList