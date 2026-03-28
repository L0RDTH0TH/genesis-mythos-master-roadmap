---
title: API Documentation
created: 2026-03-14
tags: [templates, mdkit, api, software]
source: https://mdkit.io/templates/api-documentation
---

# API Documentation: User Service

## 🔑 Authentication
Include the `Authorization: Bearer <token>` header in all requests.

## 👤 Get User Profile
`GET /api/v1/users/:id`

### Parameters
| Name | Type | Description |
| :--- | :--- | :--- |
| id | string | The unique user ID |

### Response
```json
{
  "status": "success",
  "data": {
    "username": "johndoe",
    "email": "[email protected]"
  }
}
```
