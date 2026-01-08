# Pizza Delivery API

A FastAPI-based pizza delivery service with user authentication and order management.

## Features

- User registration and authentication (JWT-based)
- Place pizza orders
- View order history
- Docker containerization with PostgreSQL

## Running with Docker

1. Build and run the application with Docker Compose:

   ```bash
   docker-compose up --build
   ```

2. The API will be available at `http://localhost:8000`

3. The PostgreSQL database will be available at `localhost:5432`

## Local Development

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Set up your local PostgreSQL database (the app will connect to `postgresql://postgres:Ke200207%40@localhost/pizza_delivery` by default).

3. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

## API Endpoints

### Authentication (`/auth`)

- `GET /auth/` - Hello message (requires authentication)
- `POST /auth/signup` - User registration
- `POST /auth/login` - User login

### Orders (`/orders`)

- `GET /orders/` - Hello message (requires authentication)
- `POST /orders/order` - Place a new order
- `GET /orders/orders` - Get user's orders
- `GET /orders/order/{order_id}` - Get specific order details
- `PUT /orders/order/update/{order_id}` - Update an order
- `DELETE /orders/order/delete/{order_id}` - Delete an order

## Environment Variables

You can override the default database connection by setting the `DATABASE_URL` environment variable:

```bash
export DATABASE_URL="postgresql://user:password@host:port/database"
```

## API Documentation

Once the server is running, visit `http://localhost:8000/docs` for interactive API documentation powered by Swagger UI.
