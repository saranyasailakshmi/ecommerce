import React, { useEffect, useState } from "react";
import api from "../api";

function Categories() {
  const [categories, setCategories] = useState([]);
  const accessToken = localStorage.getItem("access");

  useEffect(() => {
    fetchCategories();
  }, []);

  const fetchCategories = async () => {
    try {
      const res = await api.get("/product/categories/list/", {
        headers: { Authorization: `Bearer ${accessToken}` },
      });
      setCategories(res.data.data);
    } catch (err) {
      console.error("Error fetching categories:", err);
    }
  };

  return (
    <div className="container mt-5">
      <h2>Categories</h2>
      <div className="row">
        {categories.map((cat) => (
          <div className="col-md-4 mb-3" key={cat.id}>
            <div className="card">
              <div className="card-body">
                <h5 className="card-title">{cat.name}</h5>
                <p className="card-text">{cat.description}</p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Categories;
