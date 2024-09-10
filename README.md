# trader-trainer

## Introduction
Hi, my name is Mario, and I developed this project as part of software enginner training with Ed2Go, as part of certification for python skills.
This software is designed to serve those that what to learn how to trade without risking any real money.

## About Trader Trainer
Trader Trainer is a websoffware tha is avsilable in:
It was entirely design for training purposes and not to make real money


## User Stories
- As a customer I would like to be able to train my trading skills withou losing real money;
- As user, I would like to buy and sell stocks with real time prices so I know I'm dealing with real data;
- As a customer i would like to have real-time updates about my porfolio perfomance as the market changes in order to make decisions about my orders;
- As a client, I would like to reset my account whenever I want and I wand all my transactions records deleted.

## App Wireframes
All the app wireframes and system design can be found in this link: https://drive.google.com/file/d/1z3J8U5GAOfg7KtmiRaaC8dtjiZQnr8w8/view?usp=sharing


## How to use
1. Get informed about the Application on home and about page
2. Register an account
    - When registering, fill all the required fields. For this version no real email is necessary!
    - You don't need to worry about your data, it is safe. If you have doubts you can use fake data.
3. Upon registering, you can login, on login page, using your registed credentials.

### ON user dashboard
4. ON TOP: you'll find a welcome message along with your balance.
    - The settings can provides a panel with your registed information, plus add funds and reset account.
    - The logout button will take you back to login page
5. MARKET: provides informations about the stocks available to train with:
    - bid, ask, daily change and its symbol.
6. ORDERS: its form to perform buy and sell actions:
    - to buy: choose the symbol and set order to 'buy', set the amount of shares (volume) and submit
    - to sell: repeat the same process, except setting order to sell.
7. CHARTS: all symbol charts are connected with Market Symbols. Click on Market symbol to see your desired chart.
    - Beyond the chart, formation like symbol name and price can be found on the top of the charts.
8. PORTFOLIO: every time you buy a new stock it will be added to a porfolio:
    - the portfolio contains fields: name, symbol, volume, price and profit, to inform and guide you on your trading transactions
    - your volume increases when buying the same stock and decrease when selling.
    - the price for the same stock is the average of all prices when you bought the same stock
    - the profit is the difference between prices multiplied by volume of the transactions when selling.
9. TRANSACTION: it's not on user dashboard page but it can be accessed through settings:
    - it contains informations of all transactio that you made, buy or sell, time, volume and price is included on transaction list.

## Used Techologies
To build this Trader Trainer Software, I used Technologies like a desktop computer with Windows OS, and Visual Studio Code for programming the application.
- Softwares: python, django, javascript, html, css.
- other resources: internet

## Future improvements
For the future we intend to add features like: 
1. Indicators
2. Objects
3. Sell Operation without having to buy or own a stock
4. Email authentication
5. User email support
6. Add cryptocurrencies, commodities and futures
7. Improve system performance
