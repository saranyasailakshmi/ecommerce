import React from "react";
import { Link } from "react-router-dom";

function Home() {
  return (
    <div className="container mt-5 text-center">
      <h1>Welcome to E-Commerce</h1>
      <p>Please login or register to continue.</p>
      <div className="mt-4">
        <Link to="/login" className="btn btn-success mx-2">Login</Link>
        <Link to="/register" className="btn btn-primary mx-2">Register</Link>
      </div>
    </div>
  );
}

export default Home;
