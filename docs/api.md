# API Documentation

## Health Check

### Get Health Status

**URL** : `/health`

**Method** : `GET`

**Auth required** : NO

**Description** : Returns the health status of the API service. Used for monitoring and deployment checks.

**Success Response**

**Code** : `200 OK`

**Content** : 
```json
{
    "status": "healthy"
}
```
