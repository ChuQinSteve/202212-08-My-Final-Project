import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./UserForm.css";

function UserForm() {

  var response = "";

  // React States
  const [output, setOutput] = useState({});


  const handleResponse = (response) => {
    console.log(response)
    if (response.status === 200) {
      return response.json()
    }
    else {
      throw response.text()
    }
  }

  const handleError = (error) => {
    return error;
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

    const requestOptions = {
      method: "POST",
      credentials: 'include',
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    };
    fetch("http://localhost:9001/predict", requestOptions)
      .then((response) => handleResponse(response))
      .then((value) => {
        setOutput({value: "Predicted value is: " + parseFloat(value['price_predicted']).toFixed(1),
                    color: 'black'})
      })
      .catch((error) => handleError(error))
      .then((value) => {
        if (value !== undefined) setOutput({value: "Error: " + value,
                                            color: '#FF4504'})
      });
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
      <div className="vislink">
        <label>Checkout our dataset visualization </label>
        <a className="vis" href="./Visualization.html">Here</a>
      </div>
      <div className="user-form">
        <div className="title">Enter House Information For Prediction</div>
        {renderForm}
      </div>
      <div className="output-tag" style={{ color: output.color }}>{output.value}</div>
    </div>
  );
}

export default UserForm;
