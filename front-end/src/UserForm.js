import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./UserForm.css";

function UserForm() {

  var response = "";

  // React States
  const [output, setOutput] = useState('');


  const handleResponse = (response) => {
    if (response.status === 200) {
      return response.json()
    }
  }

  const handleValue = (value) => {
    setOutput("Predicted value is: " + parseFloat(value['price_predicted']).toFixed(1))
  }

  const handleError = (error) => {
    console.log(error);
  }

  const handleSubmit = (event) => {
    event.preventDefault();

    const formData = event.target.elements;

    const data = {
      "bed": formData[0].value,
      "bath": formData[1].value,
      "house_size": formData[2].value,
      "zip_code": formData[3].value
    };

    console.log(data);

    const requestOptions = {
      method: "POST",
      credentials: 'include',
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    };
    fetch("http://localhost:9001/predict", requestOptions)
      .then((response) => handleResponse(response))
      .then((value) => handleValue(value))
      .catch((error) => handleError(error));
  };



  // JSX code for login form
  const renderForm = (
    <div className="form">
      <form onSubmit={handleSubmit}>
        <div className="input-container">
          <label>Bed Number </label>
          <input type="text" name="bed" required />
        </div>
        <div className="input-container">
          <label>Bath Number </label>
          <input type="text" name="bath" required />
        </div>
        <div className="input-container">
          <label>House Size </label>
          <input type="text" name="house" required />
        </div>
        <div className="input-container">
          <label>Zip Code </label>
          <input type="text" name="zip" required />
        </div>
        <div className="button-container">
          <input type="submit" />
        </div>
      </form>
    </div>
  );

  return (
    <div className="app">
      <div className="user-form">
        <div className="title">Enter House Information For Prediction</div>
        {renderForm}
      </div>
      <div className="output-tag">{output}</div>
    </div>
  );
}

export default UserForm;
