# 6893-project

All our code for model training are stored inside `./model-code/`.

Run `./install.sh` to install all the dependent software like node and python.

To deploy the app:

1. Host Python back-end application with `nohup python3 predict.py` to run the app as a background process

2. Change ip address in UserForm.js file to the ip address of the hosting machine

3. Go to root directory of the front-end application with `cd front-end` 

4. Use npm to build the application into production with `npm run build`

5. Host React front-end application with `pm2 serve -- build` to run the app as a background process

6. Note: The demo model we choose is the random forest model `rf_model.pkl`, you can replace it with your own model and adjust the name of the model in predict.py accordingly
