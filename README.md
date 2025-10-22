# SWE40006 Project App - FRI-14:30-MD-G3

This repo contains an app to be deployed for the SWE40006 Project Presentation/Demonstration and Project Report assignments. The app is an old python web app made for assignment 3 of SWE30003. It hosts a simple e-commerce website which can do the following:
- Browse products (e.g., laptops) with prices/stock.
- Add/change/remove cart items, see total.
- Enter name/email/address to order.
- Mock payment with invoice.
- Admin panel to add/update/delete products.

## Prerequisites
- Docker installed
- Terminal

## Installation
### Latest Build
To install the project, download the latest release from Docker Hub by running:
```sh
docker pull sehaj170/swe-app:latest
```

### Building Manually
To build the project manually:
- Download the project zip.
- Open terminal, navigate to the project folder.
- Run:
```sh
docker build -t sehaj170/swe-app .
```

#### Testing
To test the project before building, run:
```sh
docker build -f Dockerfile.test -t swe-app-test .
docker run swe-app-test
```

## Running
- Run:
```sh
docker run -it -p 8000:8000 sehaj170/swe-app
```
- Open http://localhost:8000 in a browser.

Opening /metrics gives you information on how the thread you are on is running.

## Folder Structure
root/  
├── app.py              # Main app  
├── Dockerfile          # Dockerfile, container definition  
├── .github/workflows/  # GitHub automated CI/CD  
├── models/             # Code logic (e.g., shopping_cart.py)  
├── routes/             # Page routes (e.g., store_routes.py)  
├── templates/          # Web pages (e.g., home.html)  
├── static/css/         # Styles (styles.css)  
├── data/               # JSON data (e.g., products.json)  
