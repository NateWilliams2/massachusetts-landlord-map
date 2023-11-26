import GetParcel from './components/get-parcel.component';
import React, { Component } from "react";
import { AppRoutes } from "./routes";
import logo from './logo.svg';
import "bootstrap/dist/css/bootstrap.min.css";

class App extends Component {
  render() {
    return (
      <div className="App">
      {/* <Header /> */}
      <AppRoutes />
    </div>
    )
  }
}

export default App;
