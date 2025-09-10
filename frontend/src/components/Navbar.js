import React from "react";
import { Link, useNavigate } from "react-router-dom";

function Navbar() {
  const navigate = useNavigate();
  const accessToken = localStorage.getItem("access");
  const user = localStorage.getItem("user"); // username/email stored at login

  const handleLogout = () => {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    localStorage.removeItem("user");
    navigate("/login");
  };

  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
      <div className="container">
        {/* Brand Name */}
        <Link className="navbar-brand" to="/">E-Commerce</Link>

        <button
          className="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span className="navbar-toggler-icon"></span>
        </button>

        <div className="collapse navbar-collapse" id="navbarNav">
          {/* Left Side Navigation */}
          <ul className="navbar-nav me-auto">
            {accessToken && (
              <>
                <li className="nav-item">
                  <Link className="nav-link" to="/categories">Categories</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/orders">Orders</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/cart">Cart</Link>
                </li>
              </>
            )}
          </ul>

          {/* Right Side Navigation */}
          <ul className="navbar-nav ms-auto">
            {!accessToken ? (
              <>
                <li className="nav-item">
                  <Link className="nav-link" to="/login">Login</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/register">Register</Link>
                </li>
              </>
            ) : (
              <>
                {/* Logout button */}
                <li className="nav-item">
                  <button
                    className="btn btn-danger me-3"
                    onClick={handleLogout}
                  >
                    Logout
                  </button>
                </li>
                {/* Username */}
                <li className="nav-item d-flex align-items-center">
                  <span className="navbar-text text-white">
                    {user}
                  </span>
                </li>
              </>
            )}
          </ul>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
