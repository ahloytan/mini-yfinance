# Mini-yfinance
This project is a minified version of Yahoo Finance built to serve my brother's needs for specific and centralised financial data for his investment planning. Data pulled from [Yahoo Finance](https://finance.yahoo.com/quote/AAPL?p=AAPL) and [Finviz](https://finviz.com/), visualised with [ChartJS](https://www.chartjs.org/). Hosted on [Vercel](https://vercel.com/).

## Frontend
Tech stack: [VueJS](https://vuejs.org/), [Tailwind](https://tailwindcss.com/), [Vite](https://vitejs.dev/) <br>
Other libraries: Axios, VueX, ChartJS

## Backend
Tech stack: Flask (Python) <br>
Other libraries: yfinance, finviz, beautifulsoup

# How to set up
## Pre-requisites
1. Ensure you have [Node.js](https://nodejs.org/en/download) installed
2. Ensure you have [Python](https://www.python.org/downloads/) installed

## Frontend
1. Open command prompt, type in `cd frontend`
2. If this is your first time setting up, type `npm i`
3. Launch the project using `npm run dev`

## Backend
1. Open command prompt, type in `cd backend`
2. If this is your first time setting up the project, type `pip install -r requirements.txt`
3. To start the server, direct yourself to the `api` folder by entering `cd api` in the terminal and type in `python app.py`
4. Note: If you want to deploy a replica, please be reminded to set an environment variable (key=`ENV` and value=`production`) in the [Vercel](https://vercel.com/dashboard) settings page

## Deployment
1. Go to frontend folder. Type `npm run build`, followed by `vercel .` and `vercel --prod` after
2. Go to the root of the backend folder. Type `vercel .` and `vercel --prod` after

# Contact
1. To explore more of my works, head over to [Portfolio Website](https://ahloytan.netlify.app)
2. Feel free to contact me if there are issues or if there are opportunities that I can help you with!
