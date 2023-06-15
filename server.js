const stripe = require('stripe')('sk_test_51MlYkNCOdchHMTkEcb6YxDUGXohGBegQlolP44YYikQGJ7Iqq2iAiMtD1nOJywcT7dkVVlJ3pW9JvpJiqQ2BrWSv00CaHhxSgf');

const express= require('express');
const bodyparser=require('body-parser');
const app = express();



app.use(bodyparser.json())

app.get('/',(req,res)=>{
    res.send("Hello mfrs")
})


app.post('/payment-sheet', async (req, res) => {

    const {amount}=req.body;

  const customer = await stripe.customers.create();
  const ephemeralKey = await stripe.ephemeralKeys.create(
    {customer: customer.id},
    {apiVersion: '2022-11-15'}
  );
  const paymentIntent = await stripe.paymentIntents.create({
    amount: amount,
    currency: 'usd',
    customer: customer.id,
    automatic_payment_methods: {
      enabled: true,
    },
  });

  res.json({
    paymentIntent: paymentIntent.client_secret,
    ephemeralKey: ephemeralKey.secret,
    customer: customer.id,
    
  });
});



app.listen(4002,()=>console.log("Running on http://192.168.45.80:4002"))